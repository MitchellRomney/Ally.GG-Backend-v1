import graphene
import graphql_jwt
import dashboard.schema
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload
from django.contrib.auth import authenticate, login
from dynamic_preferences.registries import global_preferences_registry


class UserNode(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = get_user_model()
        filter_fields = [
            'username',
        ]

    def resolve_token(self, info, **kwargs):
        if info.context.user != self:
            return None

        payload = jwt_payload(self)
        return jwt_encode(payload)


class Query(dashboard.schema.Query, graphene.ObjectType):

    pass


class Mutation(dashboard.schema.Mutation, graphene.ObjectType):

    class Login(graphene.Mutation):
        user = graphene.Field(UserNode)
        patch = graphene.String()

        class Arguments:
            username = graphene.String()
            password = graphene.String()

        @classmethod
        def mutate(cls, root, info, username, password):
            global_preferences = global_preferences_registry.manager()
            user_model = get_user_model()

            user_obj = user_model.objects.get(username__iexact=username)

            user = authenticate(username=user_obj.username, password=password)

            if user is None:
                raise Exception('Please enter a correct username and password')

            if not user.is_active:
                raise Exception('It seems your account has been disabled')

            login(info.context, user)

            return cls(user=user, patch=global_preferences['LATEST_PATCH'])

    class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
        user = graphene.Field(dashboard.schema.UserType)
        expires = graphene.DateTime()

        @classmethod
        def resolve(cls, root, info, **kwargs):

            return cls(user=info.context.user)

    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    login = Login.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)