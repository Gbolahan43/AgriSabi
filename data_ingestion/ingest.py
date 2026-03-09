import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client (persistent storage)
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=db_path)

# Initialize Sentence Transformer model
model_name = "all-MiniLM-L6-v2"  # Fast and effective for general sentence embeddings
print(f"Loading Sentence Transformer model: {model_name}...")
embedding_model = SentenceTransformer(model_name)

def get_or_create_collection(name="agrisabi_knowledge"):
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """A naive text chunking function to simulate document processing."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += (chunk_size - overlap)
    return chunks

def ingest_dummy_data():
    collection = get_or_create_collection()
    
    # Dummy IITA manual data about Cassava
    dummy_text = (
        "Cassava is an essential crop in Nigeria. "
        "For optimal yield, plant early in the rainy season. "
        "Apply NPK 15:15:15 fertilizer at 400kg per hectare. "
        "Weed farms 4 weeks after planting. "
        "If you spot Cassava Mosaic Disease, remove and burn infected plants immediately."
    )
    
    chunks = chunk_text(dummy_text, chunk_size=20, overlap=5)
    
    docs = []
    ids = []
    embeddings = []
    
    for i, chunk in enumerate(chunks):
        docs.append(chunk)
        ids.append(f"doc_cassava_001_chunk_{i}")
        
    print(f"Creating embeddings for {len(chunks)} chunks...")
    embeddings = embedding_model.encode(docs).tolist()
    
    print("Adding to ChromaDB...")
    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids
    )
    
    print("Ingestion complete. The database has been populated with dummy Cassava data.")

if __name__ == "__main__":
    ingest_dummy_data()
