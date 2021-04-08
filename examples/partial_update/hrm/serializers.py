import hrm_pb2
from django_socio_grpc import proto_serializers
from hrm.models import Person


class PersonProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Person
        proto_class = hrm_pb2.Person
        fields = "__all__"
