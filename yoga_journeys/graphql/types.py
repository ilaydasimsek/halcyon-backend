from graphene import Connection, ConnectionField
from graphene_django import DjangoObjectType

from yoga_journeys.models import YogaJourney, JourneyCompletedYogaPractice


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

    def resolve_completed_yoga_practices(self, info, *args, **kwargs):
        return JourneyCompletedYogaPractice.objects.filter(yoga_journey=self)
