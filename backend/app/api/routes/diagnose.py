from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Optional
from ...orchestration.agents import diagnosis_agent
from ...models.schemas import DiagnosisResponse

router = APIRouter()

@router.post("/", response_model=DiagnosisResponse)
async def diagnose_endpoint(
    file: UploadFile = File(...),
    text: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Two-Stage Diagnosis API
    Takes an image upload, passes it through the orchestration layer where
    Stage 1 extracts symptoms using Claude 3.5 Sonnet Vision and Stage 2 matches 
    them against the Bedrock Knowledge Base (OpenSearch Serverless).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded was not an image.")
        
    try:
        # Route directly to the diagnosis agent, passing the new text and session_id
        result = await diagnosis_agent.handle(file, text, session_id)
        
        if "error" in result:
            raise HTTPException(status_code=422, detail=result["error"])
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Diagnose Route Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during diagnosis")
