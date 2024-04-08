import logging

import graphene
from graphene import Connection
from graphene_django import DjangoObjectType

from articles.models import (
    Article,
    ArticleImageContentItem,
    ArticleTextContentItem,
    ArticleContentItems,
    ArticleHeaderContentItem,
)

logger = logging.getLogger(__name__)


class ArticleImageContentItemNode(graphene.ObjectType):
    image_url = graphene.String(required=True)


class ArticleTextContentItemNode(graphene.ObjectType):
    content = graphene.String(required=True)


class ArticleHeaderContentItemNode(graphene.ObjectType):
    title = graphene.String(required=True)
    subtitle = graphene.String(required=False)
    image_url = graphene.String(required=False)


class ArticleContentItemNode(graphene.Union):
    class Meta:
        types = (
            ArticleImageContentItemNode,
            ArticleTextContentItemNode,
            ArticleHeaderContentItemNode,
        )

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, ArticleImageContentItem):
            return ArticleImageContentItemNode
        elif isinstance(instance, ArticleTextContentItem):
            return ArticleTextContentItemNode
        elif isinstance(instance, ArticleHeaderContentItem):
            return ArticleHeaderContentItemNode
        logger.warning("Unknown type in ArticleContentItemNode", extra={"instance": instance})


class ArticleNode(DjangoObjectType):
    class Meta:
        model = Article
        fields = ("id", "title", "is_pinned")

    content_items = graphene.List(ArticleContentItemNode)

    def resolve_content_items(self: ArticleContentItems, *args, **kwargs):
        return self.content_items.items


class ArticleConnection(Connection):
    class Meta:
        node = ArticleNode
