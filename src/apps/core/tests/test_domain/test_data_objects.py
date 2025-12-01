from itertools import chain
import json
import pytest


from apps.core.domain.data_objects import Board, Coordinates, GameConfig, MineBlock


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


@pytest.fixture
def board():
    """
    Board with this bombs disposition:
    *, 0, 0
    *, 0, 0
    0, 0, 0
    """
    return Board(
        blocks=[
            [
                MineBlock(coordinates=Coordinates(0, 0)),
                MineBlock(coordinates=Coordinates(0, 1), is_bomb=True),
                MineBlock(coordinates=Coordinates(0, 2), is_bomb=True),
            ],
            [
                MineBlock(coordinates=Coordinates(1, 0)),
                MineBlock(coordinates=Coordinates(1, 1)),
                MineBlock(coordinates=Coordinates(1, 2)),
            ],
            [
                MineBlock(coordinates=Coordinates(2, 0)),
                MineBlock(coordinates=Coordinates(2, 1)),
                MineBlock(coordinates=Coordinates(2, 2)),
            ],
        ]
    )
