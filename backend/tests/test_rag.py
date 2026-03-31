import pytest
from app.services.rag import symptom_query
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_chromadb():
    with patch("app.services.rag.get_db_client") as mock_db, \
         patch("app.services.rag.get_embedding_model") as mock_model:
        
        # Setup mock document chunks returning from DB
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "documents": [
                [
                    "Document chunk 1 about Cassava Mosaic Disease",
                    "Document chunk 2 detailing treatment",
                    "Document chunk 3 precautions"
                ]
            ]
        }
        
        db_instance = MagicMock()
        db_instance.get_collection.return_value = mock_collection
        mock_db.return_value = db_instance
        
        # Mock embedding model
        model_instance = MagicMock()
        model_instance.encode.return_value = [0.1, 0.2, 0.3]
        mock_model.return_value = model_instance
        
        yield mock_collection

def test_rag_symptom_query_structuring(mock_chromadb):
    result = symptom_query("yellow leaves on my cassava plant", top_k=3)
    
    # Needs to concatenate the documents using the '\n\n---\n\n' divider
    assert "Document chunk 1" in result
    assert "---" in result
    assert "Document chunk 2" in result
    assert "Document chunk 3" in result
    
    mock_chromadb.query.assert_called_once()
    
def test_rag_empty_results():
    with patch("app.services.rag.get_db_client") as mock_db, \
         patch("app.services.rag.get_embedding_model"):
        
        mock_collection = MagicMock()
        mock_collection.query.return_value = {"documents": []}
        
        db_instance = MagicMock()
        db_instance.get_collection.return_value = mock_collection
        mock_db.return_value = db_instance
        
        result = symptom_query("unknown symptom", top_k=5)
        assert result == "No relevant agricultural knowledge found."
