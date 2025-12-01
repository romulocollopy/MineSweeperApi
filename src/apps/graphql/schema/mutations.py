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

    # What the mutation returns
    ok = graphene.Boolean()
    board = graphene.Field(lambda: BoardType)

    def mutate(self, info, slug, coordinates):
        x = coordinates.get("x")
        y = coordinates.get("y")

        board = update_board_use_case(slug, x, y)

        return UpdateBoardMutation(ok=True, board=board.as_dict())


class Mutation(graphene.ObjectType):
    update_board = UpdateBoardMutation.Field()
