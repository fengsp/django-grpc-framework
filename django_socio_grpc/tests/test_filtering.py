import json

from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend

from django_socio_grpc import generics
from fakeapp.models import UnitTestModel
from fakeapp.serializers import UnitTestSerializer

from .grpc_test_utils.fake_grpc import FakeGRPC
from .grpc_test_utils.unittest_pb2 import UnitTestListRequest
from .grpc_test_utils.unittest_pb2_grpc import (
    UnitTestControllerStub,
    add_UnitTestControllerServicer_to_server,
)


class UnitTestService(generics.ModelService):
    queryset = UnitTestModel.objects.all()
    serializer_class = UnitTestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "text"]


class TestFiltering(TestCase):
    def setUp(self):
        for idx in range(10):
            title = "z" * (idx + 1)
            text = chr(idx + ord("a")) + chr(idx + ord("b")) + chr(idx + ord("c"))
            UnitTestModel(title=title, text=text).save()
        self.fake_grpc = FakeGRPC(
            add_UnitTestControllerServicer_to_server, UnitTestService.as_servicer()
        )

    def tearDown(self):
        self.fake_grpc.close()

    def test_django_filter(self):
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestControllerStub)
        request = UnitTestListRequest()
        filter_as_dict = {"title": "zzzzzzz"}
        metadata = (("FILTERS", (json.dumps(filter_as_dict))),)
        responses = grpc_stub.List(request=request, metadata=metadata)

        responses_as_list = [response for response in responses]

        self.assertEqual(len(responses_as_list), 1)
        # responses_as_list[0] is type of django_socio_grpc.tests.grpc_test_utils.unittest_pb2.Test
        self.assertEqual(responses_as_list[0].id, 7)
