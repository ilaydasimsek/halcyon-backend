import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_practices.graphql.types import YogaPracticeConnection
from yoga_practices.models import YogaPractice


class Query(graphene.ObjectType):
    yoga_practices = ConnectionField(YogaPracticeConnection)

    @login_required
    def resolve_yoga_practices(self, info, **kwargs):
        return YogaPractice.objects.all()
