import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_lessons.graphql.types import YogaLessonConnection, YogaLessonNode
from yoga_lessons.models import YogaLesson


class Query(graphene.ObjectType):
    yoga_lessons = ConnectionField(YogaLessonConnection)
    yoga_lesson = graphene.Field(YogaLessonNode, id=graphene.Int(required=True))

    @login_required
    def resolve_yoga_lessons(self, info, **kwargs):
        return YogaLesson.objects.all()

    @login_required
    def resolve_yoga_lesson(self, info, id, **kwargs):
        return YogaLesson.objects.get(id=id)
