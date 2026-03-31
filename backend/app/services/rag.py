import chromadb
from sentence_transformers import SentenceTransformer
import os

# Get path to existing ChromaDB
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data_ingestion", "chroma_db")

client = None
embedding_model = None
collection_name = "agrisabi_knowledge"

def get_db_client():
    global client
    if not client:
        client = chromadb.PersistentClient(path=DB_PATH)
    return client

def get_embedding_model():
    global embedding_model
    if not embedding_model:
        # Lazy load to avoid massive startup overhead if not requested
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embedding_model

def symptom_query(symptoms_text: str, top_k: int = 5) -> str:
    """
    Search the local ChromaDB knowledge base for relevant chunks.
    Phase 2: Transitioning this to AWS OpenSearch in later sprints.
    """
    try:
        db = get_db_client()
        collection = db.get_collection(name=collection_name)
        model = get_embedding_model()
        
        # Embed the query
        query_embedding = model.encode([symptoms_text]).tolist()
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        if not results or not results['documents']:
            return "No relevant agricultural knowledge found."
            
        # Combine all retrieved text chunks into one string context
        retrieved_documents = results['documents'][0]
        context = "\n\n---\n\n".join(retrieved_documents)
        return context
        
    except Exception as e:
        print(f"RAG Error: {e}")
        return "Knowledge base unavailable at the moment."
