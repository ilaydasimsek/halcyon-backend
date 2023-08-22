import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_practices.graphql.types import YogaPracticeConnection, YogaChallengeConnection, YogaPracticeNode
from yoga_practices.models import YogaPractice, YogaChallenge


class Query(graphene.ObjectType):
    yoga_practices = ConnectionField(YogaPracticeConnection)
    yoga_challenges = ConnectionField(YogaChallengeConnection)
    yoga_practice = graphene.Field(YogaPracticeNode, id=graphene.Int(required=True))

    @login_required
    def resolve_yoga_practices(self, info, **kwargs):
        return YogaPractice.objects.all()

    @login_required
    def resolve_yoga_challenges(self, info, **kwargs):
        return YogaChallenge.objects.all()

    @login_required
    def resolve_yoga_practice(self, info, id):
        return YogaPractice.objects.get(id=id)
