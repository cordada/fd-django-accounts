"""Authentication backends for :func:`django.contrib.auth.authenticate`.

This module allows using a custom user model for authentication and
authorization when ``django.contrib.auth`` is not in ``INSTALLED_APPS``,
because that app will still play a significant (although subtle) role.

Why? Because, unfortunately, the default authentication backend
:class:`django.contrib.auth.backends.ModelBackend` requires that the chosen
auth user model is a subclass of
:class:`django.contrib.auth.models.AbstractUser`, which is an extremely
opinionated user model, unlike
:class:`django.contrib.auth.base_user.AbstractBaseUser`.

The provided backend :class:`AuthUserModelAuthBackend` does not require that
the project where it is used has :class:`fd_dj_accounts.models.User`
set as its auth user model.

Notes:
- It is possible that the developer does not use Django's
  :func:`django.contrib.auth.authenticate` directly but there are plenty of
  cases where it is used indirectly e.g.:
  - In session-backed authentication.
  - By some third-party packages, such as Django REST Framework's
    authentication classes (see ``rest_framework.compat.authenticate``).
- Do not confuse ``django.contrib.auth``'s ``base_user.AbstractBaseUser``
  with ``models.AbstractUser`` (the latter is a subclass of the former).
- Although Django names these kind of backends as "Authentication Backends",
  they are also used for authorization (see
  https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#handling-authorization-in-custom-backends).
- The setting ``AUTHENTICATION_BACKENDS`` defines which backends are used.


TODO: submit the module's code to the Django project.

"""
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


UserModel = get_user_model()


class AbstractAuthBackend:

    """
    Minimal abstract auth backend as required by Django.

    Requirements are described in Django docs
    https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#writing-an-authentication-backend

    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        **kwargs: Any,
    ) -> Optional[Any]:
        """
        Validate credentials and return a user object.

        The keyword arguments must be enough to identify the corresponding user
        and validate the credentials.

        A common signature for this method is
        ``authenticate(self, request, username=None, password=None)``.

        :param request: may be None if it wasn't provided to ``authenticate()``,
            which passes it on to the backend
        :param kwargs: user's credentials set to check
        :return: user object that matches the credentials set if they are
            valid, else None

        """
        raise NotImplementedError  # pragma: no cover

    def get_user(self, user_id: Any) -> Optional[Any]:
        """
        Return user object identified by ``user_id``, if available for auth.

        :param user_id: the primary key of the user object (it could be a
            username, database ID or however it is defined in the user model),
            or the string version: ``str(user_id)``
        :return: user object, if it exists and is usable for authentication,
            else None

        """
        raise NotImplementedError  # pragma: no cover


class AuthUserModelAuthBackend(AbstractAuthBackend):

    """
    Authenticate against ``settings.AUTH_USER_MODEL``.

    To use this backend, the selected auth user model must be a subclass of
    :class:`django.contrib.auth.base_user.AbstractBaseUser` (or be compatible
    with), and its model manager must be a subclass of
    :class:`django.contrib.auth.base_user.BaseUserManager` (or be compatible
    with).

    Thus it is not required that the auth user model be
    :class:`fd_dj_accounts.models.User`.

    .. seealso::

        Django docs about "Writing an authentication backend"
        https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#writing-an-authentication-backend


    .. note::

        The code is largely based on
        :class:`django.contrib.auth.backends.ModelBackend`.

    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Any = None,
        password: str = None,
        **kwargs: Any,
    ) -> Optional[AbstractBaseUser]:
        # TODO: raise an error if neither arg 'username' nor an arg named as the auth user model
        #   'USERNAME_FIELD' was provided. By returning None in that case, the function is hiding
        #   the fact that the call signature was wrong in the first place i.e. swallowing a
        #   programming error. See test
        #   'AuthUserModelAuthBackendTestMixin.test_authenticate_bad_username_field'.

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        return None

    def user_can_authenticate(self, user: AbstractBaseUser) -> bool:
        """
        Do not let inactive users authenticate.
        """
        let_user_authenticate: bool = user.is_active
        return let_user_authenticate

    def get_user(self, user_id: Any) -> Optional[AbstractBaseUser]:
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
