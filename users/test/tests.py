from django.contrib.auth import authenticate
from django.test import TestCase

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
