.. _testing:

Testing
=======

Django gRPC framework includes a few helper classes that come in handy when
writing tests for services.


The test channel
----------------

The test channel is a Python class that acts as a dummy gRPC channel,
allowing you to test you services.  You can simulate gRPC requests on a
service method and get the response.  Here is a quick example, let's open
Django shell ``python manage.py shell``:

.. code-block:: pycon

    >>> from django_grpc_framework.test import Channel
    >>> channel = Channel()
    >>> stub = post_pb2_grpc.PostControllerStub(channel)
    >>> response = stub.Retrieve(post_pb2.PostRetrieveRequest(id=post_id))
    >>> response.title
    'This is a title'


RPC test cases
--------------

Django gRPC framework includes the following test case classes, that mirror
the existing Django test case classes, but provide a test ``Channel``
instead of ``Client``.

- ``RPCSimpleTestCase``
- ``RPCTransactionTestCase``
- ``RPCTestCase``

You can use these test case classes as you would for the regular Django test
case classes, the ``self.channel`` attribute will be an ``Channel`` instance::

    from django_grpc_framework.test import RPCTestCase
    from django.contrib.auth.models import User
    import account_pb2
    import account_pb2_grpc


    class UserServiceTest(RPCTestCase):
        def test_create_user(self):
            stub = account_pb2_grpc.UserControllerStub(self.channel)
            response = stub.Create(account_pb2.User(username='tom', email='tom@account.com'))
            self.assertEqual(response.username, 'tom')
            self.assertEqual(response.email, 'tom@account.com')
            self.assertEqual(User.objects.count(), 1)
