import boto3
import json
from ..config import settings

client = None

def get_bedrock_client():
    global client
    if not client:
        client = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
    return client

async def invoke_converse(messages: list, system_prompt: str, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"):
    """
    Wrapper for Amazon Bedrock Converse API supporting text and vision inputs.
    """
    bedrock = get_bedrock_client()
    
    try:
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
            system=[{"text": system_prompt}],
            inferenceConfig={
                "maxTokens": 4000,
                "temperature": 0.2, # Low temperature for accurate grounding
                "topP": 0.9
            }
        )
        
        # Bedrock Converse API returns the structured output
        output_text = response['output']['message']['content'][0]['text']
        return output_text
        
    except Exception as e:
        print(f"Bedrock Error: {e}")
        return None
