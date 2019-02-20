"""User account custom model.

This model is quite similar to the one it replaces
(:class:`django.contrib.auth.models.User`) (for more details, see
:class:`User`).

For that customization, the model manager plus the related class
``AnonymousUser`` had to be recreated as well.

Also, this app introduces the concept of "system user", which makes sense if
we want to register the actions performed by the app itself, even if those
correspond to actions executed manually by developers o sysadmins.
It also is necessary to have it to be able to set the User model field
``created_by`` when an instance is created on behalf of no "real user".


.. note::

    Note that throughout Django code and documentation the term "user" is short
    for "user account".


.. seealso::

    https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#specifying-a-custom-user-model
    https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#django.contrib.auth.models.User

"""
from typing import Any, List, Tuple, Type  # noqa: F401
import uuid

from django.conf import settings
import django.contrib.auth.base_user
from django.db import models
from django.utils import timezone


def get_or_create_system_user() -> 'User':
    """Return the "system user", which is created by itself.

    The system user is created, by default:
    - as active
    - as superuser (which implies as staff as well)
    - with unusable password

    However, it is alright to modify any of this user's properties after its
    creation, just as if it were any other user, except the password.

    """
    system_user_email_address = settings.FD_ACCOUNTS_SYSTEM_USER
    try:
        system_user = User.objects.get(email_address=system_user_email_address)  # type: User
    except User.DoesNotExist:
        system_user_uuid = uuid.uuid4()
        system_user = User(
            id=system_user_uuid,
            email_address=system_user_email_address,
            created_by_id=system_user_uuid,
            is_staff=True,
            is_superuser=True,
        )
        system_user.set_unusable_password()

        # Before calling 'save()' we call the parent class' implementation as a trick to skip
        #   validating field 'created_by' because it is a self reference. This only makes sense
        #   when creating a system user.
        # note: skip mypy check because it yields 'error: "super" used outside class'.
        #   See: https://github.com/python/mypy/issues/1167
        super(User, system_user).save()  # type: ignore
        system_user.save()

    return system_user


class UserManager(django.contrib.auth.base_user.BaseUserManager):

    """Manager for the custom user (account) model.

    It is almost identical to :class:`django.contrib.auth.base_user.BaseUserManager`.
    The changes are:
    - Default value for field ``created_by`` is the system user.
    - All those related to removing the field ``username``.
    - Add type annotations.

    """

    use_in_migrations = False

    def _create_user(self, email_address: str, password: str = None, **extra_fields: Any) -> 'User':
        """
        Create and save a user with the given email address and password.

        If ``password`` is None, it will be set to an unusable one.

        """
        if not email_address:
            raise ValueError('The given email address must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)  # type: User
        user.set_password(password)

        # warning: we can not just access foreign key field 'created_by' because if it has not
        #   been set the exception "User.created_by.RelatedObjectDoesNotExist" will be raised.
        if not hasattr(user, 'created_by') or user.created_by is None:
            user.created_by = get_or_create_system_user()

        user.save(using=self._db)
        return user

    def create_user(self, email_address: str, password: str = None, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email_address, password, **extra_fields)

    def create_superuser(self, email_address: str, password: str, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_address, password, **extra_fields)


class User(django.contrib.auth.base_user.AbstractBaseUser):

    """Custom user model for a user account.

    It is mostly a customization of :class:`django.contrib.auth.models.User`
    and its parent class :class:`django.contrib.auth.models.AbstractUser`:
    - Remove all about groups and permissions.
    - Delete field ``username``: use ``email_address`` instead (renamed from ``email``).
    - Change field `id`: UUID instead of int.
    - Rename ``date_joined`` to ``created_at``.
    - New fields ``created_by``, ``deactivated_at``.
    - Remove method ``email_user``.
    - Remove all about names: ``first_name``, ``last_name``, ``get_short_name``, ``get_full_name``.

    Also add type annotations and some minor changes to comply with ``mypy`` and ``flake8``.

    """

    # The name of the field on the user model that is used as the unique identifier.
    # required
    USERNAME_FIELD = 'email_address'

    # required
    EMAIL_FIELD = 'email_address'

    # note: "'REQUIRED_FIELDS' must contain all required fields on your user model, but should not
    #   contain the 'USERNAME_FIELD' or 'password' as these fields will always be prompted for."
    # required
    REQUIRED_FIELDS = []  # type: List[str]

    # Explicit override of auto-generated integer model field 'id' (primary key).
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
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
    created_by = models.ForeignKey(
        to='fd_dj_accounts.User',
        on_delete=models.PROTECT,
        related_name='users_created',
        blank=False,
        null=False,
    )
    deactivated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Call :meth:`full_clean` before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        # note: the username normalization is performed in
        #   'django.contrib.auth.base_user.AbstractBaseUser.clean()'.
        super().clean()
        klass = self.__class__  # type: Type[User]
        self.email_address = klass.objects.normalize_email(self.email_address)

    def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
        if self.deactivated_at is None:
            self.deactivated_at = timezone.now()
        self.save()


class AnonymousUser:

    """Class ``AnonymousUser`` corresponding to the custom user model for a user account.

    It is a minor simplification and customization of
    :class:`django.contrib.auth.models.AnonymousUser`.

    The changes are a reflection of those applied to :class:`User`.

    """

    id = None
    pk = None
    email_address = ''
    is_staff = False
    is_active = False
    is_superuser = False
    created_at = None
    created_by = None
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
        # Class attribute 'User.USERNAME_FIELD' is 'email_address'.
        return self.email_address
