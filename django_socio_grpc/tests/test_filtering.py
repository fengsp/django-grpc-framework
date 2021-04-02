from django.test import TestCase
import pytest
from .fake_grpc import FakeGRPC

from .echo.echo_pb2 import EchoRequest
from .echo.echo_pb2_grpc import add_EchoServiceServicer_to_server, EchoServiceStub
from .echo.servicer import Servicer


# @pytest.fixture(scope='module')
# def grpc_add_to_server():

#     return add_EchoServiceServicer_to_server


# @pytest.fixture(scope='module')
# def grpc_servicer():

#     return Servicer()


# @pytest.fixture(scope='module')
# def grpc_stub_cls(grpc_channel):

#     return EchoServiceStub


# class FakeFiltering:
#     def filter_queryset(self, request, queryset, view):
#         return ({"email": "john.doe@johndoe.com"}, {})

class TestFiltering(TestCase):
  def setUp(self):
    self.fake_grpc = FakeGRPC(add_EchoServiceServicer_to_server, Servicer())

  def tearDown(self):
    self.fake_grpc.close()

  def test_sample(self):
    assert True

  def test_some(self):
    grpc_stub = self.fake_grpc.get_fake_stub(EchoServiceStub)
    request = EchoRequest()
    response = grpc_stub.handler(request)

    assert response.name == f'test-{request.name}'
