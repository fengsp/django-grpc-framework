"""
# this file is inspirated by pytest-grpc to be able to use django TestCase
# https://github.com/kataev/pytest-grpc/blob/master/pytest_grpc/plugin.py
"""
import socket
from concurrent import futures

import grpc
from grpc._cython.cygrpc import _Metadatum


class FakeServer(object):
    def __init__(self, pool):
        self.handlers = {}
        self.pool = pool

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        from grpc._server import _validate_generic_rpc_handlers

        _validate_generic_rpc_handlers(generic_rpc_handlers)

        self.handlers.update(generic_rpc_handlers[0]._method_handlers)

    def start(self):
        pass

    def stop(self, grace=None):
        pass

    def add_secure_port(self, target, server_credentials):
        pass

    def add_insecure_port(self, target):
        pass


class FakeRpcError(RuntimeError, grpc.RpcError):
    def __init__(self, code, details):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details


class FakeContext(object):
    def __init__(self):
        self._invocation_metadata = []

    def abort(self, code, details):
        raise FakeRpcError(code, details)

    def invocation_metadata(self):
        return self._invocation_metadata


class FakeChannel:
    def __init__(self, fake_server):
        self.server = fake_server

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fake_method(self, method_name, uri, *args, **kwargs):
        handler = self.server.handlers[uri]
        real_method = getattr(handler, method_name)

        def fake_handler(request, metadata=None):
            context = FakeContext()
            if metadata:
                context._invocation_metadata.extend((_Metadatum(k, v) for k, v in metadata))

            # future = self.server.pool.submit(real_method, request, context)
            # return future.result()
            return real_method(request, context)

        return fake_handler

    def unary_unary(self, *args, **kwargs):
        return self.fake_method("unary_unary", *args, **kwargs)

    def unary_stream(self, *args, **kwargs):
        return self.fake_method("unary_stream", *args, **kwargs)

    def stream_unary(self, *args, **kwargs):
        return self.fake_method("stream_unary", *args, **kwargs)

    def stream_stream(self, *args, **kwargs):
        return self.fake_method("stream_stream", *args, **kwargs)


class FakeGRPC:
    def __init__(self, grpc_add_to_server, grpc_servicer):
        self.grpc_addr = self.get_grpc_addr()

        self.grpc_server = self.get_fake_server()

        grpc_add_to_server(grpc_servicer, self.grpc_server)
        self.grpc_server.add_insecure_port(self.grpc_addr)
        self.grpc_server.start()

        self.grpc_channel = self.get_fake_channel()

    def close(self):
        self.grpc_server.stop(grace=None)

    def get_fake_server(self):
        pool = futures.ThreadPoolExecutor(max_workers=1)
        grpc_server = FakeServer(pool)
        return grpc_server

    def get_fake_channel(self):
        return FakeChannel(self.grpc_server)

    def get_grpc_addr(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 0))
        return f"localhost:{sock.getsockname()[1]}"

    def get_fake_stub(self, grpc_stub_cls):
        return grpc_stub_cls(self.grpc_channel)
