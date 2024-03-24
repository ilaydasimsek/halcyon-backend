from typing import Literal, Union

import pydantic
from django.db import models
from django_pydantic_field import SchemaField
from pydantic import Field
from typing_extensions import Annotated


class ArticleTextContentItem(pydantic.BaseModel):
    type: Literal["text"]
    content: str


class ArticleImageContentItem(pydantic.BaseModel):
    type: Literal["image"]
    image_url: str


class ArticleContentItems(pydantic.BaseModel):
    items: list[Annotated[Union[ArticleTextContentItem, ArticleImageContentItem], Field(discriminator="type")]]


class Article(models.Model):
    class Meta:
        ordering = ["-is_pinned"]

    title = models.CharField(unique=True, blank=False, null=False, max_length=255)
    content_items: ArticleContentItems = SchemaField(schema=ArticleContentItems, default=ArticleContentItems(items=[]))
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"Article({self.id}) - {self.title}"
