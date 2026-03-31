import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_bedrock():
    with patch("app.orchestration.agents.diagnosis_agent.invoke_converse", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_rag():
    with patch("app.orchestration.agents.diagnosis_agent.symptom_query") as mock:
        yield mock

def test_diagnosis_endpoint_success(mock_bedrock, mock_rag):
    # Mock Stage 1 Response (Symptom Extraction)
    mock_bedrock.side_effect = [
        # Stage 1
        '''{"symptoms": ["yellow leaves"], "affected_parts": ["leaves"], "severity": "mild", "image_quality": "good"}''',
        # Stage 2
        '''{
            "symptoms_observed": ["yellow leaves"],
            "image_quality": "good",
            "possible_diseases": [
                {
                    "name": "Cassava Mosaic Disease",
                    "likelihood": "high",
                    "source": "Mock Document",
                    "treatment_organic": ["Remove plant"],
                    "treatment_chemical": [],
                    "dosage": null,
                    "precautions": ["Wear gloves"]
                }
            ],
            "confidence_level": "high",
            "expert_referral_recommended": false,
            "transparency_label": "Mock Label",
            "retake_guidance": null
        }'''
    ]
    
    mock_rag.return_value = "Mock RAG Document Text"
    
    # Create dummy image file
    files = {"file": ("test.jpg", b"dummy_image_bytes", "image/jpeg")}
    
    response = client.post("/diagnose/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["image_quality"] == "good"
    assert data["symptoms_observed"] == ["yellow leaves"]
    assert data["possible_diseases"][0]["name"] == "Cassava Mosaic Disease"
    
    # Verify exact number of Bedrock calls (1 for vision, 1 for synthesis)
    assert mock_bedrock.call_count == 2
    mock_rag.assert_called_once_with("yellow leaves", top_k=5)

def test_diagnosis_endpoint_poor_quality(mock_bedrock):
    # Mock Stage 1 Response stating poor quality
    mock_bedrock.return_value = '''{"symptoms": [], "affected_parts": [], "severity": "mild", "image_quality": "poor"}'''
    
    files = {"file": ("blurry.jpg", b"dummy_bytes", "image/jpeg")}
    
    response = client.post("/diagnose/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["image_quality"] == "poor"
    assert "retake" in data["retake_guidance"].lower()
    
    # Verify Bedrock stopped after stage 1
    assert mock_bedrock.call_count == 1

def test_diagnosis_endpoint_invalid_file_type():
    files = {"file": ("test.txt", b"dummy_text", "text/plain")}
    response = client.post("/diagnose/", files=files)
    
    assert response.status_code == 400
    assert "not an image" in response.json()["detail"].lower()
