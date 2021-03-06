import graphene

from authentication.models import User

from authentication.types import *
from authentication.mutations import *


class Query(graphene.ObjectType):

    # lấy thông tin của user qua id
    user_by_id = graphene.Field(UserType,
                                token=graphene.String(required=False),
                                id=graphene.Int(required=True))

    def resolve_user_by_id(root, info, **kwargs):
        id = kwargs.get('id')
        return User.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_link = CreateLinkMutation.Field()
