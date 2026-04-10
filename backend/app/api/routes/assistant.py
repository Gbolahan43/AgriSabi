from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import uuid
from ...orchestration.agents import assistant_agent

router = APIRouter(prefix="/assistant")  

@router.websocket("/stream")
async def assistant_stream(websocket: WebSocket, session_id: str = Query("anon")):
    """Full Voice-to-Voice Nova Sonic WebSocket"""
    session_id = session_id or str(uuid.uuid4())
    dummy_profile = {"primary_crops": ["cassava", "yam"], "lga": "Lagos"}
    
    try:
        await assistant_agent.handle_websocket(websocket, session_id, dummy_profile)
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
