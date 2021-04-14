from django.contrib.auth.models import User

from account.serializers import UserProtoSerializer
from django_socio_grpc import generics


class UserService(generics.ModelService):
    """
    gRPC service that allows users to be retrieved or updated.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserProtoSerializer
