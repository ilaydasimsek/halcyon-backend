import graphene
from django.conf import settings
from graphene import ObjectType, String, Schema
from graphene_django.views import GraphQLView


class TestNode(ObjectType):
    first_name = String()
    last_name = String()
    full_name = String()


class Query(ObjectType):
    test = graphene.Field(TestNode, first_name=String(required=True), last_name=String(default_value="unknown"))

    def resolve_test(root, info, first_name, last_name):
        return {"first_name": first_name, "last_name": last_name, "full_name": f"{first_name} {last_name}"}


schema = Schema(query=Query)
graphql_view = GraphQLView.as_view(graphiql=settings.IS_DEV, schema=schema)
