import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_rag_prefetch():
    with patch("app.orchestration.agents.assistant_agent.context_prefetch") as mock:
        mock.return_value = "Cassava requires well-drained soil."
        yield mock


@pytest.fixture
def mock_nova_sonic():
    with patch("app.orchestration.agents.assistant_agent.attach_websocket_to_nova", new_callable=AsyncMock) as mock:
        yield mock


def test_assistant_websocket(mock_rag_prefetch, mock_nova_sonic):
    """
    Tests the /assistant/stream WebSocket endpoint.
    Validates: RAG is prefetched, Nova Sonic is called with the enriched prompt,
    and the first message confirms initialization.
    """
    with client.websocket_connect("/assistant/stream?session_id=test123") as ws:
        # First server message must be the initialization confirmation
        data = ws.receive_text()
        assert data == "Nova Sonic Session Initialized"

        # Confirm RAG was invoked before opening the stream
        mock_rag_prefetch.assert_called_once()

        # Confirm Nova Sonic was invoked
        mock_nova_sonic.assert_called_once()

        # Confirm the enriched prompt contains our RAG data
        call_args = mock_nova_sonic.call_args
        # 3rd positional arg (index 2) is the enriched system_prompt
        passed_prompt = call_args[0][2]
        assert "Cassava requires well-drained soil." in passed_prompt
        assert "AgriSabi" in passed_prompt
