from django.core.validators import validate_email
from django.test import TestCase

from fd_dj_accounts.models import User

from .factories import create_user, generate_email_address


class FunctionsTestCase(TestCase):

    def test_generate_email_address(self):  # type: ignore
        email1 = generate_email_address()
        email2 = generate_email_address()

        validate_email(email1)
        validate_email(email2)
        self.assertRegex(email1, r'user-[0-9\.]*@example\.com')
        self.assertNotEqual(email1, email2)

    def test_create_user_default(self):  # type: ignore
        user_ = create_user()
        user = User.objects.get(pk=user_.pk)

        validate_email(user.get_username())
        self.assertTrue(user.check_password(user.email_address + 'XveRQfEh'))

        # Default user attributes.
        self.assertTrue(user.is_active)
        self.assertIsNone(user.deactivated_at)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # no validation errors should be raised
        user.full_clean()

    def test_create_user_custom(self):  # type: ignore
        email_address = 'hello@abc.com'
        password = 'my Password'

        user_ = create_user(
            email_address=email_address,
            password=password,
        )
        user = User.objects.get(pk=user_.pk)

        validate_email(user.get_username())
        self.assertEqual(user.email_address, email_address)
        self.assertTrue(user.check_password(password))

        # Default user attributes.
        self.assertTrue(user.is_active)
        self.assertIsNone(user.deactivated_at)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # no validation errors should be raised
        user.full_clean()
