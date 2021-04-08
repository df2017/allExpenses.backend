import graphene
import apps.hero.types as schemas
import graphql_jwt
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql_social_auth
from graphene_django import DjangoObjectType


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()

class Query(schemas.Query, UserQuery, MeQuery, graphene.ObjectType):
    pass

# class Mutation(schema.Mutation, AuthMutation, graphene.ObjectType):
#    pass

class Mutation(schemas.Mutation, AuthMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    social_auth = graphql_social_auth.SocialAuthJWT.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)