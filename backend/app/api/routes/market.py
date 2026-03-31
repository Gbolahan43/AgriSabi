from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def market_endpoint():
    return {"message": "Market endpoint scaffolded"}
