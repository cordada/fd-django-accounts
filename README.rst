=============================
Fyndata Django Accounts
=============================

.. image:: https://badge.fury.io/py/fyndata-django-accounts.svg
    :target: https://badge.fury.io/py/fyndata-django-accounts

.. image:: https://circleci.com/gh/fyndata/gcp-utils-python/tree/develop.svg?style=shield
    :target: https://circleci.com/gh/fyndata/fyndata-django-accounts/tree/develop

.. image:: https://codecov.io/gh/fyndata/fyndata-django-accounts/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/fyndata/fyndata-django-accounts

Reusable Django app to replace the default Django user (account) model.

Documentation
-------------

The full documentation is at https://fyndata-django-accounts.readthedocs.io.

Quickstart
----------

Install Fyndata Django Accounts::

    pip install fyndata-django-accounts

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fd_dj_accounts',
        ...
    )

Add Fyndata Django Accounts's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        path('', include('fd_dj_accounts.urls')),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
