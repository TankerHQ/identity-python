flask server example
====================

Installation
--------------

.. code-block:: console

    $ pip install flask
    $ pip install git+https://github.com/supertanker/user-token-python@master


Usage
-----

.. code-block:: console

    $ cd examples/flask
    $ FLASK_DEBUG=1 FLASK_APP=server.py flask run


.. note::

    User tokens are generated only once and never stored. In a real application you should implement a persistent storage.
