from django.contrib.auth.models import User
from django_grpc_framework import generics, proto_serializers
import demo_pb2
import demo_pb2_grpc


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = demo_pb2.User
        fields = ['id', 'username', 'email']


class UserService(generics.ModelService):
    queryset = User.objects.all()
    serializer_class = UserProtoSerializer


urlpatterns = []


def grpc_handlers(server):
    demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)