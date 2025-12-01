from http import HTTPStatus

import pytest

from src.apps.core.models import Game


def test_schema_empty_query(client_query):
    with pytest.raises(AssertionError) as exc_info:
        client_query("")

    assert exc_info.match(f".*{HTTPStatus.BAD_REQUEST}.*")


def test_user_schema(client_query):
    resp = client_query(
        """
        query UserProfileQuery {
            viewer {
                id
                name
                email
            }
        }
        """,
        operation_name="UserProfileQuery",
    )

    assert "data" in resp


@pytest.mark.django_db
def test_game_schema(client_query, game):
    resp = client_query(
        """
        query MineSweeperQuery($slug: String!) {
            mineSweeper(slug: $slug) {
            slug
            flags
            blocks {
                coordinates {
                    x
                    y
                }
                    display
                    isFlagged
                }
            }
        }
        """,
        operation_name="MineSweeperQuery",
        variables=dict(
            slug=game.slug,
        ),
    )

    assert "data" in resp

    expected = {
        "slug": game.slug,
        **game.get_board().as_dict(),
    }

    def replaceFlag(block):
        block["isFlagged"] = block.pop("is_flagged")
        return block

    expected["blocks"] = list(
        map(
            replaceFlag,
            expected["blocks"],
        )
    )

    assert resp["data"]["mineSweeper"] == expected


@pytest.fixture
def game():
    return Game.objects.new_game("my-game")
