from typing import Literal, Union, Optional

import pydantic
from django.db import models
from django_pydantic_field import SchemaField
from pydantic import Field, AfterValidator, Extra
from typing_extensions import Annotated


class BaseContentItem(pydantic.BaseModel):
    class Config:
        extra = Extra.forbid


class ArticleTextContentItem(BaseContentItem):
    type: Literal["text"]
    content: str


class ArticleImageContentItem(BaseContentItem):
    type: Literal["image"]
    image_url: str


class ArticleHeaderContentItem(BaseContentItem):
    type: Literal["header"]
    title: str
    subtitle: Optional[str] = None
    image_url: Optional[str] = None


def check_multiple_header_items(items):
    header_item_count = len([item for item in items if item.type == "header"])
    assert header_item_count <= 1, f"There can be only one header item. Found {header_item_count}"
    return items


class ArticleContentItems(pydantic.BaseModel):
    items: Annotated[
        list[
            Annotated[
                Union[ArticleTextContentItem, ArticleImageContentItem, ArticleHeaderContentItem],
                Field(discriminator="type"),
            ]
        ],
        AfterValidator(check_multiple_header_items),
    ]


class Article(models.Model):
    class Meta:
        ordering = ["-is_pinned"]

    title = models.CharField(unique=True, blank=False, null=False, max_length=255)
    content_items: ArticleContentItems = SchemaField(schema=ArticleContentItems, default=ArticleContentItems(items=[]))
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"Article({self.id}) - {self.title}"
