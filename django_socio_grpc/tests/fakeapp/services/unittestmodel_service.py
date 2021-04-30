from django_socio_grpc import generics
from fakeapp.models import UnitTestModel
from fakeapp.serializers import UnitTestModelSerializer


class UnitTestModelService(generics.ModelService):
    queryset = UnitTestModel.objects.all().order_by("id")
    serializer_class = UnitTestModelSerializer
