import graphene
from graphene import Connection
from graphene_django import DjangoObjectType

from yoga_lessons.models import YogaLesson, JourneyActiveYogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep


class YogaLessonArticleStepNode(DjangoObjectType):
    class Meta:
        model = YogaLessonArticleStep
        fields = ("id",)  # TODO: Add more fields


class YogaLessonPracticeStepNode(DjangoObjectType):
    class Meta:
        model = YogaLessonPracticeStep
        fields = ("id", "yoga_practice")


class YogaLessenStepNode(graphene.Union):
    class Meta:
        types = (
            YogaLessonArticleStepNode,
            YogaLessonPracticeStepNode,
        )


class YogaLessonNode(DjangoObjectType):
    class Meta:
        model = YogaLesson
        fields = ("id", "title", "description", "cover_image_url", "steps")

    steps_count = graphene.Int()
    steps = graphene.List(YogaLessenStepNode)

    def resolve_steps(self: YogaLesson, info, *args, **kwargs):
        return self.steps.all()


class YogaLessonConnection(Connection):
    class Meta:
        node = YogaLessonNode


class ActiveYogaLessonNode(DjangoObjectType):
    class Meta:
        model = JourneyActiveYogaLesson
        fields = ("yoga_lesson", "created_at", "completed_lesson_steps")


class ActiveYogaLessonConnection(Connection):
    class Meta:
        node = ActiveYogaLessonNode
