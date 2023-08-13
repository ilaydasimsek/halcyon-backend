import graphene
import graphql_jwt
from django.db import IntegrityError

from users.models import User


class Signup(graphql_jwt.ObtainJSONWebToken):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            User.objects.create_user(**kwargs)
        except IntegrityError:
            raise Exception("A user with the same email exists.")
        return super().mutate(root, info, **kwargs)


class Mutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    sign_up = Signup.Field()
