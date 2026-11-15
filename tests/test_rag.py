from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "API is running" in response.json()["message"]


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch("app.main.answer_question")
def test_ask_endpoint(mock_answer):
    mock_answer.return_value = {
        "answer": "PM-KISAN provides Rs. 6,000 annually.",
        "sources": [
            {
                "name": "PM-KISAN",
                "file": "tn_agriculture_schemes.json",
                "url": "https://pmkisan.gov.in/",
                "page": None,
                "type": "scheme_json"
            }
        ]
    }

    response = client.post(
        "/ask",
        json={
            "question": "What is the PM-KISAN benefit?",
            "language": "English"
        }
    )

    assert response.status_code == 200
    assert response.json()["language"] == "English"
    assert "Rs. 6,000" in response.json()["answer"]
    assert len(response.json()["sources"]) == 1
    assert response.json()["sources"][0]["name"] == "PM-KISAN"


@patch("app.main.answer_question")
def test_ask_endpoint_error(mock_answer):
    mock_answer.side_effect = ValueError("Test error")

    response = client.post(
        "/ask",
        json={
            "question": "Test question",
            "language": "English"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Test error"
