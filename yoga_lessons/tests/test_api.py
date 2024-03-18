from graphql_jwt.testcases import JSONWebTokenTestCase

from articles.models import Article, ArticleTextContentItem, ArticleImageContentItem
from users.test.factory import user_factory
from yoga_lessons.tests.factory import yoga_lesson_factory
from yoga_practices.tests.yoga_practice_factory import yoga_practice_factory

query_yoga_lessons = """
query yogaLessons {
  yogaLessons {
    edges {
      node {
        steps {
          __typename
          ... on YogaLessonPracticeStepNode {
            yogaPractice {
              id
              title
            }
          }
          ... on YogaLessonArticleStepNode {
            article {
              id
              contentItems {
                __typename
                ... on ArticleTextContentItemNode {
                  content
                }
                ... on ArticleImageContentItemNode {
                  imageUrl
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


class YogaLessonAPITestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.user = user_factory()
        self.client.authenticate(self.user)

    def test_query_yoga_lesson_steps(self):
        yoga_practice1, yoga_practice2 = yoga_practice_factory(), yoga_practice_factory()
        article = Article.objects.create(title="Fake Article", content_items=dict(items=[]))

        # Prepare -- Create a yoga lesson
        yoga_lesson_factory(steps=[yoga_practice1, article, yoga_practice2])

        response = self.client.execute(query_yoga_lessons)

        # Assert - Make sure all the steps are returned properly
        self.assertEqual(len(response.data["yogaLessons"]["edges"]), 1)
        steps_response = response.data["yogaLessons"]["edges"][0]["node"]["steps"]

        # Assert - No extra steps
        self.assertEqual(len(steps_response), 3)

        # Assert -- YogaPractice1
        self.assertEqual(steps_response[0]["__typename"], "YogaLessonPracticeStepNode")
        self.assertEqual(steps_response[0]["yogaPractice"]["id"], str(yoga_practice1.id))

        # Assert -- Article
        self.assertEqual(steps_response[1]["__typename"], "YogaLessonArticleStepNode")
        self.assertEqual(steps_response[1]["article"]["id"], str(article.id))
        self.assertIsNotNone(steps_response[1]["article"]["contentItems"])

        # Assert -- YogaPractice2
        self.assertEqual(steps_response[2]["__typename"], "YogaLessonPracticeStepNode")
        self.assertEqual(steps_response[2]["yogaPractice"]["id"], str(yoga_practice2.id))

    def test_query_yoga_lesson_steps__article(self):
        article = Article.objects.create(
            title="Fake Article",
            content_items=dict(
                items=[
                    ArticleTextContentItem(type="text", content="Some Content"),
                    ArticleImageContentItem(type="image", image_url="https://www.fakedomain.com"),
                ]
            ),
        )

        # Prepare -- Create a yoga lesson with complex article
        yoga_lesson_factory(steps=[article])

        response = self.client.execute(query_yoga_lessons)

        # Assert - Make sure all the steps are returned properly
        self.assertEqual(len(response.data["yogaLessons"]["edges"]), 1)
        steps_response = response.data["yogaLessons"]["edges"][0]["node"]["steps"]

        # Assert - No extra steps
        self.assertEqual(len(steps_response), 1)

        article_response = steps_response[0]["article"]
        self.assertEqual(article_response["id"], str(article.id))

        # Assert - No extra article content items
        self.assertEqual(len(article_response["contentItems"]), 2)

        # Assert -- Text content
        self.assertEqual(article_response["contentItems"][0]["__typename"], "ArticleTextContentItemNode")
        self.assertEqual(article_response["contentItems"][0]["content"], article.content_items.items[0].content)

        # Assert -- Image content
        self.assertEqual(article_response["contentItems"][1]["__typename"], "ArticleImageContentItemNode")
        self.assertEqual(article_response["contentItems"][1]["imageUrl"], article.content_items.items[1].image_url)
