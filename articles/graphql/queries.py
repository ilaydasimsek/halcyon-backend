import graphene
from graphql_jwt.decorators import login_required

from articles.graphql.types import ArticleNode
from articles.models import Article


class Query(graphene.ObjectType):
    article = graphene.Field(ArticleNode, id=graphene.Int(required=True))

    @login_required
    def resolve_article(self, info, id, **kwargs):
        return Article.objects.get(id=id)
