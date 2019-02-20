from django.apps import AppConfig
from django.conf import settings
import django.core.exceptions
import django.core.validators


class AccountsAppConfig(AppConfig):

    # note: the app name must be the same as the top Python package name (see its docstring).
    name = 'fd_dj_accounts'

    verbose_name = 'Fyndata Accounts'

    def ready(self) -> None:
        _validate_app_settings()


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
