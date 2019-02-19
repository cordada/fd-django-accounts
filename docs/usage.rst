=====
Usage
=====

To use Fyndata Django Accounts in a project, add it to your `INSTALLED_APPS`:

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
