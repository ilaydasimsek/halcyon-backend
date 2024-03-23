from django.conf import settings
from graphene import Schema
from graphene_django.views import GraphQLView

import users.graphql.mutations
import users.graphql.queries
import yoga_journeys.graphql.mutations
import yoga_journeys.graphql.queries
import yoga_lessons.graphql.queries
import yoga_practices.graphql.queries
import articles.graphql.queries


class Query(
    users.graphql.queries.Query,
    yoga_practices.graphql.queries.Query,
    yoga_journeys.graphql.queries.Query,
    yoga_lessons.graphql.queries.Query,
    articles.graphql.queries.Query,
):
    pass


class Mutation(users.graphql.mutations.Mutation, yoga_journeys.graphql.mutations.Mutation):
    pass


schema = Schema(query=Query, mutation=Mutation)

graphql_view = GraphQLView.as_view(graphiql=settings.IS_DEV)
