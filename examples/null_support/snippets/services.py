from django_grpc_framework import generics, mixins
from django_grpc_framework import proto_serializers
from snippets.models import Snippet
import snippets_pb2
from google.protobuf.struct_pb2 import NullValue


class SnippetProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Snippet
        fields = '__all__'

    def message_to_data(self, message):
        data = {
            'title': message.title,
        }
        if message.language.HasField('value'):
            data['language'] = message.language.value
        elif message.language.HasField('null'):
            data['language'] = None
        return data

    def data_to_message(self, data):
        message = snippets_pb2.Snippet(
            id=data['id'],
            title=data['title'],
        )
        if data['language'] is None:
            message.language.null = NullValue.NULL_VALUE
        else:
            message.language.value = data['language']
        return message


class SnippetService(mixins.UpdateModelMixin,
                     generics.GenericService):
    queryset = Snippet.objects.all()
    serializer_class = SnippetProtoSerializer
