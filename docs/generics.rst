.. _generics:

Generic services
================

The generic services provided by gRPC framework allow you to quickly build
gRPC services that map closely to your database models.  If the generic services
don't suit your needs, use the regular ``Service`` class, or reuse the mixins
and base classes used by the generic services to compose your own set of
ressable generic services.

For example::

   from blog.models import Post
   from blog.serializers import PostProtoSerializer
   from django_grpc_framework import generics


   class PostService(generics.ModelService):
      queryset = Post.objects.all()
      serializer_class = PostProtoSerializer


GenericService
--------------

This class extends ``Service`` class, adding commonly required behavior for
standard list and detail services.  All concrete generic services is built by
composing ``GenericService``, with one or more mixin classes.

Attributes
``````````

**Basic settings:**

The following attributes control the basic service behavior:

- ``queryset`` - The queryset that should be used for returning objects from this
  service.  You must set this or override the ``get_queryset`` method, you should
  call ``get_queryset`` instead of accessing this property directly, as ``queryset``
  will get evaluated once, and those results will be cached for all subsequent
  requests.
- ``serializer_class`` - The serializer class that should be used for validating
  and deserializing input, and for serializing output. You must either set this
  attribute, or override the ``get_serializer_class()`` method.
- ``lookup_field`` - The model field that should be used to for performing object
  lookup of individual model instances. Defaults to primary key field name.
- ``lookup_request_field`` - The request field that should be used for object
  lookup.  If unset this defaults to using the same value as ``lookup_field``.

Methods
```````

.. currentmodule:: django_grpc_framework.generics

.. autoclass:: GenericService
   :members:


Mixins
------

The mixin classes provide the actions that are used to privide the basic
service behavior.  The mixin classes can be imported from
``django_grpc_framework.mixins``.

.. currentmodule:: django_grpc_framework.mixins

.. autoclass:: ListModelMixin
   :members:

.. autoclass:: CreateModelMixin
   :members:

.. autoclass:: RetrieveModelMixin
   :members:

.. autoclass:: UpdateModelMixin
   :members:

.. autoclass:: DestroyModelMixin
   :members:


Concrete service classes
------------------------

The following classes are the concrete generic services.  They can be imported
from ``django_grpc_framework.generics``.

.. currentmodule:: django_grpc_framework.generics

.. autoclass:: CreateService
   :members:

.. autoclass:: ListService
   :members:

.. autoclass:: RetrieveService
   :members:

.. autoclass:: DestroyService
   :members:

.. autoclass:: UpdateService
   :members:

.. autoclass:: ReadOnlyModelService
   :members:

.. autoclass:: ModelService
   :members:

You may need to provide custom classes that have certain actions, to create
a base class that provides ``List()`` and ``Create()`` handlers, inherit from
``GenericService`` and mixin the required handlers::

    from django_grpc_framework import mixins
    from django_grpc_framework import generics

    class ListCreateService(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            GenericService):
        """
        Concrete service that provides ``Create()`` and ``List()`` handlers.
        """
        pass
