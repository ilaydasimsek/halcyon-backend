import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from articles.graphql.types import ArticleNode, ArticleConnection
from articles.models import Article


class Query(graphene.ObjectType):
    article = graphene.Field(ArticleNode, id=graphene.String(required=True))
    articles = ConnectionField(ArticleConnection)

    @login_required
    def resolve_article(self, info, id, **kwargs):
        return Article.objects.get(id=id)

    @login_required
    def resolve_articles(self, info, **kwargs):
        return Article.objects.all()
