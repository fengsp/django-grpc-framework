from django_socio_grpc import proto_serializers
from django_socio_grpc.tests.grpc_test_utils.unittest_pb2 import UnitTest

from .models import UnitTestModel


class UnitTestSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = UnitTestModel
        proto_class = UnitTest
        fields = "__all__"
