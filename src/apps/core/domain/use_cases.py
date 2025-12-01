from src.apps.core.domain.data_objects import Coordinates
from src.apps.core.models import Game


def update_board_use_case(slug: str, x: int, y: int):
    game: Game = Game.objects.get_by_slug(slug)
    board = game.get_board()
    block = board.get_block(Coordinates(x, y))
    block.dig(board)
