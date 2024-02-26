import builtins
from io import StringIO
from unittest import mock

from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings

from fd_dj_accounts import management
from fd_dj_accounts.management.commands import createsuperuser
from fd_dj_accounts.models import User


MOCK_INPUT_KEY_TO_PROMPTS = {
    'bypass': ['Bypass password validation and create user anyway? [y/N]: '],
    'email_address': ['Email address: '],
    'is_active': ['Is active: '],
    'password': ['Password: '],
}


def mock_inputs(inputs):
    """
    Decorator to temporarily replace input/getpass to allow interactive
    createsuperuser.
    """
    def inner(test_func):
        def wrapped(*args):
            class mock_getpass:
                @staticmethod
                def getpass(prompt=b'Password: ', stream=None):
                    if callable(inputs['password']):
                        return inputs['password']()
                    return inputs['password']

            def mock_input(prompt):
                assert '__proxy__' not in prompt
                response = None
                for key, val in inputs.items():
                    if val == 'KeyboardInterrupt':
                        raise KeyboardInterrupt
                    # get() fallback because sometimes 'key' is the actual
                    # prompt rather than a shortcut name.
                    prompt_msgs = MOCK_INPUT_KEY_TO_PROMPTS.get(key, key)
                    if isinstance(prompt_msgs, list):
                        prompt_msgs = [msg() if callable(msg) else msg for msg in prompt_msgs]
                    if prompt in prompt_msgs:
                        if callable(val):
                            response = val()
                        else:
                            response = val
                        break
                if response is None:
                    raise ValueError('Mock input for %r not found.' % prompt)
                return response

            old_getpass = createsuperuser.getpass
            old_input = builtins.input
            createsuperuser.getpass = mock_getpass
            builtins.input = mock_input
            try:
                test_func(*args)
            finally:
                createsuperuser.getpass = old_getpass
                builtins.input = old_input
        return wrapped
    return inner


class MockTTY:
    """
    A fake stdin object that pretends to be a TTY to be used in conjunction
    with mock_inputs.
    """
    def isatty(self):
        return True


class GetDefaultUsernameTestCase(TestCase):
    def test_simple(self) -> None:
        self.assertEqual(management.get_default_username(), '')

    # TODO: Add tests.
    #   See: https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L104-L139


class CreatesuperuserManagementCommandTestCase(TestCase):
    """
    Example tests:
        - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L253-L1036
        - https://github.com/django/django/blob/3.2/tests/auth_tests/test_management.py#L1039-L1088
    """
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

    def test_no_email_argument(self):
        new_io = StringIO()
        with self.assertRaisesMessage(CommandError, 'You must use --email_address with --noinput.'):
            call_command('createsuperuser', interactive=False, stdout=new_io)

    def test_skip_if_not_in_TTY(self):
        """
        If the command is not called from a TTY, it should be skipped and a
        message should be displayed
        """

        class FakeStdin:
            """A fake stdin object that has isatty() return False."""

            def isatty(self):
                return False

        out = StringIO()
        call_command(
            "createsuperuser",
            stdin=FakeStdin(),
            stdout=out,
            interactive=True,
        )

        self.assertEqual(User._default_manager.count(), 0)
        self.assertIn("Superuser creation skipped", out.getvalue())

    def test_interactive_basic_usage(self):
        @mock_inputs({
            'email_address': 'new_user@somewhere.org',
            'password': 'nopasswd',
        })
        def createsuperuser():
            new_io = StringIO()
            call_command(
                "createsuperuser",
                interactive=True,
                stdout=new_io,
                stdin=MockTTY(),
            )
            self.assertEqual(new_io.getvalue().strip(), 'Superuser created successfully.')

        createsuperuser()

        users = User.objects.filter(email_address="new_user@somewhere.org")
        self.assertEqual(users.count(), 1)

    def test_basic_usage_with_require_fields(self):
        @mock_inputs({
            'email_address': 'admin@somewhere.org',
            'password': 'nopasswd',
            'is_active': False,
        })
        def createsuperuser():
            new_io = StringIO()
            call_command(
                "createsuperuser",
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            command_output = new_io.getvalue().strip()
            self.assertEqual(command_output, 'Superuser created successfully.')

        with mock.patch.object(
            User,
            'REQUIRED_FIELDS',
            ['is_active'],
        ):
            createsuperuser()
        user = User.objects.get(email_address="admin@somewhere.org")
        self.assertFalse(user.is_active)

    def test_unique_usermane_validation(self):
        new_io = StringIO()
        # Create user with email address 'new_user@somewhere'.
        call_command(
            "createsuperuser",
            interactive=False,
            email_address="fake_email@somewhere.org",
            stdout=new_io,
        )

        # The first two email_address duplicated emails, but the third is a valid one.
        entered_emails = [
            "fake_email@somewhere.org",
            "fake_email@somewhere.org",
            "other_email@somewhere.org",
        ]

        def duplicated_emails_then_valid():
            return entered_emails.pop(0)

        @mock_inputs({
            'email_address': duplicated_emails_then_valid,
            'password': 'nopasswd',
        })
        def createsuperuser():
            std_out = StringIO()
            call_command(
                "createsuperuser",
                interactive=True,
                stdin=MockTTY(),
                stderr=std_out,
                stdout=std_out,
            )
            self.assertEqual(
                std_out.getvalue().strip(),
                "Error: That email address is already taken.\n"
                "Error: That email address is already taken.\n"
                "Superuser created successfully."
            )

        createsuperuser()

        users_1 = User.objects.filter(email_address="fake_email@somewhere.org")
        users_2 = User.objects.filter(email_address="other_email@somewhere.org")
        self.assertEqual(users_1.count(), 1)
        self.assertEqual(users_2.count(), 1)

    def test_invalid_username(self):
        """Creation fails if the username fails validation."""
        user_field = User._meta.get_field(User.USERNAME_FIELD)
        new_io = StringIO()
        entered_passwords = ['password', 'password', 'password']
        # Enter an invalid (too long) username first,
        # an invalid email address
        # and then a valid username.
        invalid_username = ('x' * user_field.max_length) + '@test.com'
        entered_usernames = [invalid_username, 'not_email', 'validEmail@test.com']

        def return_passwords():
            return entered_passwords.pop(0)

        def return_usernames():
            return entered_usernames.pop(0)

        @mock_inputs({'password': return_passwords, 'email_address': return_usernames})
        def test(self):
            call_command(
                'createsuperuser',
                interactive=True,
                email_address="not_email",
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            self.assertEqual(
                new_io.getvalue().strip(),
                'Enter a valid email address.\n'
                'Error: Ensure this value has at most %s characters (it has %s).\n'
                'Error: Enter a valid email address.\n'
                'Superuser created successfully.' % (user_field.max_length, len(invalid_username))
            )

        test(self)

    def test_blank_username_non_interactive(self):
        new_io = StringIO()
        with self.assertRaisesMessage(CommandError, 'Email address cannot be blank.'):
            call_command(
                'createsuperuser',
                email_address='',
                interactive=False,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )

    def test_blank_username(self):
        """Creation fails if --username is blank."""
        new_io = StringIO()
        with self.assertRaisesMessage(CommandError, 'Email address cannot be blank.'):
            call_command(
                'createsuperuser',
                email_address='',
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )

    def test_non_interactive_user_missing_required_field(self):
        """
        A Custom superuser won't be created when a required field isn't provided
        """
        # We can use the management command to create a superuser
        # We skip validation because the temporary substitution of the
        # swappable User model messes with validation.
        new_io = StringIO()
        with self.assertRaisesMessage(CommandError, 'You must use --is_active with --noinput.'):
            with mock.patch.object(
                User,
                'REQUIRED_FIELDS',
                ['is_active'],
            ):
                call_command(
                    "createsuperuser",
                    email_address="admin_user@somewhere.org",
                    interactive=False,
                    stdout=new_io,
                    stderr=new_io,
                )

        self.assertEqual(User._default_manager.count(), 0)

    def test_user_missing_required_field(self):
        """
        A Custom superuser won't be created when a required field isn't provided
        """
        entered_is_active_field = ['', True]

        def return_is_active():
            return entered_is_active_field.pop(0)

        @mock_inputs({
            'email_address': 'admin@somewhere.org',
            'password': 'nopasswd',
            'is_active': return_is_active,
        })
        def createsuperuser():
            new_io = StringIO()
            call_command(
                "createsuperuser",
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            command_output = new_io.getvalue().strip()
            self.assertEqual(
                command_output,
                "Error: “” value must be either True or False.\n"
                "Superuser created successfully."
            )

        with mock.patch.object(
            User,
            'REQUIRED_FIELDS',
            ['is_active'],
        ):
            createsuperuser()
        user = User.objects.get(email_address="admin@somewhere.org")
        self.assertTrue(user.is_active)

    def test_validation_blank_password_entered(self):
        """
        Creation should fail if the user enters blank passwords.
        """
        new_io = StringIO()

        # The first two passwords are empty strings, but the second two are
        # valid.
        entered_passwords = ["", "", "password2", "password2"]

        def blank_passwords_then_valid():
            return entered_passwords.pop(0)

        @mock_inputs({
            'password': blank_passwords_then_valid,
            'email_address': 'new_user@somewhere.org',
        })
        def test(self):
            call_command(
                "createsuperuser",
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            self.assertEqual(
                new_io.getvalue().strip(),
                "Error: Blank passwords aren't allowed.\n"
                "Superuser created successfully."
            )

        test(self)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ])
    def test_password_validation_bypass(self):
        """
        Password validation can be bypassed by entering 'y' at the prompt.
        """
        new_io = StringIO()

        @mock_inputs({
            'email_address': 'joe@example.com',
            'password': '1234567890',
            'bypass': 'y',
        })
        def test(self):
            call_command(
                'createsuperuser',
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            self.assertEqual(
                new_io.getvalue().strip(),
                'This password is entirely numeric.\n'
                'Superuser created successfully.'
            )

        test(self)

    def test_validation_mismatched_passwords(self):
        """
        Creation should fail if the user enters mismatched passwords.
        """
        new_io = StringIO()

        # The first two passwords do not match, but the second two do match and
        # are valid.
        entered_passwords = ["password", "not password", "password2", "password2"]

        def mismatched_passwords_then_matched():
            return entered_passwords.pop(0)

        @mock_inputs({
            'password': mismatched_passwords_then_matched,
            'email_address': 'fake_email@somewhere.com',
        })
        def test(self):
            call_command(
                "createsuperuser",
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
            self.assertEqual(
                new_io.getvalue().strip(),
                "Error: Your passwords didn't match.\n"
                "Superuser created successfully."
            )

        test(self)

    @mock_inputs({'email_address': 'KeyboardInterrupt'})
    def test_keyboard_interrupt(self):
        new_io = StringIO()
        with self.assertRaises(SystemExit):
            call_command(
                'createsuperuser',
                interactive=True,
                stdin=MockTTY(),
                stdout=new_io,
                stderr=new_io,
            )
        self.assertEqual(new_io.getvalue(), '\nOperation cancelled.\n')
