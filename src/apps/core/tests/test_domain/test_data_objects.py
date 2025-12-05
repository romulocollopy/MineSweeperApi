import json
from itertools import chain

import pytest

from apps.core.domain.data_objects import (
    Board,
    Coordinates,
    GameConfig,
)
from src.apps.core.domain.exceptions import Boom


@pytest.mark.parametrize(
    "dificulty",
    (
        GameConfig.Difficulty.easy,
        GameConfig.Difficulty.medium,
        GameConfig.Difficulty.hard,
    ),
)
def test_game_config(dificulty):
    board = GameConfig(dificulty).new_board()
    assert isinstance(board, Board)

    width, height, bombs = dificulty.value
    assert len(list(filter(lambda b: b.is_bomb, chain(*board.blocks)))) == bombs
    assert len(board.blocks) == width
    for col in board.blocks:
        assert len(col) == height

    assert board.grid_size == (width, height)


@pytest.mark.parametrize(
    ["x", "y"], ((0, 0), (0, 1), (1, 0), (10, 10), (15, 15), (3, 12))
)
def test_board_coordinates(x, y):
    board = GameConfig(GameConfig.Difficulty.medium).new_board()
    assert isinstance(board, Board)
    assert board.blocks[x][y].coordinates == Coordinates(x, y)


def test_block(board: Board):
    bottom_left = board.get_block(Coordinates(0, 0))
    bottom_right = board.get_block(Coordinates(2, 0))
    middle = board.get_block(Coordinates(1, 1))
    middle_top = board.get_block(Coordinates(1, 2))
    top_right = board.get_block(Coordinates(2, 2))

    assert bottom_left.bombs_around(board) == 1
    assert bottom_right.bombs_around(board) == 0
    assert middle.bombs_around(board) == 2
    assert middle_top.bombs_around(board) == 2
    assert top_right.bombs_around(board) == 0


def test_as_dict(board: Board):
    assert json.dumps(board.as_dict())


def test_dig_with_bomb(board: Board):
    block = board.get_block(Coordinates(0, 1))
    with pytest.raises(Boom):
        block.dig(board)

    assert block.display == "💣"


def test_won(board):
    for block in chain(*board.blocks):
        if not block.is_bomb:
            block.reveal(board)
    assert board.has_won()


def test_dig_cascades__changes_display(board: Board):
    block = board.get_block(Coordinates(2, 2))
    block.dig(board)

    assert board.blocks[0][0].display == ""
    assert board.blocks[0][1].display == ""
    assert board.blocks[0][2].display == ""

    assert board.blocks[1][0].display == "1"
    assert board.blocks[1][1].display == "2"
    assert board.blocks[1][2].display == "2"

    assert board.blocks[2][0].display == "-"
    assert board.blocks[2][1].display == "-"
    assert board.blocks[2][2].display == "-"


@pytest.mark.parametrize("diff_string", ("easy", "medium", "hard"))
def test_game_config_difficulty(diff_string):
    GameConfig.Difficulty(diff_string)
