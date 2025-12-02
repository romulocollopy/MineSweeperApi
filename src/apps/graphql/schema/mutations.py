import graphene

from src.apps.core.domain.use_cases import update_board_use_case
from src.apps.graphql.schema.query import BoardType


class CoordinatesInput(graphene.InputObjectType):
    x = graphene.Int(required=True)
    y = graphene.Int(required=True)


class UpdateBoardMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        coordinates = CoordinatesInput(required=True)
        action = graphene.String(required=True)

    # What the mutation returns
    game_over = graphene.Boolean()
    mine_sweeper = graphene.Field(lambda: BoardType)

    def mutate(self, info, slug, coordinates, action):
        x = coordinates.get("x")
        y = coordinates.get("y")

        board, game_over = update_board_use_case(slug, x, y, action)

        return UpdateBoardMutation(game_over=game_over, mine_sweeper=board.as_dict())


class Mutation(graphene.ObjectType):
    update_board = UpdateBoardMutation.Field()
