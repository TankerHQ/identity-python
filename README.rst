Identity SDK
============

Tanker identity generation in Python for the `Tanker SDK <https://tanker.io/docs/latest>`_.

.. image:: https://travis-ci.org/TankerHQ/identity-python.svg?branch=master
    :target: https://travis-ci.org/TankerHQ/identity-python

.. image:: https://img.shields.io/pypi/v/tankersdk-user-token.svg
    :target: https://pypi.org/project/tankersdk-user-token


Installation
------------


With `pip`:

.. code-block:: console

    $ pip install tankersdk-identity


Usage
-----



.. code-block:: python

      import tanker_identity.identity

      def retrieve_identity(user_id):
          """ Fetch a previously stored identity """
          ...


       def store_identity(user_id, identity):
          """ Store a previously generated identity """
          ...


       def check_auth(user_id):
          """ Check the user is authenticated """
          ...


      def serve_user_identity(user_id):
          """ Called during sign/up sign in of your users.

          Send a user identity, generated if necessary,
          but only to authenticated users
          """
          authorized = check_auth(user_id)
          if not authorized:
              raise UnAuthorizedError()

          token = retrieve_user_identity(user_id)

          if not identity:
            identity = tanker_identity.identity.create_identity(trustchain_id, trustchain_private_key, user_id)
            store_user_identity(user_id, identity)

          return identity


Going further
-------------


Read more about identities in the `Tanker guide <https://tanker.io/docs/latest/guide/server/>`_.

Check the `examples <https://github.com/TankerHQ/identity-python/tree/master/examples>`_ folder for usage examples.
