# Previous ai_service logic shifted here for advisory chat flow

import boto3
import os
from app.config import settings
from app.core.guardrails import guardrail

client = None

def initialize():
    global client
    client = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)

async def handle(payload: dict):
    """
    Handle generic chat or advisory flow (formerly generate_response)
    """
    # 1. Engage Native Guardrail 
    message = payload.get("message", "")
    guardrail.analyze(message)
    # Logic to be implemented in Phase 2
    return {"message": "Advisory Agent Processed Request"}
