Identity SDK
============

Tanker identity generation in Python for the `Tanker SDK <https://tanker.io/docs/latest>`_.

.. image:: https://travis-ci.org/TankerHQ/identity-python.svg?branch=master
    :target: https://travis-ci.org/TankerHQ/identity-python

.. image:: https://img.shields.io/pypi/v/tankersdk_identity.svg
    :target: https://pypi.org/project/tankersdk_identity

.. image:: https://img.shields.io/codecov/c/github/TankerHQ/identity-python.svg?label=Coverage
    :target: https://codecov.io/gh/TankerHQ/identity-python


Installation
------------


With `pip`:

.. code-block:: console

    $ pip install tankersdk-identity


API
---


.. code-block:: python

    tankersdk_identity.create_identity(trustchain_id, trustchain_private_key, user_id)

Create a new Tanker identity. This identity is secret and must only be given to a user who has been authenticated by your application. This identity is used by the Tanker client SDK to open a Tanker session

**trustchain_id**
   The trustchain ID. You can access it from the `Tanker dashboard <https://dashboard.tanker.io>`_.

**trustchain_private_key**
   The trustchain private key. A secret that you have saved right after the creation of you trustchain.
**user_id**
   The ID of a user in your application.

.. code-block:: python

    tankersdk_identity.create_provisional_identity(trustchain_id, email)

Create a Tanker provisional identity. It allows you to share a resource with a user who does not have an account in your application yet.

**trustchain_id**
   The trustchain ID. You can access it from the `Tanker dashboard <https://dashboard.tanker.io>`_.

**email**
   The email of the potential recipient of the resource.

.. code-block:: python

    tankersdk_identity.get_public_identity(identity)

Return the public identity from an identity. This public identity can be used by the Tanker client SDK to share encrypted resource.

**identity**
   A secret identity.

.. code-block:: python

    tankersdk_identity.upgrade_user_token(trustchain_id, user_id, user_token)

Return a Tanker identity from Tanker v1 user Token. Tanker v1 used a user token, when migrating to Tanker v2 you should use this function to migrate you used tokens to identities. This identity is secret and must only be given to a user who has been authenticated by your application. This identity is used by the Tanker client SDK to open a Tanker session

**trustchain_id**
   The trustchain ID. You can access it from the `Tanker dashboard <https://dashboard.tanker.io>`_.

**user_id**
   The ID of a user in your application.

**user_token**
   The Tanker v1 user token.

Going further
-------------


Read more about identities in the `Tanker guide <https://tanker.io/docs/latest/guide/server/>`_.

Check the `examples <https://github.com/TankerHQ/identity-python/tree/master/examples>`_ folder for usage examples.
