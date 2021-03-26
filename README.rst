Socotec.io Django gRPC Framework
================================

Django gRPC framework is a toolkit for building gRPC services, inspired by  django-grpc-framework.


Requirements
------------

- Python (3.6, 3.7, 3.8)
- Django (2.2, 3.0), Django REST Framework (3.10.x, 3.11.x)
- gRPC, gRPC tools, proto3


Quick start
-----------

1. Add ``django_socio_grpc`` to ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_socio_grpc',
    ]


Demo
----

Generate ``.proto`` file demo.proto_:


.. code-block:: bash

    python manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email --file demo.proto

Generate gRPC code:

.. code-block:: bash

    python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./demo.proto

Now edit the ``demo/urls.py`` module:

.. code-block:: python

import account_pb2_grpc
from account.services import UserService

urlpatterns = []

def grpc_handlers(server):
    demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)


Now edit the ``demo/serializers.py`` module:

.. code-block:: python

    from django.contrib.auth.models import User
    from django_grpc_framework import generics, proto_serializers
    import demo_pb2
    import demo_pb2_grpc

    class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
        class Meta:
            model = User
            proto_class = demo_pb2.User
            fields = ['id', 'username', 'email']


Then edit the ``demo/services.py`` module:

.. code-block:: python

    class UserService(generics.ModelService):
        queryset = User.objects.all()
        serializer_class = UserProtoSerializer


That's it, we're done!

.. code-block:: bash
    
    $ python manage.py grpcrunserver --dev

You can now run a gRPC client to access the service:

.. code-block:: python

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.UserControllerStub(channel)
        for user in stub.List(demo_pb2.UserListRequest()):
            print(user, end='')
