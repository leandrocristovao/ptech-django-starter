from django.urls import reverse


def test_health_endpoint(client):
    response = client.get(reverse("app:health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ptech-django-starter",
    }
