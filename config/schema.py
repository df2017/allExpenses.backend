import graphene
import graphql_jwt
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql_social_auth
from graphene_django import DjangoObjectType


class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    social_auth = graphql_social_auth.SocialAuthJWT.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)