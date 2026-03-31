from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def weather_endpoint():
    return {"message": "Weather endpoint scaffolded"}
