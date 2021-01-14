import grpc
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.request import HttpRequest, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.settings import api_settings

from django_grpc_framework import mixins, services
from django_grpc_framework.utils import model_meta


class GenericService(services.Service):
    """
    Base class for all other generic services.
    """
    # Either set this attribute or override ``get_queryset()``.
    queryset = None
    # Either set this attribute or override ``get_serializer_class()``.
    serializer_class = None
    # Set this if you want to use object lookups other than id
    lookup_field = None
    lookup_request_field = None

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    def get_queryset(self):
        """
        Get the list of items for this service.
        This must be an iterable, and may be a queryset.
        Defaults to using ``self.queryset``.

        If you are overriding a handler method, it is important that you call
        ``get_queryset()`` instead of accessing the ``queryset`` attribute as
        ``queryset`` will get evaluated only once.

        Override this to provide dynamic behavior, for example::

            def get_queryset(self):
                if self.action == 'ListSpecialUser':
                    return SpecialUser.objects.all()
                return super().get_queryset()
        """
        assert self.queryset is not None, (
            "'%s' should either include a ``queryset`` attribute, "
            "or override the ``get_queryset()`` method."
            % self.__class__.__name__
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        """
        Return the class to use for the serializer. Defaults to using
        `self.serializer_class`.
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def get_object(self):
        """
        Returns an object instance that should be used for detail services.
        Defaults to using the lookup_field parameter to filter the base
        queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())
        lookup_field = (
            self.lookup_field
            or model_meta.get_model_pk(queryset.model).name
        )
        lookup_request_field = self.lookup_request_field or lookup_field
        assert hasattr(self.request, lookup_request_field), (
            'Expected service %s to be called with request that has a field '
            'named "%s". Fix your request protocol definition, or set the '
            '`.lookup_field` attribute on the service correctly.' %
            (self.__class__.__name__, lookup_request_field)
        )
        lookup_value = getattr(self.request, lookup_request_field)
        filter_kwargs = {lookup_field: lookup_value}
        try:
            return get_object_or_404(queryset, **filter_kwargs)
        except (TypeError, ValueError, ValidationError, Http404):
            self.context.abort(grpc.StatusCode.NOT_FOUND, (
                '%s: %s not found!' %
                (queryset.model.__name__, lookup_value)
            ))

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.  Defaults to including
        ``grpc_request``, ``grpc_context``, and ``service`` keys.
        """
        return {
            'grpc_request': self.request,
            'grpc_context': self.context,
            'service': self,
        }

    def filter_queryset(self, queryset):
        """Given a queryset, filter it, returning a new queryset."""
        keys = self.request.DESCRIPTOR.fields_by_name.keys()
        request = HttpRequest()
        query_params = QueryDict('', mutable=True)
        query_params.update(dict(zip([k for k in keys], [getattr(self.request, k) for k in keys])))
        request.query_params = query_params
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset


class CreateService(mixins.CreateModelMixin,
                    GenericService):
    """
    Concrete service for creating a model instance that provides a ``Create()``
    handler.
    """
    pass


class ListService(mixins.ListModelMixin,
                  GenericService):
    """
    Concrete service for listing a queryset that provides a ``List()`` handler.
    """
    pass


class RetrieveService(mixins.RetrieveModelMixin,
                      GenericService):
    """
    Concrete service for retrieving a model instance that provides a
    ``Retrieve()`` handler.
    """
    pass


class DestroyService(mixins.DestroyModelMixin,
                     GenericService):
    """
    Concrete service for deleting a model instance that provides a ``Destroy()``
    handler.
    """
    pass


class UpdateService(mixins.UpdateModelMixin,
                    GenericService):
    """
    Concrete service for updating a model instance that provides a
    ``Update()`` handler.
    """
    pass


class ReadOnlyModelService(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericService):
    """
    Concrete service that provides default ``List()`` and ``Retrieve()``
    handlers.
    """
    pass


class ModelService(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericService):
    """
    Concrete service that provides default ``Create()``, ``Retrieve()``,
    ``Update()``, ``Destroy()`` and ``List()`` handlers.
    """
    pass
