from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's input message")
    language: Optional[str] = Field("English", description="The language preference, e.g., 'English', 'Nigerian Pidgin'")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI generated response")

class VoiceResponse(BaseModel):
    audio_url: str = Field(..., description="URL to the generated speech audio")
    transcript: str = Field(..., description="Text transcript of the response")
    response: str = Field(..., description="AI text response")

class DiagnosisResponse(BaseModel):
    disease: str
    confidence: int
    scientific_name: Optional[str] = None
    symptoms: List[str]
    organic_treatments: List[str]
    chemical_treatments: List[str]

class MarketPrice(BaseModel):
    price_per_kg: float
    price_per_bag: float
    trend: str
    market_name: str
    state: str
    last_updated: str
    source: str

class MarketResponse(BaseModel):
    prices: List[MarketPrice]
