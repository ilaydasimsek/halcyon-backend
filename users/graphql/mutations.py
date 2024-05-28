import logging

import graphene
import graphql_jwt
from django.db import IntegrityError
from graphql_jwt.decorators import login_required

from users.mail.service import MailService
from users.models import User, PasswordResetVerification

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

class ResetPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        new_password = graphene.String(required=True)
        verification_code = graphene.String(required=True)

    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, email, new_password, verification_code, **kwargs):
        try:
            user = User.objects.get(email=email)
            user.reset_password(new_password=new_password, verification_code=verification_code)
            return ResetPassword(ok=True)
        except (User.DoesNotExist, PermissionError):
            raise PermissionError("Invalid email or verification code")


class TriggerForgotPasswordFlow(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, email, **kwargs):
        try:
            user = User.objects.get(email=email)
            code = PasswordResetVerification.create_for_user(user).code
            MailService.send_reset_password_mail(email, code)
            return ResetPassword(ok=True)
        except User.DoesNotExist:
            # Do not reveal if email is invalid
            pass
        return TriggerForgotPasswordFlow(ok=True)

class Mutation(graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    sign_up = Signup.Field()
    delete_account = DeleteAccount.Field()
    reset_password = ResetPassword.Field()
    trigger_forgot_password_flow = TriggerForgotPasswordFlow.Field()
