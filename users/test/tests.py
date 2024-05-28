from datetime import timedelta

from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from users.models import PasswordResetVerification
from users.test.factory import user_factory


class UserTestCase(TestCase):
    def test_authentication(self):
        raw_password = "str0ngP4ssw0rd!"
        user = user_factory(password=raw_password)

        # Valid credentials
        self.assertIsNotNone(authenticate(email=user.email, password=raw_password))

        # Invalid credentials
        self.assertIsNone(authenticate(email=user.email, password="wrongpassword"))
        self.assertIsNone(authenticate(email="wrongemail@fake.com", password=raw_password))

class ResetPasswordTestCase(TestCase):
    def test_code_validation(self):
        user = user_factory()
        password_reset_verification = PasswordResetVerification.create_for_user(user)
        # Verify that the code is valid for the user
        self.assertTrue(PasswordResetVerification.is_code_valid(user, password_reset_verification.code))

    def test_expired_code(self):
        user = user_factory()
        now = timezone.now()
        with freeze_time(now):
            password_reset_verification = PasswordResetVerification.create_for_user(user)
            self.assertTrue(PasswordResetVerification.is_code_valid(user, password_reset_verification.code))
        with freeze_time(now + timedelta(minutes=5, seconds=1)):
            self.assertFalse(PasswordResetVerification.is_code_valid(user, password_reset_verification.code))

    def test_password_reset(self):
        user = user_factory()
        password_reset_verification = PasswordResetVerification.create_for_user(user)
        new_password = "newP4ssw0rd!"
        user.reset_password(new_password, password_reset_verification.code)
        self.assertTrue(user.check_password(new_password))
        self.assertFalse(PasswordResetVerification.objects.filter(id=password_reset_verification.id).exists())

        # Shouldn't be able to use the same code twice
        with self.assertRaises(PermissionError):
            user.reset_password(new_password, password_reset_verification.code)

    def test_password_reset__with_expired_code(self):
        user = user_factory()
        new_password = "newP4ssw0rd!"
        password_reset_verification = PasswordResetVerification.create_for_user(user)
        with freeze_time(timezone.now() + timedelta(minutes=5, seconds=1)):
            with self.assertRaises(PermissionError):
                user.reset_password(new_password, password_reset_verification.code)


