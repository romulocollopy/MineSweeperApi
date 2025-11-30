import json
from http import HTTPStatus

import pytest
from graphene_django.utils.testing import graphql_query


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        response = graphql_query(
            *args,
            client=client,
            graphql_url="/graphql/",
            headers={"content-type": "application/json"},
            **kwargs,
        )
        content = json.loads(response.content)
        assert response.status_code == HTTPStatus.OK
        return content

    return func
