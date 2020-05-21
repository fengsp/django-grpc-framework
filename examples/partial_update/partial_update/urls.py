from django.contrib import admin
from django.urls import path
import hrm_pb2_grpc
from hrm.services import PersonService

urlpatterns = [
    path('admin/', admin.site.urls),
]


def grpc_handlers(server):
    hrm_pb2_grpc.add_PersonControllerServicer_to_server(PersonService.as_servicer(), server)