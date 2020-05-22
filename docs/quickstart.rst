.. _quickstart:

Quickstart
==========

We're going to create a simple service to allow clients to retrieve and edit the
users in the system.


Project setup
-------------

Create a new Django project named ``quickstart``, then start a new app called
``account``::

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
    django-admin startapp account

Now sync the database::

    python manage.py migrate


Update settings
---------------

Add ``django_grpc_framework`` to ``INSTALLED_APPS``, settings module is in
``quickstart/settings.py``::

    INSTALLED_APPS = [
        ...
        'django_grpc_framework',
    ]


Defining protos
---------------

Our first step is to define the gRPC service and messages, create a file
``quickstart/account.proto`` next to ``quickstart/manage.py``:

.. code-block:: protobuf

    syntax = "proto3";

    package account;

    import "google/protobuf/empty.proto";

    service UserController {
        rpc List(UserListRequest) returns (stream User) {}
        rpc Create(User) returns (User) {}
        rpc Retrieve(UserRetrieveRequest) returns (User) {}
        rpc Update(User) returns (User) {}
        rpc Destroy(User) returns (google.protobuf.Empty) {}
    }

    message User {
        int32 id = 1;
        string username = 2;
        string email = 3;
        repeated int32 groups = 4;
    }

    message UserListRequest {
    }

    message UserRetrieveRequest {
        int32 id = 1;
    }

Or you can generate it automatically based on ``User`` model::

    python manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email,groups --file account.proto

Next we need to generate gRPC code, from the ``quickstart`` directory, run::

    python -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./account.proto


Writing serializers
-------------------

Then we're going to define a serializer, let's create a new module named
``account/serializers.py``::

    from django.contrib.auth.models import User
    from django_grpc_framework import proto_serializers
    import account_pb2


    class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
        class Meta:
            model = User
            proto_class = account_pb2.User
            fields = ['id', 'username', 'email', 'groups']


Writing services
----------------

Now we'd write some a service, create ``account/services.py``::

    from django.contrib.auth.models import User
    from django_grpc_framework import generics
    from account.serializers import UserProtoSerializer


    class UserService(generics.ModelService):
        """
        gRPC service that allows users to be retrieved or updated.
        """
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = UserProtoSerializer


Register handlers
-----------------

Ok, let's wire up the gRPC handlers, edit ``quickstart/urls.py``::

    import account_pb2_grpc
    from account.services import UserService


    urlpatterns = []


    def grpc_handlers(server):
        account_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

We're done, the project layout should look like::

    .
    ./quickstart
    ./quickstart/asgi.py
    ./quickstart/__init__.py
    ./quickstart/settings.py
    ./quickstart/urls.py
    ./quickstart/wsgi.py
    ./manage.py
    ./account
    ./account/migrations
    ./account/migrations/__init__.py
    ./account/services.py
    ./account/models.py
    ./account/serializers.py
    ./account/__init__.py
    ./account/apps.py
    ./account/admin.py
    ./account/tests.py
    ./account.proto
    ./account_pb2_grpc.py
    ./account_pb2.py


Calling our service
-------------------

Fire up the server with development mode::

    python manage.py grpcrunserver --dev

We can now access our service from the gRPC client::

    import grpc
    import account_pb2
    import account_pb2_grpc


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = account_pb2_grpc.UserControllerStub(channel)
        for user in stub.List(account_pb2.UserListRequest()):
            print(user, end='')
