from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...orchestration.agents import assistant_agent

router = APIRouter()

@router.websocket("/stream")
async def assistant_stream(websocket: WebSocket, session_id: str = "anon"):
    """
    WebSocket endpoint for the Live Nova Sonic Assistant
    User Profile can be passed in securely via dependencies in Phase 3.
    """
    # Dummy user profile for MVP logic testing
    dummy_profile = {
        "primary_crops": ["cassava", "yam"],
        "lga": "Lagos"
    }
    
    await assistant_agent.handle_websocket(
        websocket=websocket,
        session_id=session_id,
        user_profile=dummy_profile
    )
