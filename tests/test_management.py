from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class CreatesuperuserManagementCommandTestCase(TestCase):
    def test_command_minimal(self) -> None:
        new_io = StringIO()

        call_command(
            'createsuperuser',
            interactive=False,
            email_address='staff@example.com',
            verbosity=0,
            stdout=new_io,
            stderr=new_io,
        )

    # TODO: Add tests.
    #   See:
    #   - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L253-L1036
    #   - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L1039-L1088
