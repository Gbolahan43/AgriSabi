import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services import rag

client = TestClient(app)

@pytest.fixture
def mock_rag_prefetch():
    with patch("app.orchestration.agents.assistant_agent.context_prefetch") as mock:
        yield mock

@pytest.fixture
def mock_nova_sonic():
    with patch("app.orchestration.agents.assistant_agent.attach_websocket_to_nova") as mock:
        yield mock

def test_assistant_websocket(mock_rag_prefetch, mock_nova_sonic):
    # Mock RAG returning standard chunks
    mock_rag_prefetch.return_value = "Cassava requires well-drained soil."
    
    # We use FastAPI's built in TestClient for WebSockets
    with client.websocket_connect("/assistant/stream?session_id=123") as websocket:
        # First message is the initialization success
        data = websocket.receive_text()
        assert data == "Nova Sonic Session Initialized"
        
        # Ensure RAG was fetched before opening
        mock_rag_prefetch.assert_called_once()
        
        # Ensure attach_websocket_to_nova was invoked with the enriched prompt
        mock_nova_sonic.assert_called_once()
        args, kwargs = mock_nova_sonic.call_args
        assert "Cassava requires well-drained soil." in args[2] 
        assert "You are AgriSabi" in args[2]
