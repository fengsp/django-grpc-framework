.. _proto_serializers:

Proto Serializers
=================

The serializers work almost exactly the same with REST framework's ``Serializer``
class and ``ModelSerializer``, but use ``message`` instead of ``data`` as
input and output.


Declaring serializers
---------------------

Declaring a serializer looks very similar to declaring a rest framework
serializer::

    from rest_framework import serializers
    from django_grpc_framework import proto_serializers

    class PersonProtoSerializer(proto_serializers.ProtoSerializer):
        name = serializers.CharField(max_length=100)
        email = serializers.EmailField(max_length=100)

        class Meta:
            proto_class = hrm_pb2.Person


Overriding serialization and deserialization behavior
-----------------------------------------------------

A proto serializer is the same as one rest framework serializer, but we are
adding the following logic:

- Protobuf message -> Dict of python primitive datatypes.
- Protobuf message <- Dict of python primitive datatypes.

If you need to alter the convert behavior of a serializer class, you can do so
by overriding the ``.message_to_data()`` or ``.data_to_message`` methods.

Here is the default implementation::

    from google.protobuf.json_format import MessageToDict, ParseDict

    class ProtoSerializer(BaseProtoSerializer, Serializer):
        def message_to_data(self, message):
            """Protobuf message -> Dict of python primitive datatypes.
            """
            return MessageToDict(
                message, including_default_value_fields=True,
                preserving_proto_field_name=True
            )

        def data_to_message(self, data):
            """Protobuf message <- Dict of python primitive datatypes."""
            return ParseDict(
                data, self.Meta.proto_class(),
                ignore_unknown_fields=True
            )

The default behavior requires you to provide ``ProtoSerializer.Meta.proto_class``,
it is the protobuf class that should be used for create output proto message
object.  You must either set this attribute, or override the
``data_to_message()`` method. 


Serializing objects
-------------------

We can now use ``PersonProtoSerializer`` to serialize a person object::

    >>> serializer = PersonProtoSerializer(person)
    >>> serializer.message
    name: "amy"
    email: "amy@demo.com"
    >>> type(serializer.message)
    <class 'hrm_pb2.Person'>


Deserializing objects
---------------------

Deserialization is similar::

    >>> serializer = PersonProtoSerializer(message=message)
    >>> serializer.is_valid()
    True
    >>> serializer.validated_data
    OrderedDict([('name', 'amy'), ('email', 'amy@demo.com')])


ModelProtoSerializer
--------------------

This is the same as a rest framework ``ModelSerializer``::

    from django_grpc_framework import proto_serializers
    from hrm.models import Person
    import hrm_pb2


    class PersonProtoSerializer(proto_serializers.ModelProtoSerializer):
        class Meta:
            model = Person
            proto_class = hrm_pb2.Person
            fields = '__all__'