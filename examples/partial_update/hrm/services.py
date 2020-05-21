from django_grpc_framework import generics, mixins
from hrm.serializers import PersonProtoSerializer
from hrm.models import Person


"""
class PersonService(generics.GenericService):
    queryset = Person.objects.all()
    serializer_class = PersonProtoSerializer

    def PartialUpdate(self, request, context):
        instance = self.get_object()
        serializer = self.get_serializer(instance, message=request, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message
"""


class PersonService(mixins.PartialUpdateModelMixin,
                    generics.GenericService):
    queryset = Person.objects.all()
    serializer_class = PersonProtoSerializer
