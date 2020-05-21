.. _using_generics:

Using Generic Services
======================

We provide a number of pre-built services as a shortcut for common usage
patterns.  The generic services allow you to quickly build services that
map closely to database models.


Using mixins
------------

The create/list/retrieve/update/destroy operations that we've been using
so far are going to be similar for any model-backend services.  Those
operations are implemented in gRPC framework's mixin classes.

Let's take a look at how we can compose the services by using the mixin
classes, here is our ``blog/services`` file again::

    from blog.models import Post
    from blog.serializers import PostProtoSerializer
    from django_grpc_framework import mixins
    from django_grpc_framework import generics


    class PostService(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericService):
        queryset = Post.objects.all()
        serializer_class = PostProtoSerializer

We are building our service with ``GenericService``, and adding in
``ListModelMixin``,``CreateModelMixin``, etc.  The base class provides the
core functionality, and the mixin classes provice the ``.List()`` and
``.Create()`` handlers.


Using model service
-------------------

If you want all operations of create/list/retrieve/update/destroy, we provide
one already mixed-in generic services::

    class PostService(generics.ModelService):
        queryset = Post.objects.all()
        serializer_class = PostProtoSerializer