.. _serializers:

Serializers
===========

- ``proto_class`` - The protobuf class that should be used for create output
  proto message object.  You must either set this attribute, or override the
  ``data_to_message()`` method.