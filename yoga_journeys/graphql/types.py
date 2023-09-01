from graphene import Connection, ConnectionField
from graphene_django import DjangoObjectType

from yoga_journeys.models import YogaJourney, JourneyCompletedYogaPractice, JourneyActiveYogaChallenge
from yoga_practices.models import YogaPractice, YogaChallenge


class ActiveYogaChallengeNode(DjangoObjectType):
    class Meta:
        model = JourneyActiveYogaChallenge
        fields = ("yoga_challenge", "activated_at", "completed_yoga_practices")


class CompletedYogaChallengeConnection(Connection):
    class Meta:
        node = ActiveYogaChallengeNode


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
    active_yoga_challenges = ConnectionField(CompletedYogaChallengeConnection)
    inactive_yoga_challenges = ConnectionField("yoga_practices.graphql.types.YogaChallengeConnection")

    def resolve_completed_yoga_practices(self, info, *args, **kwargs):
        return JourneyCompletedYogaPractice.objects.filter(yoga_journey=self)

    def resolve_uncompleted_yoga_practices(self, info, *args, **kwargs):
        completed_practices_query_set = JourneyCompletedYogaPractice.objects.filter(yoga_journey=self).values(
            "yoga_practice"
        )
        return YogaPractice.objects.exclude(id__in=completed_practices_query_set)

    def resolve_active_yoga_challenges(self, info, *args, **kwargs):
        return JourneyActiveYogaChallenge.objects.filter(yoga_journey=self)

    def resolve_inactive_yoga_challenges(self, info, *args, **kwargs):
        completed_challenges_query_set = JourneyActiveYogaChallenge.objects.filter(yoga_journey=self).values(
            "yoga_challenge"
        )
        return YogaChallenge.objects.exclude(id__in=completed_challenges_query_set)
