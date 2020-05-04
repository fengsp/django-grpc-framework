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


Installation
------------

.. code-block:: bash
    
    $ pip install djangogrpcframework

Add ``django_grpc_framework`` to ``INSTALLED_APPS`` setting::

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

Now define protos in ``demo.proto``::

    syntax = "proto3";

    package demo;

    import "google/protobuf/empty.proto";

    message User { 
        int32 id = 1;
        string username = 2;
        string email = 3;
    }   

    service UserController {
        rpc List(google.protobuf.Empty) returns (stream User) {}
        rpc Create(User) returns (User) {}
        rpc Retrieve(User) returns (User) {}
        rpc Update(User) returns (User) {}
        rpc Destroy(User) returns (google.protobuf.Empty) {}
    }

Generate gRPC code::

    python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./demo.proto

Now edit the ``demo/urls.py`` module:

.. code-block:: python

    from django.contrib.auth.models import User
    from rest_framework import serializers
    from django_grpc_framework import generics
    import demo_pb2
    import demo_pb2_grpc


    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email']


    class UserService(generics.ModelService):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        protobuf_class = demo_pb2.User


    urlpatterns = []
    def grpc_handlers(server):
        demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

That's it, we're done!

.. code-block:: bash
    
    $ python manage.py grpcrunserver --dev

You can now run a gRPC client to access the service:

.. code-block:: python

    from google.protobuf import empty_pb2

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.UserControllerStub(channel)
        for user in stub.List(empty_pb2.Empty()):
            print(user, end='')
