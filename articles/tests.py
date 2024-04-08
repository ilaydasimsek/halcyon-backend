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
            [{"type": "header", "title": "header title"}, {"type": "image", "image_url": "https://www.fakedomain.com"}],
        ]
        # Assert -- Shouldn't raise exceptions
        for index, items in enumerate(inputs):
            Article.objects.create(title=f"Fake Article Title {index}", content_items={"items": items})

    def test_article_content_schema_errors(self):
        invalid_inputs = [
            [{"type": "text"}],  # No content,
            [{"type": "image"}],  # No image_url,
            [{"content": "some content"}],  # No type,
            [{"type": "header"}],  # No title,
            [{"type": "text", "content": "x", "extra_field": 1}],  # Extra content,
            [{"type": "text", "content": "some content"}, {"image_url": "some content"}],
            # One valid, one invalid element
        ]

        for index, items in enumerate(invalid_inputs):
            with self.assertRaises(ValidationError):
                Article.objects.create(title=f"Fake Article Title {index}", content_items={"items": items})

    def test_article_header_content_item(self):
        items = [
            {
                "type": "header",
                "title": "some title",
                "subtitle": "some subtitle",
                "image_url": "https://www.fakedomain.com",
            },
            {"type": "text", "content": "some text"},
        ]
        # Assert -- header item with no errors
        Article.objects.create(title="Fake Article Title", content_items={"items": items})

        # Assert -- multiple header items
        with self.assertRaises(ValidationError):
            Article.objects.create(title=f"Fake Article Title 2", content_items={"items": [items[0], items[0]]})
