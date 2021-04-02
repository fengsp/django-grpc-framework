from django.test import TestCase
from .fake_grpc import FakeGRPC
from django_fake_model import models as f

from .filter_test.filter_test_pb2 import FilterTestListRequest, FilterTest
from .filter_test.filter_test_pb2_grpc import (
    add_FilterTestControllerServicer_to_server,
    FilterTestControllerStub,
)
from django.db import models
from django_socio_grpc import proto_serializers
from django_socio_grpc import generics


class SearchFilterModel(f.FakeModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)


class SearchFilterSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = SearchFilterModel
        proto_class = FilterTest
        fields = "__all__"


class SearchFilterService(generics.ModelService):
    queryset = SearchFilterModel.objects.all()
    serializer_class = SearchFilterSerializer


# class FakeFiltering:
#     def filter_queryset(self, request, queryset, view):
#         return ({"email": "john.doe@johndoe.com"}, {})


@SearchFilterModel.fake_me
class TestFiltering(TestCase):
    def setUp(self):
        for idx in range(10):
            title = "z" * (idx + 1)
            text = chr(idx + ord("a")) + chr(idx + ord("b")) + chr(idx + ord("c"))
            SearchFilterModel(title=title, text=text).save()
        self.fake_grpc = FakeGRPC(
            add_FilterTestControllerServicer_to_server, SearchFilterService.as_servicer()
        )

    def tearDown(self):
        self.fake_grpc.close()

    def test_sample(self):
        assert True

    def test_some(self):
        grpc_stub = self.fake_grpc.get_fake_stub(FilterTestControllerStub)
        request = FilterTestListRequest()
        responses = grpc_stub.List(request)

        responses_as_list = [response for response in responses]

        print(len(responses_as_list))

        self.assertEqual(len(responses_as_list), 10)
