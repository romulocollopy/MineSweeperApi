import pytest

from src.apps.core.domain.data_objects import Board
from src.apps.core.models import Game


@pytest.mark.django_db
def test_game(game):
    assert isinstance(game, Game)
    assert game.id
    assert game.slug == "my-game"


@pytest.mark.django_db
def test_get_board(game):
    board = game.get_board()
    assert isinstance(board, Board)
