from dataclasses import asdict
import datetime
from src.apps.core.domain.data_objects import Coordinates
from src.apps.core.domain.exceptions import Boom
from src.apps.core.models import Game


def update_board_use_case(slug: str, x: int, y: int):
    game: Game = Game.objects.get_by_slug(slug)
    board = game.get_board()
    block = board.get_block(Coordinates(x, y))
    try:
        block.dig(board)
    except Boom as exc:
        game.game_over = True
        game.finish_time = datetime.datetime.now()
        board = exc.board
    finally:
        game.board = asdict(board)
        game.save()

    return board, game.game_over
