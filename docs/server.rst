.. _server:

Server
======

grpcrunserver
-------------

Run a grpc server::

    $ python manage.py grpcrunserver

Run a grpc development server, this tells Django to use the auto-reloader and
run checks::

    $ python manage.py grpcrunserver --dev

Run the server with a certain address::

    $ python manage.py grpcrunserver 127.0.0.1:8000 --max-workers 5


Configuration
-------------

Setting the server interceptors
```````````````````````````````

If you need to add server interceptors, you can do so by setting the

``SERVER_INTERCEPTORS`` setting.  For example, have something like this
in your ``settings.py`` file::

    GRPC_FRAMEWORK = {
        ...
        'SERVER_INTERCEPTORS': [
            'path.to.DoSomethingInterceptor',
            'path.to.DoAnotherThingInterceptor',
        ]
    }