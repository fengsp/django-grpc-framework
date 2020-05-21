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
