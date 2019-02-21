=============================
Fyndata Django Accounts
=============================

.. image:: https://img.shields.io/pypi/v/fyndata-django-accounts.svg
    :target: https://pypi.python.org/pypi/fyndata-django-accounts
    :alt: PyPI package version

.. image:: https://img.shields.io/pypi/pyversions/fyndata-django-accounts.svg
    :target: https://pypi.python.org/pypi/fyndata-django-accounts
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/fyndata-django-accounts.svg
    :target: https://pypi.python.org/pypi/fyndata-django-accounts
    :alt: License

Reusable Django app to replace the default Django user (account) model.

Documentation
-------------

The full documentation is at https://fyndata-django-accounts.readthedocs.io.

Status
-------------

.. image:: https://circleci.com/gh/fyndata/gcp-utils-python/tree/develop.svg?style=shield
    :target: https://circleci.com/gh/fyndata/fyndata-django-accounts/tree/develop
    :alt: CI status

.. image:: https://codecov.io/gh/fyndata/fyndata-django-accounts/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/fyndata/fyndata-django-accounts
    :alt: Code coverage

.. image:: https://readthedocs.org/projects/fyndata-django-accounts/badge/?version=latest
    :target: https://fyndata-django-accounts.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation

Quickstart
----------

Install Fyndata Django Accounts::

    pip install fyndata-django-accounts

Add it to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fd_dj_accounts',
        ...
    )

Set the following Django standard settings:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'fd_dj_accounts.auth_backends.AuthUserModelAuthBackend',
    ]
    AUTH_USER_MODEL = 'fd_dj_accounts.User'

and the following settings created by this app:

.. code-block:: python

    APP_ACCOUNTS_SYSTEM_USERNAME = 'accounts-system-user@localhost'  # arbitrary value

Features
--------

* TODO

Developers
----------

See 'CONTRIBUTING.rst'.

Tests
+++++

Requirements::

    pip install -r requirements_test.txt

Run test suite for all supported Python versions and run tools for
code style analysis, static type check, etc::

    make test-all
    make lint

Check code coverage of tests::

    make test-coverage
    make test-coverage-report-console

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
