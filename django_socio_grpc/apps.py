import django.db.models.options as options
from django.apps import AppConfig

# Used to add options in class meta for customizing the proto file génération
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("grpc_messages", "grpc_methods")


class DjangoSocioGrpcConfig(AppConfig):
    name = "django_socio_grpc"
    verbose_name = "Django Socio gRPC"
