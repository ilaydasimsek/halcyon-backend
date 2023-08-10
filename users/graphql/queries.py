import graphene

from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    me = graphene.Field("users.graphql.types.UserType")

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user
