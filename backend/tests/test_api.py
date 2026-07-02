import json
import pytest
from backend.app import app

@pytest.fixture

def client():
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_recommend_requires_json(client):
    response = client.post("/api/recommend", data="notjson")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_recommend_requires_recipe_text(client):
    response = client.post("/api/recommend", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "recipe_text is required and must be a string"


def test_recommend_returns_structure(client):
    payload = {
        "recipe_text": "2 huevos, 100g de harina. Mezclar y hornear.",
        "preferences": "hacerla más saludable"
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "original_ingredients" in data
    assert "modified_ingredients" in data
    assert "modified_steps" in data
    assert "warnings" in data
