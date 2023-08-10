from django.conf import settings
from graphene import Schema
from graphene_django.settings import GrapheneSettings
from graphene_django.views import GraphQLView

import users.graphql.mutations
import users.graphql.queries


class Query(users.graphql.queries.Query):
    pass


class Mutation(users.graphql.mutations.Mutation):
    pass


schema = Schema(query=Query, mutation=Mutation)

graphql_view = GraphQLView.as_view(graphiql=settings.IS_DEV)
