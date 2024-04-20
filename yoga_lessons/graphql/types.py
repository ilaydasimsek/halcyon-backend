import logging

import graphene
from graphene import Connection
from graphene_django import DjangoObjectType

from articles.graphql.types import ArticleNode
from yoga_lessons.models import YogaLesson, JourneyActiveYogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep

logger = logging.getLogger(__name__)


class YogaLessonArticleStepNode(DjangoObjectType):
    class Meta:
        model = YogaLessonArticleStep
        fields = ("id", "article")

    article = graphene.Field(ArticleNode)


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

    active_yoga_lesson = graphene.Field("yoga_lessons.graphql.types.ActiveYogaLessonNode")

    def resolve_active_yoga_lesson(self: YogaLesson, info, *args, **kwargs):
        if hasattr(self, "user_active_lessons"):
            user_active_lessons = self.user_active_lessons
            if len(user_active_lessons):
                return user_active_lessons[0]
        else:
            logger.warning("user_active_lessons field was not prefetched in yoga lessons query.")
        return None

    def resolve_steps(self: YogaLesson, info, *args, **kwargs):
        return self.steps.all()


class YogaLessonConnection(Connection):
    class Meta:
        node = YogaLessonNode


class ActiveYogaLessonNode(DjangoObjectType):
    class Meta:
        model = JourneyActiveYogaLesson
        fields = ("yoga_lesson", "created_at", "completed_lesson_steps")

    completed_lesson_steps = graphene.List(YogaLessenStepNode)

    def resolve_completed_lesson_steps(self: JourneyActiveYogaLesson, info, *args, **kwargs):
        return self.completed_lesson_steps.all()


class ActiveYogaLessonConnection(Connection):
    class Meta:
        node = ActiveYogaLessonNode
