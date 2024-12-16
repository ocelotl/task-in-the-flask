Task-In-The-Flask
=================

This is a task-system prototype.

To run the Flask app:

.. code::

    nox
    source .nox/test/bin/activate
    flask --app src/app run

Once it is running you can make a request:

.. code::

    curl http://127.0.0.1:5000/hello

The GraphQL interface is at `localhost:5000/graphql`.
