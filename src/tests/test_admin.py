import django.contrib.admin
import django.test

from fd_dj_accounts.admin import UserAdmin


class UserAdminTestCase(django.test.TestCase):
    def test_inheritance(self) -> None:
        self.assertTrue(issubclass(UserAdmin, django.contrib.admin.ModelAdmin))

    # TODO: Add more tests.
