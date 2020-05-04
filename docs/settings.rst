.. _settings:

Settings
========

Configuration for gRPC framework is all namespaced inside a single Django
setting, named ``GRPC_FRAMEWORK``, for example your project's ``settings.py``
file might look like this::

    GRPC_FRAMEWORK = {
        'ROOT_HANDLERS_HOOK': 'project.urls.grpc_handlers',
    }


Accessing settings
------------------

If you need to access the values of gRPC framework's settings in your project,
you should use the ``grpc_settings`` object.  For example::

    from django_grpc_framework.settings import grpc_settings
    print(grpc_settings.ROOT_HANDLERS_HOOK)

The ``grpc_settings`` object will check for any user-defined settings, and
otherwise fall back to the default values. Any setting that uses string import
paths to refer to a class will automatically import and return the referenced
class, instead of the string literal.


Configuration values
--------------------

.. py:data:: ROOT_HANDLERS_HOOK

    A hook function that takes gRPC server object as a single parameter and add
    all servicers to the server.

    Default: ``'{settings.ROOT_URLCONF}.grpc_handlers'``

    One example for the hook function::

        def grpc_handlers(server):
            demo_pb2_grpc.add_UserControllerServicer_to_server(UserService.as_servicer(), server)

.. py:data:: SERVER_INTERCEPTORS

    An optional list of ServerInterceptor objects that observe and optionally
    manipulate the incoming RPCs before handing them over to handlers.

    Default: ``None``