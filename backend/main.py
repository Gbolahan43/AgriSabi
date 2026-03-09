import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
import ai_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize connections, e.g. Chromadb and AWS Bedrock clients
    ai_service.initialize()
    yield
    # Cleanup on shutdown

app = FastAPI(lifespan=lifespan, title="AgriSabi API", description="Enterprise AI for African Agriculture")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AgriSabi API. Use /docs to test endpoints."}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response_text = await ai_service.generate_response(request.message, request.language)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
