from django.test.utils import CaptureQueriesContext
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.db import connection

from articles.models import Article
from users.test.factory import user_factory
from yoga_journeys.models import YogaJourney
from yoga_lessons.models import JourneyActiveYogaLesson
from yoga_lessons.tests.factory import yoga_lesson_factory
from yoga_practices.tests.yoga_practice_factory import yoga_practice_factory

start_yoga_lesson = """
mutation startYogaLesson($yogaLessonId: String!) {
  startYogaLesson(yogaLessonId: $yogaLessonId){
    ok
  }
}
"""


complete_yoga_lesson_step = """
mutation completeYogaLessonStep($yogaLessonId: String!, $yogaLessonStepId: String!) {
  completeYogaLessonStep(yogaLessonId: $yogaLessonId, yogaLessonStepId: $yogaLessonStepId){
    ok
  }
}
"""

query_yoga_lesson = """
query yogaLesson($id: String!) {
  yogaLesson(id: $id) {
    id
    activeYogaLesson {
      completedLessonSteps {
        __typename
        ...on YogaLessonArticleStepNode {
          id
          article {
            id
          }
        }
        ...on YogaLessonPracticeStepNode {
          id
          yogaPractice {
            id
          }
        }
      }
    }
  }
}
"""

query_yoga_lessons = """
query yogaLessons {
  yogaLessons {
    edges {
      node {
        title
        activeYogaLesson {
          createdAt
        }
      }
    }
  }
}
"""


class YogaJourneysLessonAPITestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.user = user_factory()
        self.client.authenticate(self.user)

    def get_yoga_journey(self):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=self.user)
        return yoga_journey

    def test_start_yoga_lesson(self):
        yoga_lesson = yoga_lesson_factory()

        response = self.client.execute(
            start_yoga_lesson,
            {"yogaLessonId": str(yoga_lesson.id)},
        )

        self.assertTrue(response.data["startYogaLesson"]["ok"])
        active_lessons = self.get_yoga_journey().active_yoga_lessons.filter()
        self.assertTrue(active_lessons.count() == 1)
        self.assertTrue(active_lessons[0].id == yoga_lesson.id)

    def test_complete_yoga_lesson_step(self):
        yoga_practice1, yoga_practice2 = yoga_practice_factory(), yoga_practice_factory()
        article = Article.objects.create(title="Fake Article", content_items=dict(items=[]))

        # Prepare -- Create a yoga lesson
        yoga_lesson = yoga_lesson_factory(steps=[yoga_practice1, article, yoga_practice2])
        self.client.execute(
            start_yoga_lesson,
            {"yogaLessonId": str(yoga_lesson.id)},
        )

        steps = list(yoga_lesson.steps.all())

        response = self.client.execute(
            complete_yoga_lesson_step,
            {"yogaLessonId": str(yoga_lesson.id), "yogaLessonStepId": str(steps[0].id)},
        )

        self.assertTrue(response.data["completeYogaLessonStep"]["ok"])
        journey_active_lesson = JourneyActiveYogaLesson.objects.get(yoga_lesson=yoga_lesson)
        completed_step_ids = list(journey_active_lesson.completed_lesson_steps.all().values_list("id", flat=True))

        self.assertTrue(steps[0].id in completed_step_ids)
        self.assertTrue(steps[1].id not in completed_step_ids)
        self.assertTrue(steps[2].id not in completed_step_ids)
        self.assertTrue(yoga_practice_factory().id not in completed_step_ids)

    def test_query_yoga_lesson(self):
        yoga_practice1, yoga_practice2 = yoga_practice_factory(), yoga_practice_factory()
        article = Article.objects.create(title="Fake Article", content_items=dict(items=[]))

        # Prepare -- Create a yoga lesson
        yoga_lesson = yoga_lesson_factory(steps=[yoga_practice1, article, yoga_practice2])
        self.client.execute(
            start_yoga_lesson,
            {"yogaLessonId": str(yoga_lesson.id)},
        )

        steps = list(yoga_lesson.steps.all())

        # Prepare -- Complete the first 2 steps
        for step in steps[:2]:
            self.client.execute(
                complete_yoga_lesson_step,
                {"yogaLessonId": str(yoga_lesson.id), "yogaLessonStepId": str(step.id)},
            )

        response = self.client.execute(
            query_yoga_lesson,
            {"id": str(yoga_lesson.id)},
        )
        completed_steps_response = response.data["yogaLesson"]["activeYogaLesson"]["completedLessonSteps"]
        self.assertEqual(len(completed_steps_response), 2)

        self.assertEqual(completed_steps_response[0]["id"], str(steps[0].id))
        self.assertEqual(completed_steps_response[0]["yogaPractice"]["id"], str(yoga_practice1.id))

        self.assertEqual(completed_steps_response[1]["id"], str(steps[1].id))
        self.assertEqual(completed_steps_response[1]["article"]["id"], str(article.id))

    def test_yoga_lessons_db_hit_count(self):
        yoga_lessons = [yoga_lesson_factory(title=f"fake-lesson-{i}") for i in range(30)]
        for i, yoga_lesson in enumerate(yoga_lessons):
            if i % 2 == 0:
                self.client.execute(
                    start_yoga_lesson,
                    {"yogaLessonId": str(yoga_lesson.id)},
                )
        with CaptureQueriesContext(connection) as context:
            self.client.execute(query_yoga_lessons)
            # DB queries are for: 1. User, 2. Yoga Lessons, 3. Attached active yoga lessons
            self.assertEqual(len(context.captured_queries), 3)
