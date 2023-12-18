import graphene
import logging
from graphene import Connection, ObjectType
from graphene_django import DjangoObjectType

from yoga_practices.models import (
    YogaPractice,
    YogaPose,
    MuscleGroup,
    YogaChallenge,
    YogaCategory,
    JourneyCompletedYogaPractice,
    JourneyActiveYogaChallenge,
    YogaStyle,
    YogaChallengePractice,
)

logger = logging.getLogger(__name__)


class YogaChallengeNode(DjangoObjectType):
    class Meta:
        model = YogaChallenge
        fields = (
            "id",
            "title",
            "description",
            "benefits_description",
            "cover_image_url",
            "created_by",
            "created_at",
        )

    active_yoga_challenge = graphene.Field("yoga_practices.graphql.types.ActiveYogaChallengeNode")
    practices = graphene.List("yoga_practices.graphql.types.YogaPracticeNode")

    def resolve_active_yoga_challenge(self: YogaChallenge, info, *args, **kwargs):
        if hasattr(self, "user_active_challenges"):
            user_active_challenges = self.user_active_challenges
            if len(user_active_challenges):
                return user_active_challenges[0]
        else:
            logger.warning("user_active_challenges field was not prefetched in yoga challenges query.")
        return None

    def resolve_practices(self: YogaChallenge, info, *args, **kwargs):
        yoga_challenge_practices = YogaChallengePractice.objects.filter(yoga_challenge=self).prefetch_related(
            "yoga_practice"
        )
        return [object.yoga_practice for object in yoga_challenge_practices]


class YogaChallengeConnection(Connection):
    class Meta:
        node = YogaChallengeNode


class YogaPracticeNode(DjangoObjectType):
    class Meta:
        model = YogaPractice
        fields = (
            "id",
            "title",
            "description",
            "benefits_description",
            "cover_image_url",
            "created_by",
            "created_at",
            "yoga_poses",
            "style",
        )

    duration = graphene.Int(description="total duration in seconds")
    muscle_groups_distribution = graphene.List("yoga_practices.graphql.types.MuscleGroupDistributionNode")
    yoga_pose_count = graphene.Int(description="Total number of poses")

    def resolve_yoga_pose_count(self: YogaPractice, info, **kwargs):
        return self.yoga_poses.count()


class YogaPracticeConnection(Connection):
    class Meta:
        node = YogaPracticeNode


class YogaPoseNode(DjangoObjectType):
    class Meta:
        model = YogaPose
        fields = (
            "id",
            "name",
            "sanskrit_name",
            "description",
            "difficulty",
            "muscle_groups",
            "audio_url",
            "image_url",
            "chakras",
        )


class MuscleGroupNode(DjangoObjectType):
    class Meta:
        model = MuscleGroup
        fields = ("id", "name")


class MuscleGroupDistributionNode(ObjectType):
    id = graphene.String()
    name = graphene.String()
    count = graphene.Int()


class YogaCategoryNode(DjangoObjectType):
    class Meta:
        model = YogaCategory
        fields = ("id", "name", "description")


class YogaCategoryConnection(Connection):
    class Meta:
        node = YogaCategoryNode


class YogaStyleNode(DjangoObjectType):
    class Meta:
        model = YogaStyle
        fields = ("id", "name", "description")


class YogaStyleConnection(Connection):
    class Meta:
        node = YogaStyleNode


class CompletedYogaPracticeNode(DjangoObjectType):
    class Meta:
        model = JourneyCompletedYogaPractice
        fields = ("yoga_practice", "created_at")


class CompletedYogaPracticeConnection(Connection):
    class Meta:
        node = CompletedYogaPracticeNode


class ActiveYogaChallengeNode(DjangoObjectType):
    class Meta:
        model = JourneyActiveYogaChallenge
        fields = ("yoga_challenge", "activated_at", "completed_yoga_practices")


class CompletedYogaChallengeConnection(Connection):
    class Meta:
        node = ActiveYogaChallengeNode
