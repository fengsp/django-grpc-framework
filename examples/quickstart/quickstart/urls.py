import demo_pb2_grpc
from demo.services import UserService


urlpatterns = []


def grpc_handlers(server):
    demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)
