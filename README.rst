.. image::  https://tanker.io/images/github-logo.png
   :target: #readme


Identity SDK
============

Tanker identity generation in Python for the `Tanker SDK <https://docs.tanker.io/latest/>`_.

.. image:: https://github.com/TankerHQ/identity-python/workflows/Tests/badge.svg
    :target: https://github.com/TankerHQ/identity-python/actions

.. image:: https://img.shields.io/pypi/v/tankersdk_identity.svg
    :target: https://pypi.org/project/tankersdk_identity

.. image:: https://img.shields.io/codecov/c/github/TankerHQ/identity-python.svg?label=Coverage
    :target: https://codecov.io/gh/TankerHQ/identity-python
    
.. image:: https://img.shields.io/badge/deps%20scanning-pyup.io-green
     :target: https://github.com/TankerHQ/identity-python/workflows/safety/


Installation
------------


With `pip`:

.. code-block:: console

    $ pip install tankersdk-identity


API
---


.. code-block:: python

    tankersdk_identity.create_identity(app_id, app_secret, user_id)

Create a new Tanker identity. This identity is secret and must only be given to a user who has been authenticated by your application. This identity is used by the Tanker client SDK to open a Tanker session

**app_id**
   The app ID, must match the one used in the constructor of the Core SDK.

**app_secret**
   The app secret, secret that you have saved right after the creation of your app.

**user_id**
   The ID of a user in your application.

.. code-block:: python

    tankersdk_identity.create_provisional_identity(app_id, "email", email)

Create a Tanker provisional identity. It allows you to share a resource with a user who does not have an account in your application yet.

**app_id**
   The app ID, must match the one used in the constructor of the Core SDK.

**email**
   The email of the potential recipient of the resource.

.. code-block:: python

    tankersdk_identity.get_public_identity(identity)

Return the public identity from an identity. This public identity can be used by the Tanker client SDK to share encrypted resource.

**identity**
   A secret identity.


Going further
-------------


Read more about identities in the `Tanker guide <https://docs.tanker.io/latest/guides/identity-management/>`_.

Check the `examples <https://github.com/TankerHQ/identity-python/tree/master/examples>`_ folder for usage examples.
