"""Smoke-тесты HTTP API: проверяют, что Flask-приложение поднимается
и базовые эндпойнты (``/health``, ``/api/meta``) отдают валидный JSON."""

import pytest

from src.service import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["status"] == "ok"
    assert "service" in payload
    assert "llm_enabled" in payload

def test_meta_endpoint_returns_config(client):
    response = client.get("/api/meta")
    assert response.status_code == 200

    payload = response.get_json()
    assert isinstance(payload, dict)

def test_extract_without_file_returns_400(client):
    response = client.post("/api/extract")
    assert response.status_code == 400

def test_predict_alias_without_file_returns_400(client):

    response = client.post("/predict")
    assert response.status_code == 400

def test_index_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200

    assert len(response.data) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
