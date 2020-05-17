from django_grpc_framework import generics, mixins
from hrm.serializers import PersonSerializer
from hrm.models import Person
import hrm_pb2
from google.protobuf.json_format import MessageToDict, ParseDict


"""
class PersonService(generics.GenericService):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    protobuf_class = hrm_pb2.Person

    def PartialUpdate(self, request, context):
        instance = self.get_object()
        data = MessageToDict(request, including_default_value_fields=True)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        protobuf_class = self.get_protobuf_class()
        return ParseDict(serializer.data, protobuf_class())
"""


class PersonService(mixins.PartialUpdateModelMixin,
                    generics.GenericService):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    protobuf_class = hrm_pb2.Person
