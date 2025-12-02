from dataclasses import asdict
import pytest

from src.apps.core.domain.data_objects import Board, Coordinates, MineBlock
from src.apps.core.models import Game


@pytest.fixture
def game(board):
    game = Game.objects.new_game("my-game")
    game.board = asdict(board)
    game.save()
    return game


@pytest.fixture
def board():
    """
    Board with this bombs disposition:
    0, 0, 0, 0
    *, 0, 0, 0
    *, 0, 0, 0
    0, 0, 0, 0
    """
    return Board(
        flags=2,
        blocks=[
            [
                MineBlock(coordinates=Coordinates(0, 0)),
                MineBlock(coordinates=Coordinates(0, 1), is_bomb=True),
                MineBlock(coordinates=Coordinates(0, 2), is_bomb=True),
                MineBlock(
                    coordinates=Coordinates(0, 3),
                ),
            ],
            [
                MineBlock(coordinates=Coordinates(1, 0)),
                MineBlock(coordinates=Coordinates(1, 1)),
                MineBlock(coordinates=Coordinates(1, 2)),
                MineBlock(coordinates=Coordinates(1, 3)),
            ],
            [
                MineBlock(coordinates=Coordinates(2, 0)),
                MineBlock(coordinates=Coordinates(2, 1)),
                MineBlock(coordinates=Coordinates(2, 2)),
                MineBlock(coordinates=Coordinates(2, 3)),
            ],
            [
                MineBlock(coordinates=Coordinates(3, 0)),
                MineBlock(coordinates=Coordinates(3, 1)),
                MineBlock(coordinates=Coordinates(3, 2)),
                MineBlock(coordinates=Coordinates(3, 3)),
            ],
        ],
    )
