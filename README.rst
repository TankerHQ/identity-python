User Token
==========

.. image:: https://travis-ci.org/TankerHQ/user-token-python.svg?branch=master
    :target: https://travis-ci.org/TankerHQ/user-token-python

User token generation in Python for the `Tanker SDK <https://tanker.io/docs/latest>`_.

Installation
------------


With `pip`:

.. code-block:: console

    $ pip install tankersdk-user-token


Usage
-----



.. code-block:: python

      import tankersdk.usertoken

      def retrieve_user_token(user_id):
          """ Fetch a previously stored token """
          ...


       def store_user_token(user_id, token):
          """ Store a previously generated token """
          ...


       def check_auth(user_id):
          """ Check the user is authenticated """
          ...


      def serve_user_token(user_id):
          """ Called during sign/up sign in of your users.

          Send a user token, generated if necessary, but only to
          authenticated users
          """
          authorized = check_auth(user_id)
          if not authorized:
              raise UnAuthorizedError()

          token = retrieve_user_token(user_id)

          if not token:
            token = tankersdk.usertoken.generate_user_token(trustchain_id, trustchain_private_key, user_id)
            store_user_token(user_id, token)

          return token


Going further
-------------


Read more about user tokens in the `Tanker guide <https://tanker.io/docs/latest/guide/server/>`_.

Check the `examples <https://github.com/TankerHQ/user-token-python/tree/master/examples>`_ folder for usage examples.
