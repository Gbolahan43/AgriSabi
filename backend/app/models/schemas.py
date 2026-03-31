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

class DiseaseInfo(BaseModel):
    name: str
    likelihood: str
    source: str
    treatment_organic: List[str]
    treatment_chemical: List[str]
    dosage: Optional[str] = None
    precautions: List[str]

class DiagnosisResponse(BaseModel):
    symptoms_observed: List[str]
    image_quality: str
    possible_diseases: List[DiseaseInfo]
    confidence_level: str
    expert_referral_recommended: bool
    transparency_label: str
    retake_guidance: Optional[str] = None

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
