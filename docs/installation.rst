.. _installation:

Installation
============


Requirements
------------

We requires the following:

- Python (3.6, 3.7, 3.8)
- Django (2.2, 3.0)
- Django REST Framework (3.10.x, 3.11.x)
- gRPC
- gRPC tools
- proto3


virtualenv
----------

Virtualenv might be something you want to use for development!  let's create
one working environment::

    $ mkdir myproject
    $ cd myproject
    $ python3 -m venv env
    $ source env/bin/activate

It is time to get the django grpc framework::

    $ pip install djangogrpcframework
    $ pip install django
    $ pip install djangorestframework
    $ pip install grpcio
    $ pip install grpcio-tools


System Wide
-----------

Install it for all users on the system::

    $ sudo pip install djangogrpcframework


Development Version
-------------------

Try the latest version::

    $ source env/bin/activate
    $ git clone https://github.com/fengsp/django-grpc-framework.git
    $ cd django-grpc-framework
    $ python setup.py develop
