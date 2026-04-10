import boto3
from ..config import settings

client = None

def get_polly_client():
    global client
    if not client:
        client = boto3.client('polly', region_name=settings.AWS_REGION)
    return client

def synthesize_speech(text: str, language_code: str = 'en-US') -> bytes:
    
    voice_map = {
        'ha': 'Amina',      # Hausa (closest neural)
        'yo': 'Ayanda',     # Yoruba (South African fallback)
        'ig': 'Ayanda',     # Igbo fallback
        'en': 'Joanna',     # Standard
        'pcm': 'Kemi'       # Nigerian English/Pidgin
    }
    
    voice_id = voice_map.get(language_code, 'Joanna')
    
    try:
        polly = get_polly_client()
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',  # ✅ Frontend-ready
            VoiceId=voice_id,
            Engine='neural'
        )
        return response["AudioStream"].read()
    except Exception as e:
        print(f"Polly Synthesis Error: {e}")
        return None
