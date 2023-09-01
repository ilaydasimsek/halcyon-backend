from graphql_jwt.testcases import JSONWebTokenTestCase

from users.test.factory import user_factory
from yoga_journeys.models import YogaJourney, JourneyActiveYogaChallenge
from yoga_practices.tests.yoga_practice_factory import yoga_practice_factory, yoga_challenge_factory

start_yoga_challenge = """
mutation startYogaChallenge($yogaChallengeId: Int!) {
  startYogaChallenge(yogaChallengeId: $yogaChallengeId){
    ok
  }
}
"""


complete_yoga_challenge_practice = """
mutation completeYogaChallengePractice($yogaPracticeId: Int!, $yogaChallengeId: Int!) {
  completeYogaChallengePractice(yogaPracticeId: $yogaPracticeId, yogaChallengeId: $yogaChallengeId){
    ok
  }
}
"""


class YogaJourneysPracticeAPITestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.user = user_factory()
        self.client.authenticate(self.user)

    def get_yoga_journey(self):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=self.user)
        return yoga_journey

    def test_start_yoga_challenge(self):
        yoga_challenge = yoga_challenge_factory()

        response = self.client.execute(
            start_yoga_challenge,
            {"yogaChallengeId": yoga_challenge.id},
        )

        self.assertTrue(response.data["startYogaChallenge"]["ok"])
        self.assertTrue(self.get_yoga_journey().active_yoga_challenges.filter(id=yoga_challenge.id).exists())

    def test_complete_yoga_challenge_practice(self):
        yoga_challenge = yoga_challenge_factory(yoga_practice_count=2)
        self.client.execute(
            start_yoga_challenge,
            {"yogaChallengeId": yoga_challenge.id},
        )

        practices = list(yoga_challenge.practices.all())

        response = self.client.execute(
            complete_yoga_challenge_practice,
            {"yogaChallengeId": yoga_challenge.id, "yogaPracticeId": practices[0].id},
        )

        self.assertTrue(response.data["completeYogaChallengePractice"]["ok"])
        journey_active_challenge = JourneyActiveYogaChallenge.objects.get(yoga_challenge=yoga_challenge)
        completed_practice_ids = list(
            journey_active_challenge.completed_yoga_practices.all().values_list("id", flat=True)
        )

        self.assertTrue(practices[0].id in completed_practice_ids)
        self.assertTrue(practices[1].id not in completed_practice_ids)
        self.assertTrue(yoga_practice_factory().id not in completed_practice_ids)
