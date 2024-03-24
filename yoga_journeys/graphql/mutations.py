import graphene
from graphql_jwt.decorators import login_required

from yoga_journeys.models import YogaJourney
from yoga_practices.models import JourneyCompletedYogaPractice


class CompleteYogaPractice(graphene.Mutation):
    class Arguments:
        yoga_practice_id = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_practice_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.complete_yoga_practice(yoga_practice_id)
        return CompleteYogaPractice(ok=True)


class DeleteCompletedYogaPractice(graphene.Mutation):
    class Arguments:
        yoga_practice_id = graphene.String(required=True)

    count = graphene.Int()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_practice_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        count, _ = JourneyCompletedYogaPractice.objects.filter(
            yoga_journey__user=info.context.user, yoga_practice_id=yoga_practice_id
        ).delete()
        return DeleteCompletedYogaPractice(count=count)


class StartYogaChallenge(graphene.Mutation):
    class Arguments:
        yoga_challenge_id = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_challenge_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.start_yoga_challenge(yoga_challenge_id)
        return StartYogaChallenge(ok=True)


class CompleteYogaChallengePractice(graphene.Mutation):
    class Arguments:
        yoga_challenge_id = graphene.String(required=True)
        yoga_practice_id = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_challenge_id, yoga_practice_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.complete_yoga_challenge_practice(
            yoga_challenge_id=yoga_challenge_id, yoga_practice_id=yoga_practice_id
        )
        return CompleteYogaChallengePractice(ok=True)


class StartYogaLesson(graphene.Mutation):
    class Arguments:
        yoga_lesson_id = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_lesson_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.start_yoga_lesson(yoga_lesson_id)
        return StartYogaLesson(ok=True)


class CompleteYogaLessonStep(graphene.Mutation):
    class Arguments:
        yoga_lesson_id = graphene.String(required=True)
        yoga_lesson_step_id = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_lesson_id, yoga_lesson_step_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.complete_yoga_lesson_step(yoga_lesson_id=yoga_lesson_id, yoga_lesson_step_id=yoga_lesson_step_id)
        return CompleteYogaLessonStep(ok=True)


class Mutation(graphene.ObjectType):
    complete_yoga_practice = CompleteYogaPractice.Field()
    delete_completed_yoga_practice = DeleteCompletedYogaPractice.Field()
    start_yoga_challenge = StartYogaChallenge.Field()
    complete_yoga_challenge_practice = CompleteYogaChallengePractice.Field()
    start_yoga_lesson = StartYogaLesson.Field()
    complete_yoga_lesson_step = CompleteYogaLessonStep.Field()
