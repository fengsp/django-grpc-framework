.. _services:

Services
========

Django gRPC framework provides an ``Service`` class, which is pretty much the
same as using a regular gRPC generated servicer interface.  For example::

    import grpc
    from django_grpc_framework.services import Service
    from blog.models import Post
    from blog.serializers import PostProtoSerializer


    class PostService(Service):
        def get_object(self, pk):
            try:
                return Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                self.context.abort(grpc.StatusCode.NOT_FOUND, 'Post:%s not found!' % pk)

        def Retrieve(self, request, context):
            post = self.get_object(request.id)
            serializer = PostProtoSerializer(post)
            return serializer.message


Service instance attributes
---------------------------

The following attributes are available in a service instance.

- ``.request`` - the gRPC request object
- ``.context`` - the ``grpc.ServicerContext`` object
- ``.action`` - the name of the current service method


As servicer method
------------------

.. currentmodule:: django_grpc_framework.services

.. automethod:: Service.as_servicer


Root handlers hook
------------------

We need a hanlders hook function to add all servicers to the server, for
example::

    def grpc_handlers(server):
        demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

You can set the root handlers hook using the ``ROOT_HANDLERS_HOOK`` setting
key, for example set the following in your ``settings.py`` file::

    GRPC_FRAMEWORK = {
        ...
        'ROOT_HANDLERS_HOOK': 'path.to.your.curtom_grpc_handlers',
    }

The default setting is ``'{settings.ROOT_URLCONF}.grpc_handlers'``.