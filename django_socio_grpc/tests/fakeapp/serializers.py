from .models import UnitTestModel
from django_socio_grpc.tests.grpc_test_utils.unittest_pb2 import UnitTest

from django_socio_grpc import proto_serializers

class UnitTestSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = UnitTestModel
        proto_class = UnitTest
        fields = "__all__"