import graphene
from graphql_jwt.decorators import login_required

from yoga_journeys.models import YogaJourney, JourneyCompletedYogaPractice


class CompleteYogaPractice(graphene.Mutation):
    class Arguments:
        yoga_practice_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_practice_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        yoga_journey.on_yoga_practice_completed(yoga_practice_id)
        return CompleteYogaPractice(ok=True)


class DeleteCompletedYogaPractice(graphene.Mutation):
    class Arguments:
        yoga_practice_id = graphene.Int(required=True)

    count = graphene.Int()

    @classmethod
    @login_required
    def mutate(cls, root, info, yoga_practice_id):
        yoga_journey, _ = YogaJourney.objects.get_or_create(user=info.context.user)
        count, _ = JourneyCompletedYogaPractice.objects.filter(
            yoga_journey__user=info.context.user, yoga_practice_id=yoga_practice_id
        ).delete()
        return DeleteCompletedYogaPractice(count=count)


class Mutation(graphene.ObjectType):
    complete_yoga_practice = CompleteYogaPractice.Field()
    delete_completed_yoga_practice = DeleteCompletedYogaPractice.Field()
