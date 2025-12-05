import pytest

from src.apps.core.domain.data_objects import Coordinates, Symbols
from src.apps.core.domain.use_cases import update_board_use_case


@pytest.mark.django_db
def test_update_board__dig(game):
    board, game_over, won, time_elapsed = update_board_use_case(game.slug, 0, 0, "dig")
    assert not game_over
    assert not won
    assert board.get_block(Coordinates(0, 0)).display == "1"


@pytest.mark.django_db
def test_update_board__dig__empty(game):
    board, game_over, _, _ = update_board_use_case(game.slug, 2, 0, "dig")
    assert not game_over
    assert board.get_block(Coordinates(2, 0)).display == Symbols.empty


@pytest.mark.django_db
def test_update_board__flag(game):
    board, game_over, won, _ = update_board_use_case(game.slug, 0, 0, "flag")
    assert not game_over
    assert not won
    assert board.get_block(Coordinates(0, 0)).display == Symbols.flag


@pytest.mark.django_db
def test_update_board__dig_bomb(game):
    board, game_over, won, _ = update_board_use_case(game.slug, 0, 1, "dig")
    assert game_over
    assert not won
    assert board.get_block(Coordinates(0, 1)).display == Symbols.bomb
