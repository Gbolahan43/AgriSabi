from fastapi import APIRouter, File, UploadFile, HTTPException
from ...orchestration.agents import voice_agent
from ...models.schemas import VoiceResponse

router = APIRouter()

@router.post("/", response_model=VoiceResponse)
async def voice_endpoint(file: UploadFile = File(...)):
    """
    Handles standard standard voice requests (Tier 1 vs Tier 2 routing).
    Expects single audio file upload.
    For live bidirectional Assistant, the client calls /assistant/stream instead.
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Uploaded file isn't an audio stream.")
        
    try:
        audio_bytes = await file.read()
        
        # Pass to Voice Agent
        result = await voice_agent.handle(audio_bytes)
        
        if "error" in result:
            raise HTTPException(status_code=422, detail=result["error"])
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Voice route error: {e}")
        raise HTTPException(status_code=500, detail="Failed to synthesize voice")
