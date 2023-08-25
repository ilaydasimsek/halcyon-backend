from graphene import Connection, ConnectionField
from graphene_django import DjangoObjectType

from yoga_journeys.models import YogaJourney, JourneyCompletedYogaPractice
from yoga_practices.models import YogaPractice


class CompletedYogaPracticeNode(DjangoObjectType):
    class Meta:
        model = JourneyCompletedYogaPractice
        fields = ("yoga_practice", "created_at")


class CompletedYogaPracticeConnection(Connection):
    class Meta:
        node = CompletedYogaPracticeNode


class YogaJourneyNode(DjangoObjectType):
    class Meta:
        model = YogaJourney
        fields = ("id",)

    completed_yoga_practices = ConnectionField(CompletedYogaPracticeConnection)
    uncompleted_yoga_practices = ConnectionField("yoga_practices.graphql.types.YogaPracticeConnection")

    def resolve_completed_yoga_practices(self, info, *args, **kwargs):
        return JourneyCompletedYogaPractice.objects.filter(yoga_journey=self)

    def resolve_uncompleted_yoga_practices(self, info, *args, **kwargs):
        completed_practices_query_set = JourneyCompletedYogaPractice.objects.filter(yoga_journey=self).values(
            "yoga_practice"
        )
        return YogaPractice.objects.exclude(id__in=completed_practices_query_set)
