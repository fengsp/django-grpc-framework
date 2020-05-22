from django_grpc_framework import proto_serializers
from hrm.models import Person
import hrm_pb2


class PersonProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Person
        proto_class = hrm_pb2.Person
        fields = '__all__'
