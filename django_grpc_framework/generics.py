from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
import grpc

from django_grpc_framework import mixins, services


class GenericService(services.Service):
    """
    Base class for all other generic services.
    """
    # Either set this attribute or override ``get_queryset()``.
    queryset = None
    # Either set this attribute or override ``get_serializer_class()``.
    serializer_class = None
    # Either set this attribute or override ``get_protobuf_class``.
    protobuf_class = None
    # Set this if you want to use object lookups other than id
    lookup_field = 'id'
    lookup_request_field = None

    def get_queryset(self):
        """
        Get the list of items for this service.
        This must be an iterable, and may be a queryset.
        Defaults to using ``self.queryset``.

        If you are overriding a handler method, it is important that you call
        ``get_queryset()`` instead of accessing the ``queryset`` attribute as
        ``queryset`` will get evaluated only once.
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
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def get_protobuf_class(self):
        """
        Return the class to use for the protobuf message.
        Defaults to using `self.protobuf_class`.
        """
        assert self.protobuf_class is not None, (
            "'%s' should either include a `protobuf_class` attribute, "
            "or override the `get_protobuf_class()` method."
            % self.__class__.__name__
        )
        return self.protobuf_class

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_request_field = self.lookup_request_field or self.lookup_field
        assert hasattr(self.request, lookup_request_field), (
            'Expected service %s to be called with request that has a field '
            'named "%s". Fix your request protocol definition, or set the '
            '`.lookup_field` attribute on the service correctly.' %
            (self.__class__.__name__, lookup_request_field)
        )
        lookup_value = getattr(self.request, lookup_request_field)
        filter_kwargs = {self.lookup_field: lookup_value}
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
        Extra context provided to the serializer class.
        """
        return {
            'grpc_request': self.request,
            'grpc_context': self.context,
        }

    def filter_queryset(self, queryset):
        return queryset


class CreateService(mixins.CreateModelMixin,
                    GenericService):
    """
    Concrete service for creating a model instance.
    """
    pass


class ListService(mixins.ListModelMixin,
                  GenericService):
    """
    Concrete service for listing a queryset.
    """
    pass


class RetrieveService(mixins.RetrieveModelMixin,
                      GenericService):
    """
    Concrete service for retrieving a model instance.
    """
    pass


class DestroyService(mixins.DestroyModelMixin,
                     GenericService):
    """
    Concrete service for deleting a model instance.
    """
    pass


class UpdateService(mixins.UpdateModelMixin,
                    GenericService):
    """
    Concrete service for updating a model instance.
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
