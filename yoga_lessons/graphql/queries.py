import graphene
from graphene import ConnectionField
from graphql_jwt.decorators import login_required

from yoga_lessons.graphql.types import YogaLessonConnection
from yoga_lessons.models import YogaLesson


class Query(graphene.ObjectType):
    yoga_lessons = ConnectionField(YogaLessonConnection, category_id=graphene.Int(required=False))

    @login_required
    def resolve_yoga_lessons(self, info, **kwargs):
        return YogaLesson.objects.all()
