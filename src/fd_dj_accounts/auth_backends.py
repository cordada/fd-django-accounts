"""Authentication backends for :func:`django.contrib.auth.authenticate`.

This module allows using a custom user model for authentication and
authorization.

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
  https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#handling-authorization-in-custom-backends).
- The setting ``AUTHENTICATION_BACKENDS`` defines which backends are used.

"""

from __future__ import annotations

from typing import Any, Optional, Set, TYPE_CHECKING, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

if TYPE_CHECKING:
    import django.db.models

    from .base_models import AnonymousUser


UserModel = get_user_model()


class AuthUserModelAuthBackend(ModelBackend):

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
        https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-an-authentication-backend

    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[AbstractBaseUser]:
        # Use implementation from :class`django.contrib.auth.backends.ModelBackend`.
        return super().authenticate(request, username, password, **kwargs)

    def user_can_authenticate(self, user: Union[AbstractBaseUser, AnonymousUser]) -> bool:
        # Use implementation from :class`django.contrib.auth.backends.ModelBackend`.
        return super().user_can_authenticate(user)  # type: ignore[no-any-return]

    _get_user_permissions = None  # Unsupported operation

    _get_group_permissions = None  # Unsupported operation

    _get_permissions = None  # Unsupported operation

    def get_user_permissions(
        self,
        user_obj: Union[AbstractBaseUser, AnonymousUser],
        obj: Optional[django.db.models.Model] = None,
    ) -> Set[str]:
        # Use implementation from :class`django.contrib.auth.backends.BaseBackend`.
        return super(ModelBackend, self).get_user_permissions(user_obj, obj)  # type: ignore[no-any-return] # noqa: E501

    def get_group_permissions(
        self,
        user_obj: Union[AbstractBaseUser, AnonymousUser],
        obj: Optional[django.db.models.Model] = None,
    ) -> Set[str]:
        # Use implementation from :class`django.contrib.auth.backends.BaseBackend`.
        return super(ModelBackend, self).get_group_permissions(user_obj, obj)  # type: ignore[no-any-return] # noqa: E501

    def get_all_permissions(
        self,
        user_obj: Union[AbstractBaseUser, AnonymousUser],
        obj: Optional[django.db.models.Model] = None,
    ) -> Set[str]:
        # Use implementation from :class`django.contrib.auth.backends.ModelBackend`.
        return super().get_all_permissions(user_obj, obj)  # type: ignore[no-any-return]

    def has_perm(
        self,
        user_obj: Union[AbstractBaseUser, AnonymousUser],
        perm: str,
        obj: Optional[django.db.models.Model] = None,
    ) -> bool:
        # Use implementation from :class`django.contrib.auth.backends.ModelBackend`.
        return super().has_perm(user_obj, perm, obj)  # type: ignore[no-any-return]

    def has_module_perms(
        self,
        user_obj: Union[AbstractBaseUser, AnonymousUser],
        app_label: str,
    ) -> bool:
        # Use implementation from :class`django.contrib.auth.backends.ModelBackend`.
        return super().has_module_perms(user_obj, app_label)  # type: ignore[no-any-return]

    with_perm = None  # Unsupported operation

    def get_user(self, user_id: Any) -> Optional[AbstractBaseUser]:
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
