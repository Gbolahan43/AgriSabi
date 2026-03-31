from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def voice_endpoint():
    return {"message": "Voice endpoint scaffolded"}
