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

def context_prefetch(user_profile: dict = None) -> str:
    """
    RAG Pre-fetch for Nova Sonic sessions.
    Builds a query based on the user's primary crops or generic seasonal advice.
    """
    if user_profile and "primary_crops" in user_profile:
        crops = ", ".join(user_profile["primary_crops"])
        lga = user_profile.get("lga", "Nigeria")
        month = "current month" # Mock, in prod we'd use datetime.now().strftime('%B')
        query = f"{crops} {lga} {month} farming advice"
        top_k = 10
    else:
        # Anonymous user query
        query = "Nigeria smallholder farming seasonal advice common crop diseases"
        top_k = 8
        
    return symptom_query(query, top_k=top_k)
