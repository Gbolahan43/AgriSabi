import pytest
from app.services.rag import symptom_query, context_prefetch
import app.services.rag as rag_module
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_kb():
    rag_module.KB_ID = "mock_kb_id_for_testing"
    yield

def test_rag_symptom_query_structuring(mock_kb):
    with patch("app.services.rag.bedrock_agent_runtime") as mock_bedrock:
        mock_bedrock.retrieve.return_value = {
            "retrievalResults": [
                {"content": {"text": "Document chunk 1 about Cassava Mosaic Disease"}},
                {"content": {"text": "Document chunk 2 detailing treatment"}},
                {"content": {"text": "Document chunk 3 precautions"}}
            ]
        }
        
        result = symptom_query("yellow leaves on my cassava plant")
        
        assert "Document chunk 1" in result
        assert "---" in result
        assert "Document chunk 2" in result
        assert "Document chunk 3" in result
        mock_bedrock.retrieve.assert_called_once()

def test_rag_empty_results(mock_kb):
    with patch("app.services.rag.bedrock_agent_runtime") as mock_bedrock:
        mock_bedrock.retrieve.return_value = {"retrievalResults": []}
        
        result = symptom_query("unknown symptom")
        assert result == "No relevant agricultural documents found matching these symptoms."

def test_rag_context_prefetch(mock_kb):
    with patch("app.services.rag.bedrock_agent_runtime") as mock_bedrock:
        mock_bedrock.retrieve.return_value = {
            "retrievalResults": [
                {"content": {"text": "Context 1"}},
                {"content": {"text": "Context 2"}}
            ]
        }
        
        result = context_prefetch("urban farming")
        assert "Context 1\n\nContext 2" in result
        mock_bedrock.retrieve.assert_called_once()
