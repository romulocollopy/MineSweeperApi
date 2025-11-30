from django.urls import reverse


def test_set_cookie(client):
    url = reverse("csrf_token")
    resp = client.get(url)
    data = resp.json()
    assert data["csrf_token"]
