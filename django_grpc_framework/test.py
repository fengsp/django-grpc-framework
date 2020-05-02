# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase
from grpc._server import _validate_generic_rpc_handlers


class TestChannel(object):
    def __init__(self, server):
        self.server = server

    def __enter__(self):
        return self

    def __exit__(self, exc_tp, exc_val, exc_tb):
        pass

    def unary_unary(self, method, request_serializer=None,
                    response_deserializer=None):
        return UnaryUnary(self, method)


class TestServer(object):
    def __init__(self):
        self.rpc_method_handlers = {}

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        _validate_generic_rpc_handlers(generic_rpc_handlers)
        self.rpc_method_handlers.update(generic_rpc_handlers[0]._method_handlers)

    def _find_method_handler(self, method_full_rpc_name):
        return self.rpc_method_handlers[method_full_rpc_name]


class UnaryUnary(object):
    def __init__(self, channel, method_full_rpc_name):
        self._channel = channel
        self._method_full_rpc_name = method_full_rpc_name

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        handler = self._channel.server._find_method_handler(self._method_full_rpc_name)
        context = TestContext()
        context._invocation_metadata.extend(metadata)
        return handler.unary_unary(request, context)


class TestContext(object):
    def __init__(self):
        self._invocation_metadata = []

    def abort(self, code, details):
        raise TestRpcError(code, details)

    def invocation_metadata(self):
        return self._invocation_metadata


class TestRpcError(Exception):
    def __init__(self, code, details):
        self.code = code
        self.details = details

    def __repr__(self):
        return '<TestRpcError code: %s, details: %s>' % (self.code, self.details)


class BaseRPCTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        server = TestServer()
        # add_services_to_server(server)
        cls.channel = TestChannel(server)
        super(BaseRPCTestCase, cls).setUpClass()
