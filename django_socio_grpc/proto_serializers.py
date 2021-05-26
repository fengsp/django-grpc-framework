from google.protobuf.pyext._message import RepeatedCompositeContainer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    LIST_SERIALIZER_KWARGS,
    BaseSerializer,
    ListSerializer,
    ModelSerializer,
    Serializer,
)
from rest_framework.settings import api_settings

from django_socio_grpc.protobuf.json_format import message_to_dict, parse_dict

LIST_PROTO_SERIALIZER_KWARGS = (*LIST_SERIALIZER_KWARGS, "message_list_attr", "message")


class BaseProtoSerializer(BaseSerializer):
    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message", None)
        self.stream = kwargs.pop("stream", None)
        self.message_list_attr = kwargs.pop("message_list_attr", None)
        if message is not None:
            self.initial_message = message
            kwargs["data"] = self.message_to_data(message)
        super().__init__(*args, **kwargs)

    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes."""
        raise NotImplementedError("`message_to_data()` must be implemented.")

    def data_to_message(self, data):
        """Protobuf message <- Dict of python primitive datatypes."""
        raise NotImplementedError("`data_to_message()` must be implemented.")

    @property
    def message(self):
        if not hasattr(self, "_message"):
            self._message = self.data_to_message(self.data)
        return self._message

    @classmethod
    def many_init(cls, *args, **kwargs):
        allow_empty = kwargs.pop("allow_empty", None)
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {"child": child_serializer}
        if allow_empty is not None:
            list_kwargs["allow_empty"] = allow_empty
        list_kwargs.update(
            {
                key: value
                for key, value in kwargs.items()
                if key in LIST_PROTO_SERIALIZER_KWARGS
            }
        )
        meta = getattr(cls, "Meta", None)
        list_serializer_class = getattr(meta, "list_serializer_class", ListProtoSerializer)
        return list_serializer_class(*args, **list_kwargs)


class ProtoSerializer(BaseProtoSerializer, Serializer):
    def message_to_data(self, message):
        """Protobuf message -> Dict of python primitive datatypes."""
        return message_to_dict(message)

    def data_to_message(self, data):
        """Protobuf message <- Dict of python primitive datatypes."""
        assert hasattr(
            self, "Meta"
        ), 'Class {serializer_class} missing "Meta" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        assert hasattr(
            self.Meta, "proto_class"
        ), 'Class {serializer_class} missing "Meta.proto_class" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        return parse_dict(data, self.Meta.proto_class())


class ListProtoSerializer(ListSerializer, BaseProtoSerializer):
    def message_to_data(self, message):
        """
        List of protobuf messages -> List of dicts of python primitive datatypes.
        """

        if self.message_list_attr is None:
            raise TypeError("message_list_attr is NoneType")

        repeated_message = getattr(message, self.message_list_attr, "")
        if not isinstance(repeated_message, RepeatedCompositeContainer):
            error_message = self.default_error_messages["not_a_list"].format(
                input_type=repeated_message.__class__.__name__
            )
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: [error_message]}, code="not_a_list"
            )
        ret = []
        for item in repeated_message:
            ret.append(self.child.message_to_data(item))
        return ret

    def data_to_message(self, data):
        """
        List of protobuf messages <- List of dicts of python primitive datatypes.
        """
        assert hasattr(
            self.child, "Meta"
        ), 'Class {serializer_class} missing "Meta" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        assert hasattr(
            self.child.Meta, "proto_class_list"
        ), 'Class {serializer_class} missing "Meta.proto_class_list" attribute'.format(
            serializer_class=self.__class__.__name__
        )

        if getattr(self.child, "stream", False):
            return [self.child.data_to_message(item) for item in data]
        else:
            response = self.child.Meta.proto_class_list()
            response.results.extend([self.child.data_to_message(item) for item in data])
            return response


class ModelProtoSerializer(ProtoSerializer, ModelSerializer):
    pass
