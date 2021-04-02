from django.test import TestCase
import pytest

from .echo.echo_pb2 import EchoRequest


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from .echo.echo_pb2_grpc import add_EchoServiceServicer_to_server

    return add_EchoServiceServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    from .echo.servicer import Servicer

    return Servicer()


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from .echo.echo_pb2_grpc import EchoServiceStub

    return EchoServiceStub


def test_some(grpc_stub):
  request = EchoRequest()
  response = grpc_stub.handler(request)

  assert response.name == f'test-{request.name}'


# class FakeFiltering:
#     def filter_queryset(self, request, queryset, view):
#         return ({"email": "john.doe@johndoe.com"}, {})


# class TestFiltering(TestCase):
#     def test_sample(self):
#         assert True

#     def test_some(self):
#       request = EchoRequest()
#       response = grpc_stub.handler(request)

#       assert response.name == f'test-{request.name}'
