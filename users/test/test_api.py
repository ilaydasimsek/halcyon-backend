from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone
from freezegun import freeze_time
from graphql_jwt.testcases import JSONWebTokenTestCase

from users.models import User
from users.test.factory import user_factory
from yoga_journeys.models import YogaJourney
from yoga_lessons.models import JourneyActiveYogaLesson
from yoga_lessons.tests.factory import yoga_lesson_factory
from yoga_practices.models import JourneyActiveYogaChallenge, JourneyCompletedYogaPractice
from yoga_practices.tests.yoga_practice_factory import yoga_challenge_factory, yoga_practice_factory

login_mutation = """
mutation login($email: String!, $password: String!) {
  login(email: $email, password: $password){
    payload
    token
  }
}
"""

refresh_token_mutation = """
mutation refresh($token: String!) {
  refreshToken(token: $token) {
    payload
  }
}
"""

delete_account_mutation = """
mutation deleteAccount {
  deleteAccount {
    ok
  }
}
"""


class AuthAPITestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.password = "str0ngP4ssw0rd!"
        self.user = user_factory(password=self.password)
        self.client.authenticate(self.user)

    def decode_jwt(self, token):
        return jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])

    def test_login(self):
        valid_login_response = self.client.execute(
            login_mutation,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )
        token = valid_login_response.data["login"]["token"]

        self.assertEqual(self.decode_jwt(token)["email"], self.user.email, "JWT token should be decoded properly.")

        invalid_login_response = self.client.execute(
            login_mutation,
            {
                "email": self.user.email,
                "password": "wrongpassword",
            },
        )

        self.assertIsNone(invalid_login_response.data["login"], "Should have thrown an error.")

    def test_jwt_expiration(self):
        valid_login_response = self.client.execute(
            login_mutation,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )
        token = valid_login_response.data["login"]["token"]
        valid_time_delta = timedelta(minutes=4, seconds=50)
        with freeze_time(timezone.now() + valid_time_delta):
            self.assertEqual(self.decode_jwt(token)["email"], self.user.email, "JWT token should be decoded properly.")

        invalid_time_deltas = timedelta(minutes=5, seconds=1)
        with freeze_time(timezone.now() + invalid_time_deltas):
            with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
                self.decode_jwt(token)

    def test_refresh_token(self):
        valid_login_response = self.client.execute(
            login_mutation,
            {
                "email": self.user.email,
                "password": self.password,
            },
        )
        token = valid_login_response.data["login"]["token"]
        response = self.client.execute(refresh_token_mutation, {"token": token})

        self.assertEqual(
            response.data["refreshToken"]["payload"]["email"], self.user.email, "JWT token should be decoded properly."
        )

    def test_delete_account(self):
        journey = YogaJourney.objects.create(user=self.user)
        self.assertTrue(YogaJourney.objects.filter(user=self.user).exists())

        journey.start_yoga_lesson(yoga_lesson_id=yoga_lesson_factory().id)
        self.assertTrue(JourneyActiveYogaLesson.objects.filter(yoga_journey__user=self.user).exists())

        journey.start_yoga_challenge(yoga_challenge_id=yoga_challenge_factory().id)
        self.assertTrue(JourneyActiveYogaChallenge.objects.filter(yoga_journey__user=self.user).exists())

        journey.complete_yoga_practice(yoga_practice_id=yoga_practice_factory().id)
        self.assertTrue(JourneyCompletedYogaPractice.objects.filter(yoga_journey__user=self.user).exists())

        user_id = self.user.id
        response = self.client.execute(delete_account_mutation)
        self.assertTrue(response.data["deleteAccount"]["ok"])

        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(YogaJourney.objects.filter(user_id=user_id).exists())
        self.assertFalse(JourneyActiveYogaLesson.objects.filter(yoga_journey__user_id=user_id).exists())
        self.assertFalse(JourneyActiveYogaChallenge.objects.filter(yoga_journey__user_id=user_id).exists())
        self.assertFalse(JourneyCompletedYogaPractice.objects.filter(yoga_journey__user_id=user_id).exists())
