=============================
Fyndata Django Accounts
=============================

.. image:: https://badge.fury.io/py/fyndata-django-accounts.svg
    :target: https://badge.fury.io/py/fyndata-django-accounts

.. image:: https://travis-ci.org/fyndata/fyndata-django-accounts.svg?branch=master
    :target: https://travis-ci.org/fyndata/fyndata-django-accounts

.. image:: https://codecov.io/gh/fyndata/fyndata-django-accounts/branch/master/graph/badge.svg
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
        'fd_dj_accounts.apps.AccountsAppConfig',
        ...
    )

Add Fyndata Django Accounts's URL patterns:

.. code-block:: python

    from fd_dj_accounts import urls as fd_dj_accounts_urls


    urlpatterns = [
        ...
        url(r'^', include(fd_dj_accounts_urls)),
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