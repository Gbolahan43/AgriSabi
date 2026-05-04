from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import chat, voice, diagnose, weather, market, history, assistant

app = FastAPI(
    title="AgriSabi API",
    description="Enterprise AI for African Agriculture - v1.1",
    version="1.1.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS.split(","),
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all endpoint routes
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(voice.router, prefix="/voice", tags=["voice"])
app.include_router(diagnose.router, prefix="/diagnose", tags=["diagnose"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(market.router, prefix="/market", tags=["market"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])

@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.1.0"}
