from graphql_jwt.testcases import JSONWebTokenTestCase

from users.test.factory import user_factory
from yoga_journeys.models import YogaJourney
from yoga_practices.tests.yoga_practice_factory import yoga_practice_factory

complete_yoga_practice = """
mutation completeYogaPractice($yogaPracticeId: Int!) {
  completeYogaPractice(yogaPracticeId: $yogaPracticeId){
    ok
  }
}
"""

query_completed_yoga_practice = """
query journey {
  journey {
    completedYogaPractices {
      edges {
        node {
          yogaPractice {
            id
          }
        }
      }
    }
    uncompletedYogaPractices {
      edges {
        node {
          id
        }
      }
    }
  }
}
"""

delete_completed_yoga_practice = """
mutation deleteCompletedYogaPractice($yogaPracticeId: Int!) {
  deleteCompletedYogaPractice(yogaPracticeId: $yogaPracticeId){
    count
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

    def test_yoga_practice_completion(self):
        yoga_practice = yoga_practice_factory()

        response = self.client.execute(
            complete_yoga_practice,
            {"yogaPracticeId": yoga_practice.id},
        )

        self.assertTrue(response.data["completeYogaPractice"]["ok"])

        self.assertTrue(self.get_yoga_journey().completed_yoga_practices.filter(id=yoga_practice.id).exists())

    def test_yoga_practice_multiple_completion(self):
        yoga_practice = yoga_practice_factory()
        for i in range(10):
            response = self.client.execute(
                complete_yoga_practice,
                {"yogaPracticeId": yoga_practice.id},
            )

            self.assertTrue(response.data["completeYogaPractice"]["ok"])

        self.assertEqual(self.get_yoga_journey().completed_yoga_practices.filter(id=yoga_practice.id).count(), 10)

    def test_completed_uncompleted_yoga_practices_query(self):
        completed_practice_ids = []
        uncompleted_practice_ids = []
        for i in range(20):
            yoga_practice = yoga_practice_factory()
            if i % 2 == 0:
                completed_practice_ids.append(yoga_practice.id)
                self.client.execute(
                    complete_yoga_practice,
                    {"yogaPracticeId": yoga_practice.id},
                )
            else:
                uncompleted_practice_ids.append(yoga_practice.id)
        response = self.client.execute(query_completed_yoga_practice)
        completed_ids_response = [
            int(edge["node"]["yogaPractice"]["id"])
            for edge in response.data["journey"]["completedYogaPractices"]["edges"]
        ]
        self.assertEqual(set(completed_ids_response), set(completed_practice_ids))
        uncompleted_ids_response = [
            int(edge["node"]["id"]) for edge in response.data["journey"]["uncompletedYogaPractices"]["edges"]
        ]
        self.assertEqual(set(uncompleted_ids_response), set(uncompleted_practice_ids))

    def test_completed_yoga_practice_deletion(self):
        yoga_practice = yoga_practice_factory()
        yoga_journey = self.get_yoga_journey()
        yoga_journey.completed_yoga_practices.add(yoga_practice)
        response = self.client.execute(
            delete_completed_yoga_practice,
            {"yogaPracticeId": yoga_practice.id},
        )
        self.assertEqual(response.data["deleteCompletedYogaPractice"]["count"], 1)

    def test_non_existing_yoga_practice_deletion(self):
        response = self.client.execute(
            delete_completed_yoga_practice,
            {"yogaPracticeId": -1},
        )
        self.assertEqual(response.data["deleteCompletedYogaPractice"]["count"], 0)
