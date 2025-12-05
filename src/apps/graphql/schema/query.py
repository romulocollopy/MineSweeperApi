import graphene

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
    is_flagged = graphene.Boolean()


class BoardType(graphene.ObjectType):
    slug = graphene.String()
    blocks = graphene.List(MineBlockType)
    flags = graphene.Int()
    game_over = graphene.Boolean()
    won = graphene.Boolean()
    time_elapsed = graphene.Int()
    difficulty = graphene.String()


class Query(graphene.ObjectType):
    mine_sweeper = graphene.Field(
        BoardType,
        slug=graphene.String(required=True),
        difficulty=graphene.String(),
    )

    def resolve_mine_sweeper(self, info, slug, difficulty=None):
        print((slug, difficulty))
        try:
            game = Game.objects.get_by_slug(slug=slug)
        except Game.DoesNotExist:
            try:
                difficulty = GameConfig.Difficulty(difficulty)
            except Exception:
                logger.exception(f"Invalid difficulty selected: {difficulty}")
                difficulty = GameConfig.Difficulty.hard

            print((slug, difficulty))

            game = Game.objects.new_game(slug=slug, difficulty=difficulty)

        return {
            **game.get_board().as_dict(),
            "game_over": game.game_over,
            "won": game.won,
            "time_elapsed": game.time_elapsed,
        }
