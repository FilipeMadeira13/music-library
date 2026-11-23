from django.test import Client


def test_suite_runs() -> None:
    assert 1 + 1 == 2


def test_healthz_returns_ok(client: Client) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthz_rejects_post(client: Client) -> None:
    response = client.post("/healthz")

    assert response.status_code == 405
