from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from fd_dj_accounts.models import User


class CreatesuperuserManagementCommandTestCase(TestCase):
    def test_basic_usage(self) -> None:
        """
        Check the operation of the createsuperuser management command
        """
        # We can use the management command to create a superuser
        new_io = StringIO()
        call_command(
            'createsuperuser',
            interactive=False,
            email_address='staff@example.com',
            stdout=new_io
        )
        command_output = new_io.getvalue().strip()
        self.assertEqual(command_output, 'Superuser created successfully.')
        u = User.objects.get(email_address='staff@example.com')
        self.assertEqual(u.get_username(), 'staff@example.com')

        # created password should be unusable
        self.assertFalse(u.has_usable_password())

    # TODO: Add tests.
    #   See:
    #   - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L253-L1036
    #   - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L1039-L1088
