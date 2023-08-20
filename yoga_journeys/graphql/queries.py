import graphene
from graphql_jwt.decorators import login_required

from yoga_journeys.models import YogaJourney


class Query(graphene.ObjectType):
    journey = graphene.Field("yoga_journeys.graphql.types.YogaJourneyNode")

    @login_required
    def resolve_journey(self, info, **kwargs):
        user = info.context.user
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=user)
        return yoga_journey
