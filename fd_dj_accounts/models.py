"""
Concrete models.

"""
from typing import Any  # noqa: F401
import uuid

from django.conf import settings
from django.db import models

from . import base_models


def get_or_create_system_user() -> 'User':
    """Return the "system user", which is created by itself.

    The system user is created, by default:
    - as active
    - as superuser (which implies as staff as well)
    - with unusable password

    However, it is alright to modify any of this user's properties after its
    creation, just as if it were any other user, except the password.

    """
    system_user_email_address = settings.APP_ACCOUNTS_SYSTEM_USERNAME
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


class UserManager(base_models.UserManager):

    """
    Manager for model :class:`User`.

    Extra customizations (besides those in the parent class):
    - Default value for field ``created_by`` is the system user.

    """

    use_in_migrations = False

    def _create_user(self, email_address: str, password: str = None, **extra_fields: Any) -> 'User':
        """
        Customization.

        This override is necessary for setting a default value for field
        ``created_by``: the system user.

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


class User(base_models.BaseUser):

    """
    Custom Django user (account) model.

    Extra customizations (besides those in the parent class):
    - New field ``created_by``.
    - Change field `id`: UUID instead of int.
    - Override :meth:`save` to make sure full validation is performed before
      each and every save (including creation).
    - Custom model manager.

    .. seealso:: :class:`AnonymousUser`.

    """

    # Explicit override of auto-generated integer model field 'id' (primary key).
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_by = models.ForeignKey(
        to='fd_dj_accounts.User',
        on_delete=models.PROTECT,
        related_name='users_created',
        blank=False,
        null=False,
    )

    objects = UserManager()

    class Meta:
        abstract = False

        verbose_name = 'user'
        verbose_name_plural = 'users'

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Call :meth:`full_clean` before saving."""
        self.full_clean()
        super().save(*args, **kwargs)


class AnonymousUser(base_models.AnonymousUser):

    """
    "Anonymous User" corresponding to the custom Django user model.

    The changes are a reflection of those applied to :class:`User`.

    .. seealso:: :class:`User`.

    """

    created_by = None
