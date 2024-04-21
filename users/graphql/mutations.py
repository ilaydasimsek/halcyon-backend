import logging

import graphene
import graphql_jwt
from django.db import IntegrityError
from graphql_jwt.decorators import login_required

from users.models import User

logger = logging.getLogger(__name__)


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


class DeleteAccount(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        logger.info(f"Removing user {user.id}")
        user.delete()
        return DeleteAccount(ok=True)


class Mutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    sign_up = Signup.Field()
    delete_account = DeleteAccount.Field()
