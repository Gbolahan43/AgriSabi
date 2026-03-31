import boto3
from ..config import settings

client = None

def get_polly_client():
    global client
    if not client:
        client = boto3.client('polly', region_name=settings.AWS_REGION)
    return client

def synthesize_speech(text: str, language_code: str = 'en-US') -> bytes:
    """
    Synthesize speech from text using Amazon Polly Neural voices.
    """
    # Mapping our internal language codes to Polly languages
    voice_map = {
        'ha': 'Amina',     # Mock or real if supported
        'yo': 'Ayanda',    # South African voice as placeholder if no Yor is available natively
        'ig': 'Ayanda',
        'en': 'Joanna',
        'pcm': 'Kemi'      # Nigerian English/Pidgin
    }
    
    voice_id = voice_map.get(language_code, 'Joanna')
    
    try:
        polly = get_polly_client()
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural'
        )
        
        if "AudioStream" in response:
            return response["AudioStream"].read()
        return None
    except Exception as e:
        print(f"Polly Synthesis Error: {e}")
        return None
