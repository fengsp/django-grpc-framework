from django.contrib.auth.models import User
from rest_framework import serializers
from django_grpc_framework import generics
import demo_pb2
import demo_pb2_grpc


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserService(generics.ModelService):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    protobuf_class = demo_pb2.User


urlpatterns = []


def grpc_handlers(server):
    demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)
