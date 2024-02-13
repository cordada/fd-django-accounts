from django.contrib.auth import signals
from django.test import TestCase
from django.test.client import RequestFactory
from fd_dj_accounts.models import User


class SignalTestCase(TestCase):

    def test_update_last_login(self) -> None:
        """Only `last_login` is updated in `update_last_login`"""
        user = User.objects.create_user(email_address='staff@a.com', password='password')
        self.assertIsNone(user.last_login)

        request = RequestFactory().get('/login')
        signals.user_logged_in.send(sender=user.__class__, request=request, user=user)
        self.assertIsNotNone(user.last_login)

        old_last_login = user.last_login
        request = RequestFactory().get('/login')
        signals.user_logged_in.send(sender=user.__class__, request=request, user=user)
        user.refresh_from_db()

        self.assertEqual(user.get_username(), 'staff@a.com')
        self.assertGreater(user.last_login, old_last_login)
