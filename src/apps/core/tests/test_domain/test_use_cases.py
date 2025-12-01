from src.apps.core.domain.use_cases import update_board_use_case

import pytest


@pytest.mark.django_db
def test_update_board(game):
    update_board_use_case(game.slug, 0, 0)
