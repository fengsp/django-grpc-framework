from functools import update_wrapper

import grpc
from django import db
from django.db.models.query import QuerySet
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.settings import api_settings


class Service:
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        if isinstance(getattr(cls, 'queryset', None), QuerySet):
            def force_evaluation():
                raise RuntimeError(
                    'Do not evaluate the `.queryset` attribute directly, '
                    'as the result will be cached and reused between requests.'
                    ' Use `.all()` or call `.get_queryset()` instead.'
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
                        self.context = self.initialize_context(context)
                        self.action = action
                        return getattr(self, action)(request, context)
                    finally:
                        db.close_old_connections()
                update_wrapper(handler, getattr(cls, action))
                return handler
        update_wrapper(Servicer, cls, updated=())
        return Servicer()

    def initialize_context(self,  context: grpc.ServicerContext, *args, **kwargs):
        """
        Returns the initial request object.
        """
        # parser_context = cls.get_parser_context(request)
        request = HttpRequest()
        request.META = dict(context.invocation_metadata())
        r = Request(
            request,
            authenticators=self.get_authenticators(),
            # negotiator=self.get_content_negotiator(),
            # parser_context=parser_context
        )
        context.user = r.user
        self.check_permissions(r, context)
        return context

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request, context):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    context,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None),
                )

    def permission_denied(self, request, context: grpc.ServicerContext, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, details=message if message else '')
            # raise exceptions.NotAuthenticated()
        context.abort(grpc.StatusCode.PERMISSION_DENIED, details=message if message else '')
        # raise exceptions.PermissionDenied(detail=message, code=code)


def not_implemented(request, context):
    """Method not implemented"""
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
