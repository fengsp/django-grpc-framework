from django.db import models
from django_fake_model import models as f

from django_socio_grpc import proto_serializers

from .unittest_pb2 import UnitTest


class UnitTestModel(f.FakeModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)


class UnitTestSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = UnitTestModel
        proto_class = UnitTest
        fields = "__all__"
