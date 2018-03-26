Flask server example
====================

Installation
--------------

.. code-block:: console

    $ pip install flask
    $ pip install tankersdk-user-token


Usage
-----

.. code-block:: console

    $ cd examples/flask
    $ FLASK_DEBUG=1 FLASK_APP=server.py flask run


.. note::

    User tokens are generated only once and never stored. In a real application you should implement a persistent storage.
