import boto3
import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from weather_tool import get_weather_data

# The model choice (Haiku is fast and cost-effective)
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
client = None
chroma_client = None
collection = None
embedding_model = None

def initialize():
    global client, chroma_client, collection, embedding_model
    # Boto3 will automatically use AWS credentials from environment or ~/.aws/credentials
    client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION", "us-east-1"))
    
    # Initialize ChromaDB and Embeddings
    print("Loading Sentence Transformer model...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data_ingestion", "chroma_db")
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="agrisabi_knowledge", metadata={"hnsw:space": "cosine"})

async def generate_response(user_input: str, language: str) -> str:
    """
    Generates a RAG-augmented response using AWS Bedrock Claude 3 Haiku, 
    with tools provided to the model.
    """
    if client is None:
        raise Exception("Bedrock client not initialized")
    
    # Retrieve Context from ChromaDB
    query_embedding = embedding_model.encode([user_input]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    
    context_chunks = results["documents"][0] if results["documents"] else []
    context_text = "\n".join(context_chunks)
    if not context_text:
        context_text = "No specific agricultural context found. Answer purely using general knowledge while staying helpful."
    
    system_prompt = f"You are AgriSabi, an agricultural extension agent for African smallholder farmers. Answer the user prompt using ONLY the provided context. Respond fluently in {language}. If the context is empty, simply tell the farmer that you don't have information about that right now."
    
    # We construct a prompt that includes context and the user query
    user_message = f"Context: {context_text}\n\nUser Question: {user_input}"
    
    # Tool definition for Claude 3
    tools = [
        {
            "toolSpec": {
                "name": "get_weather_data",
                "description": "Fetch current weather data for a specified location.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "City or location name"}
                        },
                        "required": ["location"]
                    }
                }
            }
        }
    ]

    messages = [
        {"role": "user", "content": [{"text": user_message}]}
    ]

    try:
        # First call to Bedrock
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            system=[{"text": system_prompt}],
            toolConfig={"tools": tools}
        )
        
        output_message = response['output']['message']
        messages.append(output_message) # Add to conversation history
        
        # Check if model wants to use a tool
        tool_results = []
        for content_block in output_message['content']:
            if 'toolUse' in content_block:
                tool_use = content_block['toolUse']
                tool_name = tool_use['name']
                tool_input = tool_use['input']
                
                print(f"Model requested tool: {tool_name} with input {tool_input}")
                
                if tool_name == 'get_weather_data':
                    location = tool_input.get('location')
                    weather_result = get_weather_data(location)
                    
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use['toolUseId'],
                            "content": [{"json": weather_result}]
                        }
                    })
        
        # If tools were used, send results back to model
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
            
            second_response = client.converse(
                modelId=MODEL_ID,
                messages=messages,
                system=[{"text": system_prompt}],
                toolConfig={"tools": tools}
            )
            output_message = second_response['output']['message']
            
        # Extract text response string
        text_response = next((content['text'] for content in output_message['content'] if 'text' in content), "No text produced.")
        return text_response
        
    except Exception as e:
        print(f"Bedrock API error: {e}")
        return f"An error occurred while generating a response: {str(e)}"
