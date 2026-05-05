import boto3
import io
import base64
import uuid
import requests
import asyncio
from app.config import settings

transcribe = boto3.client('transcribe', region_name=settings.AWS_REGION)

async def transcribe_audio(audio_bytes: bytes, language: str = "en-US") -> str:
    """Real-time audio → text using Amazon Transcribe"""
    # Save temp to S3 (Transcribe requirement)
    s3 = boto3.client('s3')
    bucket = settings.S3_BUCKET
    key = f"transcribe/{uuid.uuid4()}.webm"
    s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes)
    
    job_name = f"agrisabi-{uuid.uuid4()}"
    
    # Simplified: Use batch for MVP
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{bucket}/{key}'},
        MediaFormat='webm',
        LanguageCode=language,
        OutputBucketName=bucket
    )
    
    # Poll for completion (async in prod)
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        await asyncio.sleep(1)
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # Fetch and parse JSON transcript
        response = requests.get(transcript_uri)
        return response.json()['results']['transcripts'][0]['transcript']
    
    return ""
