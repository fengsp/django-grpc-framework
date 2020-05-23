from google.protobuf import empty_pb2


class CreateModelMixin:
    def Create(self, request, context):
        """
        Create a model instance.

        The request should be a proto message of ``serializer.Meta.proto_class``.
        If an object is created this returns a proto message of
        ``serializer.Meta.proto_class``.
        """
        serializer = self.get_serializer(message=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.message

    def perform_create(self, serializer):
        """Save a new object instance."""
        serializer.save()


class ListModelMixin:
    def List(self, request, context):
        """
        List a queryset.  This sends a sequence of messages of
        ``serializer.Meta.proto_class`` to the client.

        .. note::

            This is a server streaming RPC.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for message in serializer.message:
            yield message


class RetrieveModelMixin:
    def Retrieve(self, request, context):
        """
        Retrieve a model instance.

        The request have to include a field corresponding to
        ``lookup_request_field``.  If an object can be retrieved this returns
        a proto message of ``serializer.Meta.proto_class``.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return serializer.message


class UpdateModelMixin:
    def Update(self, request, context):
        """
        Update a model instance.

        The request should be a proto message of ``serializer.Meta.proto_class``.
        If an object is updated this returns a proto message of
        ``serializer.Meta.proto_class``.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, message=request)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return serializer.message

    def perform_update(self, serializer):
        """Save an existing object instance."""
        serializer.save()


class PartialUpdateModelMixin:
    def PartialUpdate(self, request, context):
        """
        Partial update a model instance.

        The request have to include a field corresponding to
        ``lookup_request_field`` and you need to explicitly set the fields that
        you want to update.  If an object is updated this returns a proto
        message of ``serializer.Meta.proto_class``.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, message=request, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_partial_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return serializer.message

    def perform_partial_update(self, serializer):
        """Save an existing object instance."""
        serializer.save()


class DestroyModelMixin:
    def Destroy(self, request, context):
        """
        Destroy a model instance.

        The request have to include a field corresponding to
        ``lookup_request_field``.  If an object is deleted this returns
        a proto message of ``google.protobuf.empty_pb2.Empty``.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return empty_pb2.Empty()

    def perform_destroy(self, instance):
        """Delete an object instance."""
        instance.delete()
