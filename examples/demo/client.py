import grpc
from google.protobuf import empty_pb2
import demo_pb2_grpc


with grpc.insecure_channel('localhost:50051') as channel:
    stub = demo_pb2_grpc.UserControllerStub(channel)
    for user in stub.List(empty_pb2.Empty()):
        print(user, end='')
