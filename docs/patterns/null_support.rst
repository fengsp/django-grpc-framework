.. _null_support:

Null Support
============

In proto3, all fields are never null.  However, we can use ``Oneof`` to define
a nullable type, for example:

.. code-block:: protobuf

    syntax = "proto3";

    package snippets;

    import "google/protobuf/struct.proto";

    service SnippetController {
        rpc Update(Snippet) returns (Snippet) {}
    }

    message NullableString {
        oneof kind {
            string value = 1;
            google.protobuf.NullValue null = 2;
        }
    }

    message Snippet {
        int32 id = 1;
        string title = 2;
        NullableString language = 3;
    }

The client example::

    import grpc
    import snippets_pb2
    import snippets_pb2_grpc
    from google.protobuf.struct_pb2 import NullValue


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = snippets_pb2_grpc.SnippetControllerStub(channel)
        request = snippets_pb2.Snippet(id=1, title='snippet title')
        # send non-null value
        # request.language.value = "python"
        # send null value
        request.language.null = NullValue.NULL_VALUE
        response = stub.Update(request)
        print(response, end='')

The service implementation::

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