.. _protos:

Proto
=====

Django gRPC framework provides support for automatic generation of proto_.

.. _proto: https://developers.google.com/protocol-buffers/docs/proto3


Generate proto for model
------------------------

If you want to automatically generate proto definition based on a model,
you can use the ``generateproto`` management command::

    python manage.py generateproto --model django.contrib.auth.models.User

To specify fields and save it to a file, use::

    python manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email --file demo.proto

Once you've generated a proto file in this way, you can edit it as you wish.