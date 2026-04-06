import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

def test_voice_endpoint_tier_1():
    """
    Tier 1 (English/Pidgin): The voice agent returns an error directing user to WebSocket.
    The route must propagate this as a 422 HTTPException.
    """
    with patch("app.api.routes.voice.voice_agent.handle", new_callable=AsyncMock) as mock_handle:
        mock_handle.return_value = {"error": "Use the /assistant/stream WebSocket endpoint for Nova Sonic."}

        files = {"file": ("audio.wav", b"dummy_audio_bytes", "audio/wav")}
        response = client.post("/voice/", files=files)

        assert response.status_code == 422
        assert "WebSocket endpoint" in response.json()["detail"]
        mock_handle.assert_called_once()


def test_voice_endpoint_tier_2():
    """
    Tier 2 (Hausa/Yoruba/Igbo): Full transcription pipeline runs end-to-end.
    The route returns transcript + response text.
    """
    with patch("app.api.routes.voice.voice_agent.handle", new_callable=AsyncMock) as mock_handle:
        mock_handle.return_value = {
            "transcript": "Sannu, mene ne wannan ciwo a kan masara ta?",
            "response": "Wannan ciwon yana kama da...",
            "audio_url": "https://s3.placeholder.url/audio.mp3"
        }

        files = {"file": ("hausa_query.wav", b"dummy_audio_bytes", "audio/wav")}
        response = client.post("/voice/", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["transcript"] == "Sannu, mene ne wannan ciwo a kan masara ta?"
        assert data["response"] == "Wannan ciwon yana kama da..."
        mock_handle.assert_called_once()


def test_voice_endpoint_invalid_file_type():
    """Uploading a non-audio file must immediately return 400."""
    files = {"file": ("test.txt", b"dummy_text", "text/plain")}
    response = client.post("/voice/", files=files)

    assert response.status_code == 400
    assert "isn't an audio stream" in response.json()["detail"].lower()
