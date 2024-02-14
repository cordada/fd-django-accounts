from typing import Any
import uuid

import django.test.signals
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import MD5PasswordHasher
from django.core.signals import setting_changed
from django.test import TestCase, override_settings

from fd_dj_accounts.auth_backends import AuthUserModelAuthBackend
from . import utils


# warning: this is critical for being able to mess with 'AUTH_USER_MODEL' in the tests.
setting_changed.disconnect(receiver=django.test.signals.user_model_swapped)
setting_changed.connect(receiver=utils.auth_user_model_swapped_receiver)


class CountingMD5PasswordHasher(MD5PasswordHasher):
    """Hasher that counts how many times it computes a hash."""

    calls = 0

    def encode(self, *args, **kwargs):  # type: ignore
        type(self).calls += 1
        return super().encode(*args, **kwargs)


class AuthUserModelAuthBackendTestMixin:

    """
    Base class for test cases of ``AuthUserModelAuthBackend``.

    Validate the authentication backend with a test class per different user
    model subclass of :class:`django.contrib.auth.base_user.AbstractBaseUser`.

    Each test case class must:
    - Set class attr ``non_existent_user_id`` to a valid value for the
      corresponding user model field ``id``, which depends on type of the
      field.
    - Define a method ``create_users() to create two users for test purposes.

    """

    non_existent_user_id: Any = None

    @classmethod
    def setUpClass(cls):  # type: ignore
        super().setUpClass()  # type: ignore  # mypy issue 246
        cls.UserModel = get_user_model()

        if cls.non_existent_user_id is None:
            raise Exception("Remember to set the class attr 'non_existent_user_id'.")

    def setUp(self):  # type: ignore
        self.create_users()

    @override_settings(
        PASSWORD_HASHERS=['tests.test_auth_backends.CountingMD5PasswordHasher'])  # type: ignore  # noqa: E501
    def test_authentication_timing(self):  # type: ignore
        """Hasher is run once regardless of whether the user exists. Refs #20760."""
        # Re-set the password, because this tests overrides PASSWORD_HASHERS
        self.user1.set_password('test')
        self.user1.save()

        CountingMD5PasswordHasher.calls = 0
        username = self.user1.get_username()
        authenticate(username=username, password='test')
        self.assertEqual(CountingMD5PasswordHasher.calls, 1)

        CountingMD5PasswordHasher.calls = 0
        authenticate(username='no_such_user@example.com', password='test')
        self.assertEqual(CountingMD5PasswordHasher.calls, 1)

    def test_authenticate_inactive(self):  # type: ignore
        self.assertEqual(authenticate(**self.user1_credentials), self.user1)
        self.user1.is_active = False
        self.user1.save()
        self.assertIsNone(authenticate(**self.user1_credentials))

    def test_authenticate(self):  # type: ignore
        self.assertEqual(authenticate(**self.user2_credentials), self.user2)

    def test_authenticate_with_USERNAME_FIELD(self):  # type: ignore
        self.user2_credentials[self.user2.USERNAME_FIELD] = self.user2_credentials.pop('username')
        self.assertEqual(authenticate(**self.user2_credentials), self.user2)

    def test_authenticate_bad_password(self):  # type: ignore
        self.user2_credentials['password'] = 'bad-password'
        self.assertIsNone(authenticate(**self.user2_credentials))

    def test_authenticate_bad_username_field(self):  # type: ignore
        self.user2_credentials['username_x'] = self.user2_credentials.pop('username')
        self.assertIsNone(authenticate(**self.user2_credentials))

    def test_get_user(self):  # type: ignore
        backend = AuthUserModelAuthBackend()
        self.assertEqual(backend.get_user(self.user1.id), self.user1)

    def test_get_user_pk_str(self):  # type: ignore
        backend = AuthUserModelAuthBackend()
        self.assertEqual(backend.get_user(str(self.user1.id)), self.user1)

    def test_get_user_inactive(self):  # type: ignore
        backend = AuthUserModelAuthBackend()
        self.assertEqual(backend.get_user(self.user1.id), self.user1)

        self.user1.is_active = False
        self.user1.save()
        self.assertFalse(backend.user_can_authenticate(self.user1))
        self.assertIsNone(backend.get_user(self.user1.id))

    def test_get_user_does_not_exist(self):  # type: ignore
        backend = AuthUserModelAuthBackend()
        self.assertIsNone(backend.get_user(user_id=self.non_existent_user_id))


@override_settings(
    AUTHENTICATION_BACKENDS=['fd_dj_accounts.auth_backends.AuthUserModelAuthBackend'],
    AUTH_USER_MODEL='fd_dj_accounts.User',
)
class FdDjAccountsAuthUserModelAuthBackendTest(AuthUserModelAuthBackendTestMixin, TestCase):

    non_existent_user_id = uuid.uuid4()

    def create_users(self):  # type: ignore
        self.user1_credentials = {'username': 'test@example.com', 'password': 'test'}
        self.user2_credentials = {'username': 'test2@example.com', 'password': 'test'}

        self.user1 = self.UserModel.objects.create_user(
            email_address=self.user1_credentials['username'],
            password=self.user1_credentials['password'],
        )
        self.user2 = self.UserModel.objects.create_user(
            email_address=self.user2_credentials['username'],
            password=self.user2_credentials['password'],
        )


# TODO: test the backend with the default auth user model 'django.contrib.auth.models.User'.
#   This is not terribly complicated by itself, but the test setup needs to be different, something
#   more similar to how a 3rd-party package is tested, not how a Django project is tested.
#   Why? Because that app's models tables need to be created, which happens at the beggining of the
#   execution of the Django test suite, which means 'django.contrib.auth' must be in
#   'INSTALLED_APPS' from the very beginning, instead of being added to it when the specific test
#   case is run.
#
# from django.test import TestCase, modify_settings, override_settings
#
# @override_settings(
#     AUTHENTICATION_BACKENDS=['fd_dj_accounts.auth_backends.AuthUserModelAuthBackend'],
#     AUTH_USER_MODEL='auth.User',
# )
# @modify_settings(
#     INSTALLED_APPS={
#         'prepend': ['django.contrib.auth', 'django.contrib.contenttypes'],
#         'remove': 'fd_dj_accounts',
#     },
# )
# class StandardUserModelAuthBackendTest(AuthUserModelAuthBackendTestMixin, TestCase):
#
#     def create_users(self):  # type: ignore
#         self.user1_credentials = {'username': 'test@example.com', 'password': 'test'}
#         self.user2_credentials = {'username': 'test2@example.com', 'password': 'test'}
#
#         self.user1 = self.UserModel.objects.create_user(
#             username=self.user1_credentials['username'],
#             password=self.user1_credentials['password'],
#         )
#         self.user2 = self.UserModel.objects.create_user(
#             username=self.user2_credentials['username'],
#             password=self.user2_credentials['password'],
#         )
