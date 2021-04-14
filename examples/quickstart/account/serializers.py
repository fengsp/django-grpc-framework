from django.contrib.auth.models import User

import account_pb2
from django_socio_grpc import proto_serializers


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = account_pb2.User
        fields = ["id", "username", "email", "groups"]
