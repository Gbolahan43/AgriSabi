import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_transcribe():
    with patch("app.services.transcribe.identify_language") as mock:
        yield mock

@pytest.fixture
def mock_transcribe_full():
    with patch("app.services.transcribe.full_transcription") as mock:
        yield mock

@pytest.fixture
def mock_advisory():
    with patch("app.orchestration.agents.voice_agent.advisory_handle", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_polly():
    with patch("app.services.polly.synthesize_speech") as mock:
        yield mock

def test_voice_endpoint_tier_1(mock_transcribe):
    # Tier 1 triggers when language is English/Pidgin and confidence > 0.8
    mock_transcribe.return_value = ("en", 0.95)
    
    files = {"file": ("audio.wav", b"dummy_audio_bytes", "audio/wav")}
    response = client.post("/voice/", files=files)
    
    # Tier 1 should return a 422 redirecting to the Nova Sonic WebSocket route
    assert response.status_code == 422
    assert "WebSocket endpoint" in response.json()["detail"]

def test_voice_endpoint_tier_2(mock_transcribe, mock_transcribe_full, mock_advisory, mock_polly):
    # Tier 2 triggers for Hausa/Yoruba/Igbo
    mock_transcribe.return_value = ("ha", 0.95)
    mock_transcribe_full.return_value = "Sannu, mene ne wannan ciwo a kan masara ta?"
    mock_advisory.return_value = "Wannan ciwon yana kama da..." # Mocked response
    mock_polly.return_value = b"mocked_mp3_audio_data"
    
    files = {"file": ("hausa_query.wav", b"dummy_audio_bytes", "audio/wav")}
    response = client.post("/voice/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == "Sannu, mene ne wannan ciwo a kan masara ta?"
    assert data["response"] == "Wannan ciwon yana kama da..."
    
    # Ensure correct pipeline flow
    mock_transcribe.assert_called_once()
    mock_transcribe_full.assert_called_once()
    mock_advisory.assert_called_once()
    mock_polly.assert_called_once()

def test_voice_endpoint_invalid_file_type():
    files = {"file": ("test.txt", b"dummy_text", "text/plain")}
    response = client.post("/voice/", files=files)
    
    assert response.status_code == 400
    assert "isn't an audio stream" in response.json()["detail"].lower()
