import graphene

from src.apps.core.domain.data_objects import GameConfig
from src.apps.core.models import Game


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
    slug = graphene.String()
    blocks = graphene.List(MineBlockType)


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)
    mineSweeper = graphene.Field(BoardType, slug=graphene.String(required=True))

    def resolve_viewer(self, info):
        # Just return a dict with the required fields
        return {"id": "user_123", "name": "Test User", "email": "test@example.com"}

    def resolve_mineSweeper(self, info, slug):
        # Just return a dict with the required fields
        try:
            game = Game.objects.get_by_slug(slug=slug)
        except Game.DoesNotExist:
            game = Game.objects.new_game(slug=slug)

        return {"slug": game.slug, **game.get_board().as_dict()}


schema = graphene.Schema(query=Query)
