from django.test import SimpleTestCase, TestCase

from fd_dj_accounts.models import AnonymousUser, User, UserManager, get_or_create_system_user


class FunctionsTestCase(TestCase):

    def test_get_or_create_system_user(self):  # type: ignore
        from django.conf import settings

        system_user_email_address = settings.APP_ACCOUNTS_SYSTEM_USERNAME
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email_address=system_user_email_address)

        system_user = get_or_create_system_user()
        self.assertEqual(system_user.created_by, system_user)
        self.assertEqual(system_user.email_address, system_user_email_address)
        self.assertEqual(get_or_create_system_user(), system_user)


class NaturalKeysTestCase(TestCase):

    def test_user_natural_key(self):  # type: ignore
        staff_user = User.objects.create_user(email_address='staff@example.com')
        self.assertEqual(User.objects.get_by_natural_key('staff@example.com'), staff_user)
        self.assertEqual(staff_user.natural_key(), ('staff@example.com',))


class LoadDataWithoutNaturalKeysTestCase(TestCase):
    fixtures = ['regular.json']

    def test_user_is_created(self):  # type: ignore
        user = User.objects.get(email_address='email@example.com')
        self.assertEqual(user, User.objects.get(email_address='email@example.com'))


class UserManagerTestCase(TestCase):

    def test_create_user(self):  # type: ignore
        user1_email_address = 'user1@normal.com'
        user1 = User.objects.create_user(user1_email_address)
        self.assertEqual(user1.email_address, user1_email_address)
        self.assertEqual(user1.get_username(), user1_email_address)
        self.assertFalse(user1.has_usable_password())

        user2_email_address = 'user2@normal.com'
        user2 = User.objects.create_user(user2_email_address, created_by=user1)
        self.assertEqual(user2.email_address, user2_email_address)
        self.assertEqual(user2.get_username(), user2_email_address)
        self.assertFalse(user2.has_usable_password())

    def test_empty_username(self):  # type: ignore
        with self.assertRaisesMessage(ValueError, 'The given email address must be set'):
            User.objects.create_user(email_address='')

    def test_create_user_is_staff(self):  # type: ignore
        email_address = 'normal@normal.com'
        user = User.objects.create_user(email_address, is_staff=True)
        self.assertEqual(user.email_address, email_address)
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):  # type: ignore
        email_address = 'superuser@test.com'
        user = User.objects.create_superuser(email_address, password='test')
        self.assertEqual(user.email_address, email_address)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_super_user_raises_error_on_false_is_superuser(self):  # type: ignore
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(
                email_address='test@test.com',
                password='test', is_superuser=False,
            )

    def test_create_superuser_raises_error_on_false_is_staff(self):  # type: ignore
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(
                email_address='test@test.com',
                password='test', is_staff=False,
            )


class UserTestCase(TestCase):

    def test_model_manager(self):  # type: ignore
        self.assertIsInstance(User.objects, UserManager)

    def test_clean_normalize_email_address_as_username(self):  # type: ignore
        # Unicode characters that look the same but are different ones.
        email_address_original_ohm = 'iamtheΩ@example.com'  # U+2126 OHM SIGN
        email_address_normalized_omega = 'iamtheΩ@example.com'  # U+03A9 GREEK CAPITAL LETTER OMEGA

        user = User(email_address=email_address_original_ohm)

        # Apply normalization.
        user.clean()
        email_address = user.get_username()
        self.assertNotEqual(email_address, email_address_original_ohm)
        self.assertEqual(email_address, email_address_normalized_omega)

    def test_user_clean_normalize_email(self):  # type: ignore
        user = User(email_address='foo@BAR.com')
        user.clean()
        self.assertEqual(user.email_address, 'foo@bar.com')

    def test_default_email(self):  # type: ignore
        user = User()
        self.assertEqual(user.get_email_field_name(), 'email_address')

    def test_created_by(self):  # type: ignore
        user_creator = User.objects.create_user(email_address='user_creator@example.com')
        user = User(email_address='user@example.com', created_by=user_creator)
        user.set_password('foo')
        user.save()
        self.assertEqual(user.created_by, user_creator)

        # Test field attribute 'related_name'.
        self.assertListEqual(list(user_creator.users_created.all()), [user])

    def test_deactivate(self):  # type: ignore
        user_creator = User.objects.create_user(email_address='user_creator@example.com')
        user = User(email_address='foo@BAR.com', created_by=user_creator)
        # note: need to set a password or 'full_clean()' raises a ValidationError.
        user.set_password('foo')
        user.save()

        self.assertTrue(user.is_active)
        self.assertIsNone(user.deactivated_at)

        user.deactivate()

        user.refresh_from_db()
        self.assertFalse(user.is_active)
        deactivated_at_1 = user.deactivated_at
        self.assertIsNotNone(user.deactivated_at)

        user.deactivate()

        user.refresh_from_db()
        self.assertFalse(user.is_active)
        deactivated_at_2 = user.deactivated_at
        self.assertEqual(deactivated_at_1, deactivated_at_2)


class IsActiveTestCase(TestCase):
    """
    Tests the behavior of the guaranteed is_active attribute
    """

    def test_builtin_user_isactive(self):  # type: ignore
        user_creator = User.objects.create_user(email_address='user_creator@example.com')
        user = User(email_address='foo@bar.com', created_by=user_creator)
        # is_active is true by default
        self.assertIs(user.is_active, True)
        user.is_active = False
        # note: need to set a password or 'full_clean()' raises a ValidationError.
        user.set_unusable_password()
        user.save()
        user_fetched = User.objects.get(pk=user.pk)
        # the is_active flag is saved
        self.assertFalse(user_fetched.is_active)


class AnonymousUserTests(SimpleTestCase):
    no_repr_msg = "Django doesn't provide a DB representation for AnonymousUser."

    def setUp(self):  # type: ignore
        self.user = AnonymousUser()

    def test_properties(self):  # type: ignore
        self.assertIsNone(self.user.pk)
        self.assertEqual(self.user.email_address, '')
        self.assertEqual(self.user.get_username(), '')
        self.assertIs(self.user.is_anonymous, True)
        self.assertIs(self.user.is_authenticated, False)
        self.assertIs(self.user.is_staff, False)
        self.assertIs(self.user.is_active, False)
        self.assertIs(self.user.is_superuser, False)

    def test_str(self):  # type: ignore
        self.assertEqual(str(self.user), 'AnonymousUser')

    def test_eq(self):  # type: ignore
        self.assertEqual(self.user, AnonymousUser())
        self.assertNotEqual(self.user, User('super', 'super@example.com', 'super'))

    def test_hash(self):  # type: ignore
        self.assertEqual(hash(self.user), 1)

    def test_delete(self):  # type: ignore
        with self.assertRaisesMessage(NotImplementedError, self.no_repr_msg):
            self.user.delete()

    def test_save(self):  # type: ignore
        with self.assertRaisesMessage(NotImplementedError, self.no_repr_msg):
            self.user.save()

    def test_set_password(self):  # type: ignore
        with self.assertRaisesMessage(NotImplementedError, self.no_repr_msg):
            self.user.set_password('password')

    def test_check_password(self):  # type: ignore
        with self.assertRaisesMessage(NotImplementedError, self.no_repr_msg):
            self.user.check_password('password')

    def test_deactivate(self):  # type: ignore
        with self.assertRaisesMessage(NotImplementedError, self.no_repr_msg):
            self.user.deactivate()
