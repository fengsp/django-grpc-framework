from django.contrib.auth.models import User
from django_grpc_framework import generics
from demo.serializers import UserSerializer
import demo_pb2


class UserService(generics.ModelService):
    """
    gRPC service that allows users to be retrieved or updated.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    protobuf_class = demo_pb2.User
