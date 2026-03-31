from ..services import transcribe, polly, nova_sonic
from .advisory_agent import handle as advisory_handle
from fastapi import WebSocket

async def handle(audio_bytes: bytes) -> dict:
    """
    Handles standard voice queries.
    Routes to Tier 1 or Tier 2 based on language detection.
    """
    lang_code, confidence = transcribe.identify_language(audio_bytes)
    
    # Tier 1 vs Tier 2 
    if confidence > 0.8 and lang_code in ["en", "pcm"]:
        # Tier 1 - Usually handled by WebSockets, falling back to straight Nova process
        return {"error": "Use the /assistant/stream WebSocket endpoint for Nova Sonic."}
    else:
        # Tier 2 - Full Transcribe Pipeline (Hausa/Yoruba/Igbo)
        text = transcribe.full_transcription(audio_bytes, lang_code)
        
        # Route to Advisory Agent to synthesize response based on text
        # (Mock payload schema)
        response_text = await advisory_handle({"message": text})
        
        audio_out = polly.synthesize_speech(str(response_text), lang_code)
        
        # In a real app we'd save the audio to S3 and return a URL
        return {
            "transcript": text,
            "response": response_text,
            "audio_url": "https://s3.placeholder.url/audio.mp3" # Mock
        }
