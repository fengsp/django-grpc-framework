.. _installation:

Installation
============


Requirements
------------

We requires the following:

- Python (3.6,3.7,3.8)
- Django (2.0,2.1,2.2,3.0)


virtualenv
----------

Virtualenv might be something you want to use for development!  If you do not
have it yet, try the following command::

    $ sudo pip install virtualenv

Since we have virtualenv installed now, let's create one working environment::

    $ mkdir myproject
    $ cd myproject
    $ virtualenv venv
    $ . venv/bin/activate

It is time to get the django grpc framework::

    $ pip install djangogrpcframework


System Wide
-----------

Install it for all users on the system::

    $ sudo pip install djangogrpcframework


Development Version
-------------------

Try the latest version::

    $ . venv/bin/activate
    $ git clone https://github.com/fengsp/django-grpc-framework.git
    $ cd django-grpc-framework
    $ python setup.py develop