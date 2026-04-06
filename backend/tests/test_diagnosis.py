import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_bedrock():
    with patch("app.orchestration.agents.diagnosis_agent.get_bedrock_client") as mock_factory:
        mock_client = MagicMock()
        mock_factory.return_value = mock_client
        yield mock_client.converse


@pytest.fixture
def mock_rag():
    with patch("app.orchestration.agents.diagnosis_agent.symptom_query") as mock:
        yield mock


def test_diagnosis_endpoint_success(mock_bedrock, mock_rag):
    stage1_json = '{"symptoms": ["yellow leaves"], "affected_parts": ["leaves"], "severity": "mild", "image_quality": "good"}'
    stage2_json = '{"disease": "Cassava Mosaic Disease", "confidence": 95, "scientific_name": "Begomovirus", "symptoms": ["yellow leaves"], "organic_treatments": ["Remove plant"], "chemical_treatments": []}'

    mock_bedrock.side_effect = [
        {"output": {"message": {"content": [{"text": stage1_json}]}}},
        {"output": {"message": {"content": [{"text": stage2_json}]}}}
    ]

    mock_rag.return_value = "Mock RAG Document Text"

    files = {"file": ("test.jpg", b"dummy_image_bytes", "image/jpeg")}
    response = client.post("/diagnose/", files=files)

    assert response.status_code == 200, f"Unexpected {response.status_code}: {response.text}"
    data = response.json()
    assert data["disease"] == "Cassava Mosaic Disease"
    assert data["confidence"] == 95
    assert data["organic_treatments"][0] == "Remove plant"

    assert mock_bedrock.call_count == 2
    mock_rag.assert_called_once_with("yellow leaves")


def test_diagnosis_endpoint_poor_quality(mock_bedrock):
    stage1_json = '{"symptoms": [], "affected_parts": [], "severity": "mild", "image_quality": "poor"}'
    mock_bedrock.return_value = {"output": {"message": {"content": [{"text": stage1_json}]}}}

    files = {"file": ("blurry.jpg", b"dummy_bytes", "image/jpeg")}
    response = client.post("/diagnose/", files=files)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert "too blurry" in data["detail"].lower()
    assert mock_bedrock.call_count == 1


def test_diagnosis_endpoint_invalid_file_type():
    files = {"file": ("test.txt", b"dummy_text", "text/plain")}
    response = client.post("/diagnose/", files=files)

    assert response.status_code == 400
    assert "not an image" in response.json()["detail"].lower()
