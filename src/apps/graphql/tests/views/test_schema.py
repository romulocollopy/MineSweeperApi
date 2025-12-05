from http import HTTPStatus

import pytest


def test_schema_empty_query(client_query):
    with pytest.raises(AssertionError) as exc_info:
        client_query("")

    assert exc_info.match(f".*{HTTPStatus.BAD_REQUEST}.*")


@pytest.mark.django_db
def test_game_schema(client_query, game):
    resp = client_query(
        """
        query MineSweeperQuery($slug: String!) {
            mineSweeper(slug: $slug) {
            slug
            flags
            gameOver
            won
            timeElapsed
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
        "gameOver": game.game_over,
        "timeElapsed": game.time_elapsed,
        "won": game.won,
        **game.get_board().as_dict(),
    }

    def replaceFlag(block):
        block["isFlagged"] = block.pop("is_flagged")
        del block["is_reveled"]
        return block

    expected["blocks"] = list(
        map(
            replaceFlag,
            expected["blocks"],
        )
    )

    assert resp["data"]["mineSweeper"] == expected


@pytest.mark.django_db
def test_update_board_mutation(client_query, game):
    mutation = """
        mutation UpdateBoard($slug: String!, $coordinates: CoordinatesInput!, $action: String!) {
            updateBoard(slug: $slug, coordinates: $coordinates, action: $action) {
                gameOver
                mineSweeper {
                    slug
                    flags
                    blocks {
                        coordinates {
                            x
                            y
                        }
                        display
                    }
                }
            }
        }
    """

    variables = {"slug": game.slug, "coordinates": {"x": 0, "y": 0}, "action": "dig"}

    resp = client_query(
        mutation,
        operation_name="UpdateBoard",
        variables=variables,
    )

    # --- Assertions ---
    assert "errors" not in resp
    data = resp["data"]["updateBoard"]

    assert data["gameOver"] is False
    assert data["mineSweeper"] is not None
    assert "blocks" in data["mineSweeper"]
    assert "flags" in data["mineSweeper"]

    # Check the returned block format
    first_block = data["mineSweeper"]["blocks"][0]
    assert "coordinates" in first_block
    assert "display" in first_block

    coords = first_block["coordinates"]
    assert "x" in coords
    assert "y" in coords


@pytest.mark.django_db
def test_update_board_mutation__game_over(client_query, game):
    mutation = """
        mutation UpdateBoard($slug: String!, $coordinates: CoordinatesInput!, $action: String!) {
            updateBoard(slug: $slug, coordinates: $coordinates, action: $action) {
                gameOver
                timeElapsed
                mineSweeper {
                    slug
                    flags
                    blocks {
                        coordinates {
                            x
                            y
                        }
                        display
                    }
                }
            }
        }
    """

    variables = {"slug": game.slug, "coordinates": {"x": 0, "y": 1}, "action": "dig"}

    resp = client_query(
        mutation,
        operation_name="UpdateBoard",
        variables=variables,
    )

    # --- Assertions ---
    assert "errors" not in resp
    data = resp["data"]["updateBoard"]

    assert data["gameOver"] is True
    assert data["mineSweeper"] is not None
    assert "blocks" in data["mineSweeper"]

    # Check the returned block format
    first_block = data["mineSweeper"]["blocks"][0]
    assert "coordinates" in first_block
    assert "display" in first_block

    coords = first_block["coordinates"]
    assert "x" in coords
    assert "y" in coords
