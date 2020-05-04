"""
Run the ``python manage.py shell``, create two groups first::

    from django.contrib.auth.models import Group
    Group.objects.create(name='group1')
    Group.objects.create(name='group2')
"""
import grpc
from google.protobuf import empty_pb2
import demo_pb2_grpc
import demo_pb2


with grpc.insecure_channel('localhost:50051') as channel:
    stub = demo_pb2_grpc.UserControllerStub(channel)
    print('----- Create -----')
    request = demo_pb2.User(username='tom', email='tom@demo.com')
    request.groups.extend([1,2])
    response = stub.Create(request)
    print(response, end='')
    print('----- List -----')
    for user in stub.List(empty_pb2.Empty()):
        print(user, end='')
