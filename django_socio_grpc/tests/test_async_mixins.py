import os
import unittest

import pytest
from asgiref.sync import sync_to_async
from django.test import TestCase

from django_socio_grpc import generics
from fakeapp.grpc.fakeapp_pb2 import UnitTestModelListRequest
from fakeapp.grpc.fakeapp_pb2_grpc import (
    UnitTestModelControllerStub,
    add_UnitTestModelControllerServicer_to_server,
)
from fakeapp.models import UnitTestModel
from fakeapp.serializers import UnitTestModelSerializer

from .grpc_test_utils.fake_grpc import FakeGRPC


class UnitTestService(generics.ModelService):
    queryset = UnitTestModel.objects.all()
    serializer_class = UnitTestModelSerializer


class TestAsyncMixins(unittest.IsolatedAsyncioTestCase, TestCase):
    async def asyncSetUp(self):
        os.environ["GRPC_ASYNC"] = "True"
        self.fake_grpc = FakeGRPC(
            add_UnitTestModelControllerServicer_to_server, UnitTestService.as_servicer()
        )

    def tearDown(self):
        self.fake_grpc.close()

    @sync_to_async
    def create_instances(self):
        for idx in range(10):
            title = "z" * (idx + 1)
            text = chr(idx + ord("a")) + chr(idx + ord("b")) + chr(idx + ord("c"))
            UnitTestModel(title=title, text=text).save()

    @pytest.mark.django_db
    async def test_async_list(self):
        await self.create_instances()
        grpc_stub = self.fake_grpc.get_fake_stub(UnitTestModelControllerStub)
        request = UnitTestModelListRequest()
        response = await grpc_stub.List(request=request)

        self.assertEqual(len(response.results), 10)
