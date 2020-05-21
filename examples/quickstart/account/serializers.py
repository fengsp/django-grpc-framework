from django.contrib.auth.models import User
from django_grpc_framework import serializers
import account_pb2


class UserProtoSerializer(serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = account_pb2.User
        fields = ['id', 'username', 'email', 'groups']
