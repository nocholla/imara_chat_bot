import pytest
from fastapi.testclient import TestClient

from src.llm_pipeline import app

client = TestClient(app)

def test_generate():
    response = client.post(
        "/generate",
        json={
            "query": "How do I edit my profile?",
            "lang_code": "en",
            "is_soccer_enthusiast": False,
            "name": "TestUser"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_feedback():
    response = client.post(
        "/feedback",
        json={"conversation_history": "user: Hello\nassistant: Hi"}
    )
    assert response.status_code == 200
    assert "feedback" in response.json()