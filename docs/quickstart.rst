.. _quickstart:

Quickstart
==========

We're going to create a simple service to allow clients to view and edit the
users in the system.


Project setup
-------------

Create a new Django project named ``quickstart``, then start a new app called
``demo``::

    # Create a virtual environment
    python3 -m venv env
    source env/bin/activate
    # Install Django and Django gRPC framework
    pip install django
    pip install djangorestframework
    pip install djangogrpcframework
    pip install grpcio
    pip install grpcio-tools
    # Create a new project and a new application
    django-admin startproject quickstart
    cd quickstart
    django-admin startapp demo

Now sync the database::

    python manage.py migrate


Settings
--------

Add ``django_grpc_framework`` to ``INSTALLED_APPS``, settings module is in
``quickstart/settings.py``::

    INSTALLED_APPS = [
        ...
        'django_grpc_framework',
    ]


Protos
------

Our first step is to define the gRPC service and messages, create a file
``quickstart/demo.proto`` next to ``quickstart/manage.py``::

    syntax = "proto3";

    package demo;

    import "google/protobuf/empty.proto";

    message User {
        int32 id = 1;
        string username = 2;
        string email = 3;
        repeated int32 groups = 4;
    }

    service UserController {
        rpc List(google.protobuf.Empty) returns (stream User) {}
        rpc Create(User) returns (User) {}
        rpc Retrieve(User) returns (User) {}
        rpc Update(User) returns (User) {}
        rpc Destroy(User) returns (google.protobuf.Empty) {}
    }

Next we need to generate gRPC code, from the ``quickstart`` directory, run::

    python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./demo.proto


Serializers
-----------

Then we're going to define a serializer, let's create a new module named
``demo/serializers.py``::

    from django.contrib.auth.models import User
    from rest_framework import serializers


    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'groups']


Services
--------

Now we'd write some a service, create ``demo/services.py``::

    from django.contrib.auth.models import User
    from django_grpc_framework import generics
    from demo.serializers import UserSerializer
    import demo_pb2


    class UserService(generics.ModelService):
        """
        gRPC service that allows users to be retrieved or updated.
        """
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = UserSerializer
        protobuf_class = demo_pb2.User


Handlers
--------

Ok, let's wire up the gRPC handlers, edit ``quickstart/urls.py``::

    import demo_pb2_grpc
    from demo.services import UserService


    urlpatterns = []


    def grpc_handlers(server):
        demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

We're done, the project layout should look like::

    .
    ./demo
    ./demo/migrations
    ./demo/migrations/__init__.py
    ./demo/services.py
    ./demo/models.py
    ./demo/serializers.py
    ./demo/__init__.py
    ./demo/apps.py
    ./demo/admin.py
    ./demo/tests.py
    ./demo/views.py
    ./demo.proto
    ./demo_pb2.py
    ./demo_pb2_grpc.py
    ./quickstart
    ./quickstart/asgi.py
    ./quickstart/__init__.py
    ./quickstart/settings.py
    ./quickstart/urls.py
    ./quickstart/wsgi.py
    ./manage.py


Testing our gRPC Service
------------------------

Fire up the server with development mode::

    python manage.py grpcrunserver --dev

We can now access our service from the gRPC client::

    import grpc
    from google.protobuf import empty_pb2
    import demo_pb2_grpc


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.UserControllerStub(channel)
        for user in stub.List(empty_pb2.Empty()):
            print(user, end='')