=====
Usage
=====

To use Fyndata Django Accounts in a project, add it to your ``INSTALLED_APPS``:

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
