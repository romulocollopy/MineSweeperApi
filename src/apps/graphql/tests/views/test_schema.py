from http import HTTPStatus

import pytest


def test_schema_empty_query(client_query):
    with pytest.raises(AssertionError) as exc_info:
        client_query("")

    assert exc_info.match(f".*{HTTPStatus.BAD_REQUEST}.*")


def test_schema(client_query):
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
