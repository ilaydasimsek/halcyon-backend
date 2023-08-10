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

main_schema_settings = GrapheneSettings(
    {
        "SCHEMA": schema,
        "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
    },
)
graphql_view = GraphQLView.as_view(graphiql=settings.IS_DEV, schema=schema, middleware=main_schema_settings.MIDDLEWARE)
