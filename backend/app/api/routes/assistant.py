from fastapi import APIRouter

router = APIRouter()

@router.websocket("/stream")
async def assistant_stream():
    # WebSocket route placeholder
    pass
