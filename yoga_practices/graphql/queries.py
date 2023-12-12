import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_practices.graphql.types import (
    YogaPracticeConnection,
    YogaChallengeConnection,
    YogaPracticeNode,
    YogaChallengeNode,
    YogaCategoryConnection,
    YogaStyleConnection,
)
from yoga_practices.models import YogaPractice, YogaChallenge, YogaCategory, YogaStyle
from django.db import models


class Query(graphene.ObjectType):
    yoga_practices = ConnectionField(YogaPracticeConnection, style_id=graphene.Int(required=False))
    yoga_challenges = ConnectionField(YogaChallengeConnection)
    yoga_categories = ConnectionField(YogaCategoryConnection)
    yoga_styles = ConnectionField(YogaStyleConnection)

    yoga_practice = graphene.Field(YogaPracticeNode, id=graphene.Int(required=True))
    yoga_challenge = graphene.Field(YogaChallengeNode, id=graphene.Int(required=True))

    @login_required
    def resolve_yoga_practices(self, info, **kwargs):
        query = models.Q()
        style_id = kwargs.get("style_id")
        if style_id is not None:
            query &= models.Q(style=style_id)
        return YogaPractice.objects.filter(query).distinct()

    @login_required
    def resolve_yoga_challenges(self, info, **kwargs):
        return YogaChallenge.objects.related_active_challenges(user=info.context.user).all()

    @login_required
    def resolve_yoga_categories(self, info, **kwargs):
        return YogaCategory.objects.all()

    @login_required
    def resolve_yoga_styles(self, info, **kwargs):
        return YogaStyle.objects.all()

    @login_required
    def resolve_yoga_practice(self, info, id):
        return YogaPractice.objects.get(id=id)

    @login_required
    def resolve_yoga_challenge(self, info, id):
        return YogaChallenge.objects.related_active_challenges(user=info.context.user).get(id=id)
