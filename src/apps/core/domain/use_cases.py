from dataclasses import asdict
import datetime
from src.apps.core.domain.data_objects import Board, Coordinates, MineBlock
from src.apps.core.domain.exceptions import Boom
from src.apps.core.models import Game


def run_action(block: MineBlock, board: Board, action: str):
    if action == "flag":
        if block.is_flagged:
            return block.remove_flag(board)

        return block.flag(board)

    block.dig(board)


def update_board_use_case(slug: str, x: int, y: int, action: str):
    game: Game = Game.objects.get_by_slug(slug)
    board = game.get_board()
    block = board.get_block(Coordinates(x, y))
    try:
        run_action(block, board, action)
    except Boom as exc:
        game.game_over = True
        game.finish_time = datetime.datetime.now()
        board = exc.board
    finally:
        if board.has_won():
            game.won = True
            game.finish_time = datetime.datetime.now()
        game.board = asdict(board)
        game.save()

    return board, game.game_over, game.won
