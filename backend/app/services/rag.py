import os
import boto3

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=os.getenv("AWS_REGION", "us-east-1"))
KB_ID = os.getenv("KNOWLEDGE_BASE_ID")

def symptom_query(symptoms: str) -> str:
    """
    Stage 2 Diagnosis Helper: Retrieves top matching chunks from OpenSearch via Bedrock KB 
    based on the raw visual symptoms extracted by Claude 3.5 Sonnet Vision.
    """
    if not KB_ID:
        return "Error: KNOWLEDGE_BASE_ID not configured."
        
    try:
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=KB_ID,
            retrievalQuery={'text': symptoms},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )
        results = response.get('retrievalResults', [])
        chunks = [r['content']['text'] for r in results]
        return "\n\n---\n\n".join(chunks) if chunks else "No relevant agricultural documents found matching these symptoms."
    except Exception as e:
        print(f"RAG Retrieval Error: {e}")
        return "Error connecting to the IITA/NCRI Knowledge Base."

def context_prefetch(user_profile: str = "") -> str:
    """
    Nova Sonic Helper: Prefetch broader farming context to inject into 
    the system prompt before opening the WebSocket stream.
    """
    if not KB_ID:
        return "General Nigerian agriculture context unavailable."
        
    query = "Nigeria smallholder farming seasonal advice common crop diseases"
    if user_profile:
         query = f"Nigeria farming {user_profile} seasonal advice"
         
    try:
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=KB_ID,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 8
                }
            }
        )
        results = response.get('retrievalResults', [])
        chunks = [r['content']['text'] for r in results]
        return "\n\n".join(chunks)
    except Exception as e:
        print(f"RAG Context Error: {e}")
        return ""
