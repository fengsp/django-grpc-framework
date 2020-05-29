Django gRPC Framework
=====================

.. image:: https://img.shields.io/pypi/v/djangogrpcframework.svg
   :target: https://img.shields.io/pypi/v/djangogrpcframework.svg

.. image:: https://readthedocs.org/projects/djangogrpcframework/badge/?version=latest
   :target: https://readthedocs.org/projects/djangogrpcframework/badge/?version=latest

.. image:: https://travis-ci.org/fengsp/django-grpc-framework.svg?branch=master
   :target: https://travis-ci.org/fengsp/django-grpc-framework.svg?branch=master

.. image:: https://img.shields.io/pypi/pyversions/djangogrpcframework
   :target: https://img.shields.io/pypi/pyversions/djangogrpcframework

.. image:: https://img.shields.io/pypi/l/djangogrpcframework
   :target: https://img.shields.io/pypi/l/djangogrpcframework

Django gRPC framework is a toolkit for building gRPC services, inspired by
djangorestframework.


Requirements
------------

- Python (3.6, 3.7, 3.8)
- Django (2.2, 3.0), Django REST Framework (3.10.x, 3.11.x)
- gRPC, gRPC tools, proto3


Installation
------------

.. code-block:: bash
    
    $ pip install djangogrpcframework

Add ``django_grpc_framework`` to ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_grpc_framework',
    ]


Demo
----

Here is a quick example of using gRPC framework to build a simple
model-backed service for accessing users, startup a new project:

.. code-block:: bash
    
    $ django-admin startproject demo
    $ python manage.py migrate

Generate ``.proto`` file demo.proto_:

.. _demo.proto: https://github.com/fengsp/django-grpc-framework/blob/master/examples/demo/demo.proto

.. code-block:: bash

    python manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email --file demo.proto

Generate gRPC code:

.. code-block:: bash

    python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./demo.proto

Now edit the ``demo/urls.py`` module:

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


    class UserService(generics.ModelService):
        queryset = User.objects.all()
        serializer_class = UserProtoSerializer


    urlpatterns = []
    def grpc_handlers(server):
        demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

That's it, we're done!

.. code-block:: bash
    
    $ python manage.py grpcrunserver --dev

You can now run a gRPC client to access the service:

.. code-block:: python

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.UserControllerStub(channel)
        for user in stub.List(demo_pb2.UserListRequest()):
            print(user, end='')
