# Previous ai_service logic shifted here for advisory chat flow

import boto3
import os
import asyncio
from app.config import settings
from app.core.guardrails import guardrail
from app.core.prompts import ADVISORY_SYSTEM_PROMPT
from app.services import dynamo
from app.services.bedrock import invoke_converse

async def handle(payload: dict):
    """
    Handle generic chat or advisory flow with memory.
    """
    session_id = payload.get("session_id", "default_session")
    message = payload.get("message", "")
    
    # 1. Engage Native Guardrail 
    guardrail.analyze(message)
    
    # 2. Fetch history
    history = dynamo.get_session_history(session_id)
    
    # 3. Append current message to payload sent to AWS
    messages = history + [{"role": "user", "content": [{"text": message}]}]
    
    # 4. Invoke Claude with strict linguistic prompt
    print(f"Invoking Bedrock for session: {session_id}")
    response_text = await invoke_converse(
        messages=messages,
        system_prompt=ADVISORY_SYSTEM_PROMPT
    )
    
    if not response_text:
        return {"error": "Failed to generate advisory response."}
        
    # 5. Save the interaction in the background so we don't block the return
    def save_to_db():
        dynamo.save_interaction(session_id, message, response_text)
        
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, save_to_db)
    
    return {"message": response_text}
