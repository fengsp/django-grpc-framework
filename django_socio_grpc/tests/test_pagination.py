from django.test import TestCase
from .grpc_test_utils.fake_grpc import FakeGRPC

from .grpc_test_utils.unittest_pb2 import UnitTestListRequest, UnitTest
from .grpc_test_utils.unittest_pb2_grpc import (
    add_UnitTestControllerServicer_to_server,
    UnitTestControllerStub,
)
from django_socio_grpc import generics
import json
from rest_framework.pagination import PageNumberPagination
from .grpc_test_utils.django_classes_for_tests import UnitTestModel, UnitTestSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100

class UnitTestService(generics.ModelService):
    queryset = UnitTestModel.objects.all()
    serializer_class = UnitTestSerializer
    pagination_class = StandardResultsSetPagination


@UnitTestModel.fake_me
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

    def test_sample(self):
        assert True

    def test_page_number_pagination(self):
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestControllerStub)
        request = UnitTestListRequest()
        responses = grpc_stub.List(request=request)

        responses_as_list = [response for response in responses]

        print(responses_as_list)

        self.assertEqual(len(responses_as_list), 3)

    # def test_page_number_pagination(self):
    #     grpc_stub = self.fake_grpc.get_fake_stub(FilterUnitTestControllerStub)
    #     request = FilterUnitTestListRequest()
    #     pagination_as_dict = {"title": "zzzzzzz"}
    #     metadata = (("PAGINATION", (json.dumps(pagination_as_dict))),)
    #     responses = grpc_stub.List(request=request, metadata=metadata)

    #     responses_as_list = [response for response in responses]

    #     self.assertEqual(len(responses_as_list), 1)
    #     # responses_as_list[0] is type of django_socio_grpc.tests.filter_test.filter_unittest_pb2.FilterTest
    #     self.assertEqual(responses_as_list[0].id, 7)
