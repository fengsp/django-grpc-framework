import account_pb2_grpc
from account.services import UserService


urlpatterns = []


def grpc_handlers(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)
