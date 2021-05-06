from asgiref.sync import sync_to_async
from google.protobuf import empty_pb2

from django_socio_grpc.settings import grpc_settings


############################################################
#   Synchronous mixins                                     #
############################################################
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

    @staticmethod
    def get_default_method(model_name):
        return {
            "Create": {
                "request": {"is_stream": False, "message": model_name},
                "response": {"is_stream": False, "message": model_name},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields="__all__"):
        return {
            model_name: fields,
        }


class ListModelMixin:
    def List(self, request, context):
        """
        List a queryset.  This sends a message array of
        ``serializer.Meta.proto_class`` to the client.

        .. note::

            This is a server streaming RPC.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if hasattr(serializer.message, "count"):
                serializer.message.count = self.paginator.page.paginator.count
            return serializer.message
        else:
            serializer = self.get_serializer(queryset, many=True)
            return serializer.message

    @staticmethod
    def get_default_method(model_name):
        return {
            "List": {
                "request": {"is_stream": False, "message": f"{model_name}ListRequest"},
                "response": {"is_stream": False, "message": f"{model_name}ListResponse"},
            },
        }

    @staticmethod
    def get_default_message(
        model_name, fields=None, pagination=None, response_field_name="results"
    ):
        if fields is None:
            fields = []
        # If user let default choose for pagination we check if there is a default pagination class setted
        if pagination is None:
            pagination = grpc_settings.DEFAULT_PAGINATION_CLASS is not None

        response_fields = [f"__custom__repeated {model_name}__{response_field_name}__"]
        if pagination:
            response_fields += ["__custom__int32__count__"]
        return {
            f"{model_name}ListRequest": fields,
            f"{model_name}ListResponse": response_fields,
        }


class StreamModelMixin:
    def Stream(self, request, context):
        """
        List a queryset.  This sends a sequence of messages of
        ``serializer.Meta.proto_class`` to the client.

        .. note::

            This is a server streaming RPC.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, stream=True)
        else:
            serializer = self.get_serializer(queryset, many=True, stream=True)

        for message in serializer.message:
            yield message

    @staticmethod
    def get_default_method(model_name):
        return {
            "Stream": {
                "request": {"is_stream": False, "message": f"{model_name}StreamRequest"},
                "response": {"is_stream": True, "message": model_name},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields=None):
        if fields is None:
            fields = []
        return {
            f"{model_name}StreamRequest": fields,
        }


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

    @staticmethod
    def get_default_method(model_name):
        return {
            "Retrieve": {
                "request": {"is_stream": False, "message": f"{model_name}RetrieveRequest"},
                "response": {"is_stream": False, "message": model_name},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields="__pk__"):
        return {
            f"{model_name}RetrieveRequest": fields,
        }


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

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return serializer.message

    def perform_update(self, serializer):
        """Save an existing object instance."""
        serializer.save()

    @staticmethod
    def get_default_method(model_name):
        return {
            "Update": {
                "request": {"is_stream": False, "message": model_name},
                "response": {"is_stream": False, "message": model_name},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields="__all__"):
        return {
            f"{model_name}UpdateRequest": fields,
        }


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

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return serializer.message

    def perform_partial_update(self, serializer):
        """Save an existing object instance."""
        serializer.save()

    @staticmethod
    def get_default_method(model_name):
        return {
            "Update": {
                "request": {"is_stream": False, "message": model_name},
                "response": {"is_stream": False, "message": model_name},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields="__all__"):
        return {
            f"{model_name}PartialUpdateRequest": fields,
        }


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

    @staticmethod
    def get_default_method(model_name):
        return {
            "Destroy": {
                "request": {"is_stream": False, "message": f"{model_name}DestroyRequest"},
                "response": {"is_stream": False, "message": "google.protobuf.Empty"},
            },
        }

    @staticmethod
    def get_default_message(model_name, fields="__pk__"):
        return {
            f"{model_name}DestroyRequest": fields,
        }


############################################################
#   Asynchronous mixins                                    #
############################################################


class AsyncCreateModelMixin(CreateModelMixin):
    async def Create(self, request, context):
        async_parent_method = sync_to_async(super().Create)
        return await async_parent_method(request, context)


class AsyncListModelMixin(ListModelMixin):
    async def List(self, request, context):
        async_parent_method = sync_to_async(super().List)
        return await async_parent_method(request, context)


class AsyncStreamModelMixin(StreamModelMixin):
    @sync_to_async
    def _get_list_data(self):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, stream=True)
        else:
            serializer = self.get_serializer(queryset, many=True, stream=True)

        return serializer.message

    async def Stream(self, request, context):
        """
        List a queryset.  This sends a sequence of messages of
        ``serializer.Meta.proto_class`` to the client.

        .. note::

            This is a server streaming RPC.
        """
        messages = await self._get_list_data()
        for message in messages:
            context.write(message)


class AsyncRetrieveModelMixin(RetrieveModelMixin):
    async def Retrieve(self, request, context):
        async_parent_method = sync_to_async(super().Retrieve)
        return await async_parent_method(request, context)


class AsyncUpdateModelMixin(UpdateModelMixin):
    async def Update(self, request, context):
        async_parent_method = sync_to_async(super().Update)
        return await async_parent_method(request, context)


class AsyncPartialUpdateModelMixin(PartialUpdateModelMixin):
    async def PartialUpdate(self, request, context):
        async_parent_method = sync_to_async(super().PartialUpdate)
        return await async_parent_method(request, context)


class AsyncDestroyModelMixin(DestroyModelMixin):
    async def Destroy(self, request, context):
        async_parent_method = sync_to_async(super().Destroy)
        return await async_parent_method(request, context)


############################################################
#   Default grpc messages                                  #
############################################################


def get_default_grpc_methods(model_name):
    """
    return the default grpc methods generated for a django model.
    """
    return {
        **ListModelMixin.get_default_method(model_name),
        **CreateModelMixin.get_default_method(model_name),
        **RetrieveModelMixin.get_default_method(model_name),
        **UpdateModelMixin.get_default_method(model_name),
        **DestroyModelMixin.get_default_method(model_name),
    }


def get_default_grpc_messages(model_name):
    """
    return the default protobuff message we want to generate
    """
    return {
        **CreateModelMixin.get_default_message(model_name),
        **ListModelMixin.get_default_message(model_name),
        **RetrieveModelMixin.get_default_message(model_name),
        **DestroyModelMixin.get_default_message(model_name),
    }
