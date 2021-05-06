from django_socio_grpc import generics, mixins
from fakeapp.models import UnitTestModel
from fakeapp.serializers import UnitTestModelSerializer


class UnitTestModelService(generics.ModelService, mixins.StreamModelMixin):
    queryset = UnitTestModel.objects.all().order_by("id")
    serializer_class = UnitTestModelSerializer
