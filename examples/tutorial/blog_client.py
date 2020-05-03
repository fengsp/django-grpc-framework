import grpc
from google.protobuf import empty_pb2
from blog_proto import post_pb2, post_pb2_grpc


with grpc.insecure_channel('localhost:50051') as channel:
    stub = post_pb2_grpc.PostControllerStub(channel)
    print('----- Create -----')
    response = stub.Create(post_pb2.Post(title='t1', content='c1'))
    print(response, end='')
    print('----- List -----')
    for post in stub.List(empty_pb2.Empty()):
        print(post, end='')
    print('----- Retrieve -----')
    response = stub.Retrieve(post_pb2.Post(id=response.id))
    print(response, end='')
    print('----- Update -----')
    response = stub.Update(post_pb2.Post(id=response.id, title='t2', content='c2'))
    print(response, end='')
    print('----- Delete -----')
    stub.Destroy(post_pb2.Post(id=response.id))
