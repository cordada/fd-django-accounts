"""
Fyndata Django Accounts
=======================

Reusable Django app to replace the default Django user (account) model,
whose implementation is located in the package (and Django app)
:mod:`django.contrib.auth`.

.. note::
    The Python package name is ``fd_dj_accounts``, not ``fd_accounts``, to
    avoid possible namespace clashes in the future. However, we refer to
    this Django app as "Fyndata Accounts" or just "Accounts".

.. note::
    Throughout Django code and documentation the term "user" is short for
    "user account".


Authentication Backend
----------------------

Custom Django authentication backend
:class:`fd_dj_accounts.auth_backends.AuthUserModelAuthBackend` allows using
ANY custom user model for authentication and authorization (not necessarily
the one included in ``fd_dj_accounts``).

To use this backend, the selected auth user model must be a subclass of
:class:`django.contrib.auth.base_user.AbstractBaseUser` (or be compatible
with), and its model manager must be a subclass of
:class:`django.contrib.auth.base_user.BaseUserManager` (or be compatible
with).

..warning::
    Do not confuse `:class:`django.contrib.auth.base_user.AbstractBaseUser`
    with :class:`django.contrib.auth.models.AbstractUser` (the latter is a
    subclass of the former).


Base custom Django user (account) model
---------------------------------------

The abstract model :class:`fd_dj_accounts.base_models.BaseUser` is quite
similar to the one it replaces (:class:`django.contrib.auth.models.User`
and its parents).

The main differences are:
- Username field is ``email_address``, and ``username`` is gone.
- Remove all about groups and permissions.
- Remove all about "names" (first, last, short, full, etc).
- Add support for "deactivation".
- Rename some fields.

For the customizations it was necessary to recreate the model manager and
the "anonymous user" class as well.


Concrete custom Django user (account) model
-------------------------------------------

Main changes of :class:`fd_dj_accounts.models.User` with respect to
:class:`fd_dj_accounts.base_models.BaseUser`:
- New field ``created_by``.
- Change field `id`: UUID instead of int.

Also, in :mod:`fd_dj_accounts.models` the concept of "system user" is
introduced, which makes sense if we want to register the actions performed
by the app itself, even if those correspond to actions executed manually
by developers o sysadmins.
A "system user" is also necessary to be able to set the user model field
``created_by`` when an instance is created on behalf of no "real user".


About customization of the Django user model
--------------------------------------------

.. seealso::
    https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-a-custom-user-model
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django.contrib.auth.models.User


"""


__version__ = '0.15.0'


default_app_config = 'fd_dj_accounts.apps.AccountsAppConfig'
