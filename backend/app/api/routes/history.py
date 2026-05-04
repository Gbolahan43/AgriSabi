from fastapi import APIRouter, HTTPException
from app.services.dynamo import get_session_history

router = APIRouter()

@router.get("/{session_id}")
async def get_history(session_id: str):
    """Fetch voice/text session history from DynamoDB"""
    if not session_id:
        raise HTTPException(400, "session_id required")
    
    history = get_session_history(session_id)
    return {"history": history, "session_id": session_id}
