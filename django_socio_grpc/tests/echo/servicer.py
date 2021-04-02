from .echo_pb2 import EchoRequest, EchoResponse
from .echo_pb2_grpc import EchoServiceServicer


class Servicer(EchoServiceServicer):
    def handler(self, request: EchoRequest, context) -> EchoResponse:
        return EchoResponse(name=f'test-{request.name}')

    def error_handler(self, request: EchoRequest, context) -> EchoResponse:
        raise RuntimeError('Some error')