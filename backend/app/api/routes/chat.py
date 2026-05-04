import re
from fastapi import APIRouter, HTTPException, File, UploadFile
from ...services.transcribe import transcribe_audio
from ...models.schemas import ChatRequest, ChatResponse
from ...orchestration.agents import advisory_agent

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main Chat Endpoint: Handles text-based advisory queries from the Omni-Chat UI.
    Routes through the Advisory Agent with weather & soil tool support.
    """
    try:
        payload = {
            "message": request.message,
            "session_id": "default_session",
        }
        result = await advisory_agent.handle(payload)

        if "error" in result:
            raise HTTPException(status_code=502, detail=result["error"])

        # Strip any <thinking> internal blocks from Claude
        response_text = result.get("message", "")
        response_text = re.sub(r'<thinking>.*?</thinking>', '', response_text, flags=re.DOTALL).strip()

        # Advisory agent returns {"message": "..."}, schema expects {"response": "..."}
        return ChatResponse(response=response_text)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    """Receives audio file from browser and returns text transcription."""
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Must be an audio file.")
        
    try:
        audio_bytes = await file.read()
        text = await transcribe_audio(audio_bytes)
        return {"text": text.strip()}
    except Exception as e:
        print(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")
