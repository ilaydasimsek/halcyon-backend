from django.core.exceptions import ValidationError
from django.test import TestCase

from articles.models import Article


class ArticleTestCase(TestCase):
    def test_valid_article_creation(self):
        inputs = [
            [],
            [{"type": "text", "content": "some content"}],
            [{"type": "image", "image_url": "https://www.fakedomain.com"}],
            [{"type": "text", "content": "some content"}, {"type": "image", "image_url": "https://www.fakedomain.com"}],
        ]
        # Assert -- Shouldn't raise exceptions
        for items in inputs:
            Article.objects.create(title="Fake Article Title", content_items={"items": items})

    def test_article_content_schema_errors(self):
        invalid_inputs = [
            [{"type": "text"}],  # No content,
            [{"type": "image"}],  # No image_url,
            [{"content": "some content"}],  # No type,
            [{"image_url": "some content"}],  # No image_url,
            [{"type": "text", "content": "some content"}, {"image_url": "some content"}],
            # One valid, one invalid element
        ]

        for items in invalid_inputs:
            with self.assertRaises(ValidationError):
                Article.objects.create(title="Fake Article Title", content_items={"items": items})
