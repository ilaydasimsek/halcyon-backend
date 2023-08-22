import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_practices.graphql.types import (
    YogaPracticeConnection,
    YogaChallengeConnection,
    YogaPracticeNode,
    YogaCategoryConnection,
)
from yoga_practices.models import YogaPractice, YogaChallenge, YogaCategory
from django.db import models


class Query(graphene.ObjectType):
    yoga_practices = ConnectionField(YogaPracticeConnection, category_id=graphene.Int(required=False))
    yoga_challenges = ConnectionField(YogaChallengeConnection)
    yoga_categories = ConnectionField(YogaCategoryConnection)

    yoga_practice = graphene.Field(YogaPracticeNode, id=graphene.Int(required=True))

    @login_required
    def resolve_yoga_practices(self, info, **kwargs):
        query = models.Q()
        category_id = kwargs.get("category_id")
        if category_id is not None:
            query &= models.Q(yoga_poses__categories=category_id)
        return YogaPractice.objects.filter(query)

    @login_required
    def resolve_yoga_challenges(self, info, **kwargs):
        return YogaChallenge.objects.all()

    @login_required
    def resolve_yoga_categories(self, info, **kwargs):
        return YogaCategory.objects.all()

    @login_required
    def resolve_yoga_practice(self, info, id):
        return YogaPractice.objects.get(id=id)
