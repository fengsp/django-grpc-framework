from functools import update_wrapper

import grpc
from django import db
from django.db.models.query import QuerySet
from django.http import Http404
from rest_framework import exceptions

from django_grpc_framework.settings import grpc_settings


def find_unique_value_error(exc_detail):
    """Find unique value error in exception details."""
    for field, errors in exc_detail.items():  # noqa: B007
        for error in errors:
            if error.code == 'unique':
                return error

    return None


def parse_validation_error(exc, context):
    """If code == `unique` return grpc.StatusCode.ALREADY_EXISTS."""
    if isinstance(exc.detail, dict):
        error = find_unique_value_error(exc.detail)
        if error:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, error)
            return

    context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))


def exception_handler(exc: Exception, context) -> None:  # noqa: WPS231
    """
    Returns the response that should be used for any given exception.

    Any unhandled exceptions will return grpc.StatusCode.INTERNAL: Internal error.
    """
    if isinstance(exc, (Http404, exceptions.NotFound)):  # noqa: WPS223
        context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
        return
    elif isinstance(exc, exceptions.ValidationError):
        parse_validation_error(exc, context)
        return

    raise exc


class Service:

    settings = grpc_settings

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
                    try:
                        self = cls(**initkwargs)
                        self.action = action
                        self.context = context
                        self.request = request
                        return getattr(self, action)(request, context)
                    except Exception as exc:
                        self.handle_exception(exc)
                    finally:
                        db.close_old_connections()

                update_wrapper(handler, getattr(cls, action))
                return handler

        update_wrapper(Servicer, cls, updated=())
        return Servicer()

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        exception_handler(exc, context)

    def get_exception_handler_context(self):
        """
        Returns a dict that is passed through to EXCEPTION_HANDLER,
        as the `context` argument.
        """
        return getattr(self, 'context', None)

    def get_exception_handler(self):
        """
        Returns the exception handler that this view uses.
        """
        return self.settings.EXCEPTION_HANDLER


def not_implemented(request, context):
    """Method not implemented"""
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')
