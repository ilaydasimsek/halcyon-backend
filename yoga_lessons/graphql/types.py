import graphene
from graphene import Connection
from graphene_django import DjangoObjectType

from yoga_lessons.models import YogaLesson, YogaLessonStep


class YogaLessonNode(DjangoObjectType):
    class Meta:
        model = YogaLesson
        fields = ("id", "title", "description", "cover_image_url", "steps")

    steps_count = graphene.Int()


class YogaLessonConnection(Connection):
    class Meta:
        node = YogaLessonNode


class YogaLessonStepNode(DjangoObjectType):
    class Meta:
        model = YogaLessonStep
        fields = ("title", "duration", "audio_url", "image_url", "order")
