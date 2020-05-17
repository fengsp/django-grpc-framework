"""
Run the ``python manage.py shell``, create two groups first::

    from django.contrib.auth.models import Group
    Group.objects.create(name='group1')
    Group.objects.create(name='group2')
"""
import grpc
import account_pb2_grpc
import account_pb2


with grpc.insecure_channel('localhost:50051') as channel:
    stub = account_pb2_grpc.UserControllerStub(channel)
    print('----- Create -----')
    request = account_pb2.User(username='tom', email='tom@account.com')
    request.groups.extend([1,2])
    response = stub.Create(request)
    print(response, end='')
    print('----- List -----')
    for user in stub.List(account_pb2.UserListRequest()):
        print(user, end='')
