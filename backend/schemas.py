from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's input message")
    language: Optional[str] = Field("English", description="The language preference, e.g., 'English', 'Nigerian Pidgin'")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI generated response")
