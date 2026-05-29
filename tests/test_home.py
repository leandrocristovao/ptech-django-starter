from django.urls import reverse


def test_home_page(client):
    response = client.get(reverse("app:home"))

    assert response.status_code == 200
    assert "PTech Django Starter" in response.content.decode()
