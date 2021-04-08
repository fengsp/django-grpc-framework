from functools import update_wrapper

import grpc
from django import db
from django.db.models.query import QuerySet

from django_socio_grpc.request_transformer.grpc_socio_proxy_context import (
    GRPCSocioProxyContext,
)
from django_socio_grpc.settings import grpc_settings


class Service:

    authentication_classes = grpc_settings.DEFAULT_AUTHENTICATION_CLASSES

    def __init__(self, **kwargs):
        """
        Set kwargs as self attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def perform_authentication(self):
        user_auth_tuple = self.resolve_user()
        if user_auth_tuple:
            self.context.user = user_auth_tuple[0]
            self.context.token = user_auth_tuple[1]
        else:
            self.context.user = None
            self.context.token = None

    def resolve_user(self):
        auth_responses = [
            auth().authenticate(self.context) for auth in self.authentication_classes
        ]
        if auth_responses:
            return auth_responses[0]
        return None

    def before_action(self):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.perform_authentication()
        # self.check_permissions(request)

    @classmethod
    def as_servicer(cls, **initkwargs):
        """
        Returns a gRPC servicer instance::

            servicer = PostService.as_servicer()
            add_PostControllerServicer_to_server(servicer, server)
        """
        for key in initkwargs:
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. as_servicer only "
                    "accepts arguments that are already attributes of the "
                    "class." % (cls.__name__, key)
                )
        if isinstance(getattr(cls, "queryset", None), QuerySet):

            def force_evaluation():
                raise RuntimeError(
                    "Do not evaluate the `.queryset` attribute directly, "
                    "as the result will be cached and reused between requests."
                    " Use `.all()` or call `.get_queryset()` instead."
                )

            cls.queryset._fetch_all = force_evaluation

        class Servicer:
            def __getattr__(self, action):
                if not hasattr(cls, action):
                    return not_implemented

                def handler(request, context):
                    # db connection state managed similarly to the wsgi handler
                    db.reset_queries()
                    db.close_old_connections()
                    try:
                        self = cls(**initkwargs)
                        self.request = request
                        self.context = GRPCSocioProxyContext(context)
                        self.action = action
                        self.before_action()
                        return getattr(self, action)(self.request, self.context)
                    finally:
                        db.close_old_connections()

                update_wrapper(handler, getattr(cls, action))
                return handler

        update_wrapper(Servicer, cls, updated=())
        return Servicer()


def not_implemented(request, context):
    """Method not implemented"""
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details("Method not implemented!")
    raise NotImplementedError("Method not implemented!")
