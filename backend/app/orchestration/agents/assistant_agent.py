from fastapi import WebSocket
from ...services.rag import context_prefetch
from ...core.prompts import NOVA_SONIC_SYSTEM_PROMPT
from ...services.nova_sonic import attach_websocket_to_nova

async def handle_websocket(websocket: WebSocket, session_id: str, user_profile: dict = None):
    """
    Handles the standalone English Live AI Assistant session using Nova Sonic.
    Runs RAG pre-fetch at session start, then hands off to the bidirectional Bedrock stream.
    """
    await websocket.accept()
    
    # 1. RAG Pre-fetch
    print(f"Session {session_id}: Pre-fetching RAG context for Nova Sonic...")
    pre_fetched_chunks = context_prefetch(user_profile)
    
    # 2. Build Enriched System Prompt
    enriched_prompt = NOVA_SONIC_SYSTEM_PROMPT.replace(
        "{pre_fetched_chunks}", pre_fetched_chunks
    )
    
    # 3. Stream Audio Bidirectionally
    try:
        # Mocking the actual streaming logic from services.nova_sonic
        await websocket.send_text("Nova Sonic Session Initialized")
        await attach_websocket_to_nova(websocket, session_id, enriched_prompt)
        
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
        print(f"Session {session_id} cleanly closed.")
