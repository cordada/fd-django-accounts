from django.apps import AppConfig
from django.conf import settings
import django.core.exceptions
import django.core.validators
from django.contrib.auth import get_user_model
from django.contrib.auth.checks import check_user_model
from django.contrib.auth.signals import user_logged_in
from django.core import checks
from django.db.models.query_utils import DeferredAttribute


class AccountsAppConfig(AppConfig):

    # note: the app name must be the same as the top Python package name (see its docstring).
    name = 'fd_dj_accounts'

    verbose_name = 'Fyndata Accounts'

    def ready(self) -> None:
        _validate_app_settings()

        #######################################################################
        # note: this code block is a partial copy of 'django.contrib.auth.apps.AuthConfig.ready()'.
        last_login_field = getattr(get_user_model(), 'last_login', None)

        # Register the handler only if UserModel.last_login is a field.
        if isinstance(last_login_field, DeferredAttribute):
            from .models import update_last_login
            from .auth_backends import AbstractBaseUser
            assert issubclass(get_user_model(), AbstractBaseUser)
            user_logged_in.connect(update_last_login, dispatch_uid='update_last_login')
        #######################################################################

        checks.register(check_user_model, checks.Tags.models)


def _validate_app_settings() -> None:
    # note: we don't validate that setting 'AUTH_USER_MODEL' is set to 'fd_dj_accounts.User' because
    #   there might be other reason for a project to use this app without changing that setting.

    try:
        system_user_email_address = settings.APP_ACCOUNTS_SYSTEM_USERNAME
    except AttributeError as exc:
        msg = "Setting 'APP_ACCOUNTS_SYSTEM_USERNAME' must be set."
        raise django.core.exceptions.ImproperlyConfigured(msg) from exc
    try:
        django.core.validators.validate_email(system_user_email_address)
    except django.core.exceptions.ValidationError as exc:
        msg = "Setting 'APP_ACCOUNTS_SYSTEM_USERNAME' value is not a valid email address."
        raise django.core.exceptions.ImproperlyConfigured(msg) from exc
