import graphene
import graphql_jwt
import dashboard.schema


class Query(dashboard.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(dashboard.schema.Mutation, graphene.ObjectType):

    class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
        user = graphene.Field(dashboard.schema.UserType)
        expires = graphene.DateTime()

        @classmethod
        def resolve(cls, root, info, **kwargs):

            return cls(user=info.context.user)

    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)