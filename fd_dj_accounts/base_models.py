"""
Base implementation and abstract models.

This module allows importing :class:`BaseUser`, :class:`UserManager` and
:class:`AnonymousUser` even when ``fd_dj_accounts`` is not in setting
``INSTALLED_APPS`` (analogous to :mod:`django.contrib.auth.base_user`).

"""
from typing import Any, List, Tuple, Type  # noqa: F401

import django.contrib.auth.base_user
from django.db import models
from django.utils import timezone


class UserManager(django.contrib.auth.base_user.BaseUserManager):

    """
    Model manager for a custom user (account) model.

    It is almost identical to its parent class
    (:class:`django.contrib.auth.base_user.BaseUserManager`).
    The changes are:
    - All those related to removing the field ``username``.
    - Add type annotations.

    .. seealso:: :class:`BaseUser`.

    """

    use_in_migrations = False

    def _create_user(
        self, email_address: str, password: str = None,
        **extra_fields: Any,
    ) -> 'BaseUser':
        """
        Create and save a user with the given email address and password.

        If ``password`` is None, it will be set to an unusable one.

        """
        if not email_address:
            raise ValueError('The given email address must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)  # type: BaseUser
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(
        self, email_address: str, password: str = None,
        **extra_fields: Any,
    ) -> 'BaseUser':
        """
        Create and save a user with the given email address and password.

        If ``password`` is None, it will be set to an unusable one.

        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email_address, password, **extra_fields)

    def create_superuser(
        self, email_address: str, password: str,
        **extra_fields: Any,
    ) -> 'BaseUser':
        """
        Create and save a superuser with the given email address and password.

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_address, password, **extra_fields)


class BaseUser(django.contrib.auth.base_user.AbstractBaseUser):

    """
    Abstract model for a custom Django user (account) model.

    It is mostly a customization of :class:`django.contrib.auth.models.User`
    and its parent class :class:`django.contrib.auth.models.AbstractUser`:
    - Remove all about groups and permissions.
    - Delete field ``username``: use ``email_address`` instead (renamed from
      ``email``).
    - Rename ``date_joined`` to ``created_at``.
    - Add support for "deactivation", including new field ``deactivated_at``.
    - Remove method ``email_user``.
    - Remove all about names: ``first_name``, ``last_name``,
      ``get_short_name``, ``get_full_name``.

    Also add type annotations and some minor changes to comply with
    ``mypy`` and ``flake8``.

    .. seealso:: :class:`AnonymousUser`.

    """

    class Meta:
        # note: Django model's Meta at the top for clarity.
        abstract = True

    # The name of the field on the user model that is used as the unique identifier.
    # required
    USERNAME_FIELD = 'email_address'

    # required
    EMAIL_FIELD = 'email_address'

    # note: "'REQUIRED_FIELDS' must contain all required fields on your user model, but should not
    #   contain the 'USERNAME_FIELD' or 'password' as these fields will always be prompted for."
    # required
    REQUIRED_FIELDS = []  # type: List[str]

    email_address = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        error_messages={
            'unique': "A user with that email address already exists.",
        },
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Whether this user should be treated as enabled. "
            "Deactivate a user account instead of deleting it."
        ),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=(
            "Designates that this user has all permissions without explicitly assigning them."
        ),
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        blank=False,
        null=False,
    )
    deactivated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    objects = UserManager()

    # note: even though it is highly recommended to override 'save()' so 'full_clean()' is called
    #   before, it corresponds to the concrete models to make that choice.
    # def save(self, *args: Any, **kwargs: Any) -> None:
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def clean(self) -> None:
        # note: the username normalization is performed in
        #   'django.contrib.auth.base_user.AbstractBaseUser.clean()'.
        super().clean()
        klass = self.__class__  # type: Type[BaseUser]
        self.email_address = klass.objects.normalize_email(self.email_address)

    def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
        if self.deactivated_at is None:
            self.deactivated_at = timezone.now()
        self.save()


class AnonymousUser:

    """
    "Anonymous User" entity appropriate for the custom Django user model.

    It is a minor simplification and customization of
    :class:`django.contrib.auth.models.AnonymousUser` (which corresponds
    to the user model :class:`django.contrib.auth.models.User`).

    The customizations are a reflection of the difference between
    :class:`django.contrib.auth.models.User` and :class:`BaseUser`.

    .. seealso:: :class:`BaseUser`.

    """

    id = None
    pk = None
    email_address = ''
    is_staff = False
    is_active = False
    is_superuser = False
    created_at = None
    deactivated_at = None

    def __str__(self) -> str:
        return 'AnonymousUser'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return 1  # instances always return the same hash value

    def save(self) -> None:
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self) -> Tuple[int, dict]:
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password: str) -> None:
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password: str) -> bool:
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def deactivate(self) -> None:
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def is_anonymous(self) -> bool:
        return True

    @property
    def is_authenticated(self) -> bool:
        return False

    def get_username(self) -> str:
        # Class attribute 'BaseUser.USERNAME_FIELD' is 'email_address'.
        return self.email_address
