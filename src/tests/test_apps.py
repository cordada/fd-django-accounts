import django.core.exceptions
from django.test import SimpleTestCase, override_settings

from fd_dj_accounts.apps import AccountsAppConfig, _validate_app_settings


@override_settings(APP_ACCOUNTS_SYSTEM_USERNAME='user@example.com')
class AppConfigTestCase(SimpleTestCase):

    def test_ready(self):  # type: ignore
        from django.apps.registry import apps

        _app_config = apps.app_configs['fd_dj_accounts']
        app_config = AccountsAppConfig(
            app_name=_app_config.name,
            app_module=_app_config.module,
        )

        # Nothing should be raised.
        app_config.ready()


class FunctionsTestCase(SimpleTestCase):

    @override_settings(APP_ACCOUNTS_SYSTEM_USERNAME='user@example.com')
    def test__validate_app_settings_ok(self):  # type: ignore
        # nothing is raised by default.
        _validate_app_settings()

    @override_settings()
    def test__validate_app_settings_fail_not_set(self):  # type: ignore
        from django.conf import settings

        # To remove a setting properly we must use the decorator '@override_settings'.
        del settings.APP_ACCOUNTS_SYSTEM_USERNAME

        exc_class = django.core.exceptions.ImproperlyConfigured
        exc_msg = "Setting 'APP_ACCOUNTS_SYSTEM_USERNAME' must be set."
        with self.assertRaisesMessage(exc_class, exc_msg):
            _validate_app_settings()

    @override_settings(APP_ACCOUNTS_SYSTEM_USERNAME='accounts-system-user@local host')
    def test__validate_app_settings_fail_invalid(self):  # type: ignore
        exc_class = django.core.exceptions.ImproperlyConfigured
        exc_msg = "Setting 'APP_ACCOUNTS_SYSTEM_USERNAME' value is not a valid email address."
        with self.assertRaisesMessage(exc_class, exc_msg):
            _validate_app_settings()
