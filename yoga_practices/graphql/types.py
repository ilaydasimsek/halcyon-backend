from graphene import Connection
from graphene_django import DjangoObjectType

from yoga_practices.models import YogaPractice, YogaPose, MuscleGroup, YogaChallenge


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


class YogaPracticeConnection(Connection):
    class Meta:
        node = YogaPracticeNode


class YogaPoseNode(DjangoObjectType):
    class Meta:
        model = YogaPose
        fields = ("id", "name", "sanskrit_name", "description", "difficulty", "muscle_groups", "audio_url", "image_url")


class MuscleGroupNode(DjangoObjectType):
    class Meta:
        model = MuscleGroup
        fields = ("id", "name")
