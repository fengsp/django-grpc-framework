import grpc
import demo_pb2_grpc
import demo_pb2


with grpc.insecure_channel('localhost:50051') as channel:
    stub = demo_pb2_grpc.UserControllerStub(channel)
    for user in stub.List(demo_pb2.UserListRequest()):
        print(user, end='')
