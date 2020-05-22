.. _building_services:

Building Services
=================

This tutorial will create a simple blog gRPC Service.


Environment setup
-----------------

Create a new virtual environment for our project::

    python3 -m venv env
    source env/bin/activate

Install our packages::

    pip install django
    pip install djangorestframework   # we need the serialization
    pip install djangogrpcframework
    pip install grpcio
    pip install grpcio-tools


Project setup
-------------

Let's create a new project to work with::

    django-admin startproject tutorial
    cd tutorial

Now we can create an app that we'll use to create a simple gRPC Service::

    python manage.py startapp blog

We'll need to add our new ``blog`` app and the ``django_grpc_framework`` app to
``INSTALLED_APPS``.  Let's edit the ``tutorial/settings.py`` file::

    INSTALLED_APPS = [
        ...
        'django_grpc_framework',
        'blog',
    ]


Create a model
--------------

Now we're going to create a simple ``Post`` model that is used to store blog
posts.  Edit the ``blog/models.py`` file::

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()
        created = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ['created']

We also need to create a migration for our post model, and sync the database::

    python manage.py makemigrations blog
    python manage.py migrate


Defining a service
------------------

Our first step is to define the gRPC service and messages, create a directory
``tutorial/protos`` that sits next to ``tutorial/manage.py``, create another
directory ``protos/blog_proto`` and create the ``protos/blog_proto/post.proto``
file:

.. code-block:: protobuf

    syntax = "proto3";

    package blog_proto;

    import "google/protobuf/empty.proto";

    service PostController {
        rpc List(PostListRequest) returns (stream Post) {}
        rpc Create(Post) returns (Post) {}
        rpc Retrieve(PostRetrieveRequest) returns (Post) {}
        rpc Update(Post) returns (Post) {}
        rpc Destroy(Post) returns (google.protobuf.Empty) {}
    }

    message Post {
        int32 id = 1;
        string title = 2;
        string content = 3;
    }

    message PostListRequest {
    }

    message PostRetrieveRequest {
        int32 id = 1;
    }

For a model-backed service, you could also just run the model proto generator::

    python manage.py generateproto --model blog.models.Post --fields=id,title,content --file protos/blog_proto/post.proto

Then edit it as needed, here the package name can't be automatically inferred
by the proto generator, change ``package post`` to ``package blog_proto``.

Next we need to generate gRPC code, from the ``tutorial`` directory, run::

    python -m grpc_tools.protoc --proto_path=./protos --python_out=./ --grpc_python_out=./ ./protos/blog_proto/post.proto


Create a Serializer class
-------------------------

Before we implement our gRPC service, we need to provide a way of serializing
and deserializing the post instances into protocol buffer messages.  We can
do this by declaring serializers, create a file in the ``blog`` directory
named ``serializers.py`` and add the following::

    from django_grpc_framework import proto_serializerss
    from blog.models import Post
    from blog_proto import post_pb2


    class PostProtoSerializer(proto_serializers.ModelProtoSerializer):
        class Meta:
            model = Post
            proto_class = post_pb2.Post
            fields = ['id', 'title', 'content']


Write a service
---------------

With our serializer class, we'll write a regular grpc service, create a file
in the ``blog`` directory named ``services.py`` and add the following::

    import grpc
    from google.protobuf import empty_pb2
    from django_grpc_framework.services import Service
    from blog.models import Post
    from blog.serializers import PostProtoSerializer


    class PostService(Service):
        def List(self, request, context):
            posts = Post.objects.all()
            serializer = PostProtoSerializer(posts, many=True)
            for msg in serializer.message:
                yield msg

        def Create(self, request, context):
            serializer = PostProtoSerializer(message=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.message

        def get_object(self, pk):
            try:
                return Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                self.context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

        def Retrieve(self, request, context):
            post = self.get_object(request.id)
            serializer = PostProtoSerializer(post)
            return serializer.message

        def Update(self, request, context):
            post = self.get_object(request.id)
            serializer = PostProtoSerializer(post, message=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.message

        def Destroy(self, request, context):
            post = self.get_object(request.id)
            post.delete()
            return empty_pb2.Empty()

Finally we need to wire there services up, create ``blog/handlers.py`` file::

    from blog._services import PostService
    from blog_proto import post_pb2_grpc


    def grpc_handlers(server):
        post_pb2_grpc.add_PostControllerServicer_to_server(PostService.as_servicer(), server)

Also we need to wire up the root handlers conf, in ``tutorial/urls.py``
file, include our blog app's grpc handlers::

    from blog.handlers import grpc_handlers as blog_grpc_handlers


    urlpatterns = []


    def grpc_handlers(server):
        blog_grpc_handlers(server)


Calling our service
-------------------

Now we can start up a gRPC server so that clients can actually use our
service::

    python manage.py grpcrunserver --dev

In another terminal window, we can test the server::

    import grpc
    from blog_proto import post_pb2, post_pb2_grpc


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = post_pb2_grpc.PostControllerStub(channel)
        print('----- Create -----')
        response = stub.Create(post_pb2.Post(title='t1', content='c1'))
        print(response, end='')
        print('----- List -----')
        for post in stub.List(post_pb2.PostListRequest()):
            print(post, end='')
        print('----- Retrieve -----')
        response = stub.Retrieve(post_pb2.PostRetrieveRequest(id=response.id))
        print(response, end='')
        print('----- Update -----')
        response = stub.Update(post_pb2.Post(id=response.id, title='t2', content='c2'))
        print(response, end='')
        print('----- Delete -----')
        stub.Destroy(post_pb2.Post(id=response.id))
