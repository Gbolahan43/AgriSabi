import asyncio
import json
from fastapi import WebSocket
from ...services.rag import context_prefetch
from ...core.prompts import NOVA_SONIC_SYSTEM_PROMPT
from ...services.nova_sonic import attach_websocket_to_nova

async def handle_websocket(websocket: WebSocket, session_id: str, user_profile: dict = None):
    """
    Tier 1 Voice & Live Assistant: Bridges a client WebSocket to Amazon Nova Sonic.
    Handles RAG pre-fetch and hands off to the bidirectional service.
    """
    # 1. RAG Pre-fetch
    print(f"Session {session_id}: Pre-fetching RAG context for Nova Sonic...")
    pre_fetched_chunks = context_prefetch(user_profile)
    
    # 2. Build Enriched System Prompt
    enriched_prompt = NOVA_SONIC_SYSTEM_PROMPT.replace(
        "{pre_fetched_chunks}", pre_fetched_chunks
    )
    
    # 3. Hand off to Nova Sonic Service for bidirectional streaming
    try:
        await attach_websocket_to_nova(websocket, session_id, enriched_prompt)
        
    except Exception as e:
        print(f"WebSocket Error: {e}")
        if not websocket.client_state.name == "DISCONNECTED":
            await websocket.close()
