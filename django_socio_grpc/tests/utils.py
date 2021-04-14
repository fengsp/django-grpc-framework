import grpc
from django.test import testcases

from django_socio_grpc.settings import grpc_settings


class Channel:
    def __init__(self):
        server = FakeServer()
        grpc_settings.ROOT_HANDLERS_HOOK(server)
        self.server = server

    def __enter__(self):
        return self

    def __exit__(self, exc_tp, exc_val, exc_tb):
        pass

    def unary_unary(self, method, *args, **kwargs):
        return UnaryUnary(self, method)

    def unary_stream(self, method, *args, **kwargs):
        return UnaryStream(self, method)

    def stream_unary(self, method, *args, **kwargs):
        return StreamUnary(self, method)

    def stream_stream(self, method, *args, **kwargs):
        return StreamStream(self, method)


class _MultiCallable:
    def __init__(self, channel, method_full_rpc_name):
        self._handler = channel.server._find_method_handler(method_full_rpc_name)

    def with_call(self, *args, **kwargs):
        raise NotImplementedError

    def future(self, *args, **kwargs):
        raise NotImplementedError


class UnaryUnary(_MultiCallable, grpc.UnaryUnaryMultiCallable):
    def __call__(self, request, timeout=None, metadata=None, *args, **kwargs):
        context = FakeContext()
        context._invocation_metadata.extend(metadata or [])
        return self._handler.unary_unary(request, context)


class UnaryStream(_MultiCallable, grpc.UnaryStreamMultiCallable):
    def __call__(self, request, timeout=None, metadata=None, *args, **kwargs):
        context = FakeContext()
        context._invocation_metadata.extend(metadata or [])
        return self._handler.unary_stream(request, context)


class StreamUnary(_MultiCallable, grpc.StreamUnaryMultiCallable):
    def __call__(self, request_iterator, timeout=None, metadata=None, *args, **kwargs):
        context = FakeContext()
        context._invocation_metadata.extend(metadata or [])
        return self._handler.stream_unary(request_iterator, context)


class StreamStream(_MultiCallable, grpc.StreamStreamMultiCallable):
    def __call__(self, request_iterator, timeout=None, metadata=None, *args, **kwargs):
        context = FakeContext()
        context._invocation_metadata.extend(metadata or [])
        return self._handler.stream_stream(request_iterator, context)


class FakeRpcError(grpc.RpcError):
    def __init__(self, code, details):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details

    def __repr__(self):
        return "<FakeRpcError code: %s, details: %s>" % (self._code, self._details)


class FakeServer:
    def __init__(self):
        self.rpc_method_handlers = {}

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        from grpc._server import _validate_generic_rpc_handlers

        _validate_generic_rpc_handlers(generic_rpc_handlers)
        self.rpc_method_handlers.update(generic_rpc_handlers[0]._method_handlers)

    def _find_method_handler(self, method_full_rpc_name):
        return self.rpc_method_handlers[method_full_rpc_name]


class FakeContext:
    def __init__(self):
        self._invocation_metadata = []

    def abort(self, code, details):
        raise FakeRpcError(code, details)

    def invocation_metadata(self):
        return self._invocation_metadata


class RPCSimpleTestCase(testcases.SimpleTestCase):
    channel_class = Channel

    def setUp(self):
        super().setUp()
        self.channel = self.channel_class()


class RPCTransactionTestCase(testcases.TransactionTestCase):
    channel_class = Channel

    def setUp(self):
        super().setUp()
        self.channel = self.channel_class()


class RPCTestCase(testcases.TestCase):
    channel_class = Channel

    def setUp(self):
        super().setUp()
        self.channel = self.channel_class()
