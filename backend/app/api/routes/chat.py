from fastapi import APIRouter, HTTPException
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

        # Advisory agent returns {"message": "..."}, schema expects {"response": "..."}
        return ChatResponse(response=result.get("message", ""))

    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat route error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
