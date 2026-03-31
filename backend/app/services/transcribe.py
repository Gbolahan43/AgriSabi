import boto3

def get_transcribe_client():
    return boto3.client('transcribe')

def identify_language(audio_bytes: bytes) -> tuple[str, float]:
    """
    Analyze the first 2 seconds of audio to detect the language.
    Returns the language code (en, pcm, ha, yo, ig) and confidence score.
    Note: For MVP, returning a mock based on expected logic.
    """
    # Mock detection: Assumes English/Pidgin > 0.8 confidence by default
    # Real implementation would call Transcribe Streaming IdentifyLanguage
    return "en", 0.95

def full_transcription(audio_bytes: bytes, language_code: str) -> str:
    """
    Transcribe the full audio block using Transcribe.
    """
    # Mock text
    return "This is a transcribed sentence of the farmer's query."
