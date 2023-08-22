import graphene
from graphene import Connection, ObjectType
from graphene_django import DjangoObjectType

from yoga_practices.models import YogaPractice, YogaPose, MuscleGroup, YogaChallenge, YogaCategory


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
            "practices",
        )


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
