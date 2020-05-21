.. _partial_update:

Handling Partial Update
=======================

In proto3:

1. All fields are optional
2. Singular primitive fields, repeated fields, and map fields are initialized
   with default values (0, empty list, etc).  There's no way of telling whether
   a field was explicitly set to the default value (for example whether a
   boolean was set to false) or just not set at all.

If we want to do a partial update on resources, we need to know whether a field
was set or not set at all.  There are different strategies that can be used to
represent ``unset``, we'll use a pattern called ``"Has Pattern"`` here.

Singular field absence
----------------------

In proto3, for singular field types, you can use the parent message's
``HasField()`` method to check if a message type field value has been set,
but you can't do it with non-message singular types.

For primitive types if you need ``HasField`` to you could use
``"google/protobuf/wrappers.proto"``.  Wrappers are useful for places where you
need to distinguish between the absence of a primitive typed field and its
default value:

.. code-block:: protobuf

    import "google/protobuf/wrappers.proto";

    service PersonController {
        rpc PartialUpdate(PersonPartialUpdateRequest) returns (Person) {}
    }

    message Person {
        int32 id = 1;
        string name = 2;
        string email = 3;
    }

    message PersonPartialUpdateRequest {
        int32 id = 1;
        google.protobuf.StringValue name = 2;
        google.protobuf.StringValue email = 3;
    }

Here is the client usage::

    from google.protobuf.wrappers_pb2 import StringValue


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hrm_pb2_grpc.PersonControllerStub(channel)
        request = hrm_pb2.PersonPartialUpdateRequest(id=1, name=StringValue(value="amy"))
        response = stub.PartialUpdate(request)
        print(response, end='')

The service implementation::

    class PersonService(generics.GenericService):
        queryset = Person.objects.all()
        serializer_class = PersonProtoSerializer

        def PartialUpdate(self, request, context):
            instance = self.get_object()
            serializer = self.get_serializer(instance, message=request, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.message

Or you can just use ``PartialUpdateModelMixin`` to get the same behavior::

    class PersonService(mixins.PartialUpdateModelMixin,
                        generics.GenericService):
        queryset = Person.objects.all()
        serializer_class = PersonProtoSerializer


Repeated and map field absence
------------------------------

If you need to check whether repeated fields and map fields are set or not,
you need to do it manually:

.. code-block:: protobuf

    message PersonPartialUpdateRequest {
        int32 id = 1;
        google.protobuf.StringValue name = 2;
        google.protobuf.StringValue email = 3;
        repeated int32 groups = 4;
        bool is_groups_set = 5;
    }