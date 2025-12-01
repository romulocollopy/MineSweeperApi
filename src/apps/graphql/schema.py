import graphene

from src.apps.core.domain.data_objects import GameConfig


class UserType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()


class CoordinateType(graphene.ObjectType):
    x = graphene.Int()
    y = graphene.Int()


class MineBlockType(graphene.ObjectType):
    coordinates = graphene.Field(CoordinateType)
    display = graphene.String()


class BoardType(graphene.ObjectType):
    id = graphene.ID()
    blocks = graphene.List(MineBlockType)


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)
    mineSweeper = graphene.Field(BoardType, id=graphene.ID(required=True))

    def resolve_viewer(self, info):
        # Just return a dict with the required fields
        return {"id": "user_123", "name": "Test User", "email": "test@example.com"}

    def resolve_mineSweeper(self, info, id):
        # Just return a dict with the required fields
        return GameConfig(GameConfig.Difficulty.medium).new_board().as_dict()


schema = graphene.Schema(query=Query)
