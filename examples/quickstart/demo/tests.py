from django_grpc_framework.test import RPCTestCase
from django.contrib.auth.models import User
import demo_pb2
import demo_pb2_grpc


class UserServiceTest(RPCTestCase):
    def test_create_user(self):
        stub = demo_pb2_grpc.UserControllerStub(self.channel)
        response = stub.Create(demo_pb2.User(username='tom', email='tom@demo.com'))
        self.assertEqual(response.username, 'tom')
        self.assertEqual(response.email, 'tom@demo.com')
        self.assertEqual(User.objects.count(), 1)
