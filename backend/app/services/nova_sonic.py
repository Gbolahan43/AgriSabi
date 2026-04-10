# Full Nova Sonic Bidirectional Implementation
import asyncio
import base64
import json
from typing import AsyncGenerator
from fastapi import WebSocket
from botocore.exceptions import ClientError
from app.config import settings
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
NOVA_SONIC_MODEL_ID = settings.NOVA_SONIC_MODEL_ID

async def attach_websocket_to_nova(websocket: WebSocket, session_id: str, system_prompt: str):
    """Real-time bidirectional Nova Sonic voice agent.
    Input: 16kHz PCM mono from mic
    Output: 24kHz PCM mono + text events
    Specs: Base64 audio chunks, barge-in enabled."""
    
    try:
        await websocket.accept()
        
        # 1. Initialize Nova Sonic Session (EventStream)
        stream = await bedrock_runtime.invoke_model_with_bidirectional_stream(
            modelId=NOVA_SONIC_MODEL_ID,
            body={
                'sessionStart': {
                    'inferenceConfiguration': {
                        'maxTokens': 1024,
                        'topP': 0.9,
                        'temperature': 0.7
                    },
                    'turnDetectionConfiguration': {
                        'endpointingSensitivity': 'HIGH'  # Barge-in
                    }
                }
            }
        )
        
        # 2. Send System Prompt
        await send_event(stream, {
            'promptStart': {'promptName': 'agrisabi'},
            'contentStart': {'type': 'TEXT', 'role': 'SYSTEM'},
            'textInput': {'content': system_prompt},
            'contentEnd': {}
        })
        
        # 3. Bidirectional Loop
        async for chunk in stream:
            event = json.loads(chunk)
            
            # Output: Audio chunks to WS
            if 'audioOutputChunk' in event:
                audio_b64 = event['audioOutputChunk']['data']
                audio_bytes = base64.b64decode(audio_b64)
                await websocket.send_bytes(audio_bytes)
            
            # Text events (subtitles)
            if 'textOutputChunk' in event:
                await websocket.send_text(event['textOutputChunk']['content'])
            
            # Receive input from WS
            try:
                input_audio = await asyncio.wait_for(websocket.receive_bytes(), timeout=1.0)
                await send_audio_input(stream, input_audio)
            except asyncio.TimeoutError:
                pass  # No input, continue listening
                
    except ClientError as e:
        print(f"Nova Sonic Error [{session_id}]: {e}")
        await websocket.send_text("❌ Voice connection failed")
    except Exception as e:
        print(f"WS Error [{session_id}]: {e}")
    finally:
        await websocket.close()

async def send_event(stream, event_data: dict):
    """Send JSON event to Nova Sonic stream."""
    event_json = json.dumps({'event': event_data})
    stream.send_event(event_json.encode())

async def send_audio_input(stream, audio_bytes: bytes):
    """Send 16kHz PCM audio chunk."""
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_event = {
        'audioInputChunk': {
            'data': b64_audio,
            'sampleRateHertz': 16000,
            'sampleSizeBits': 16,
            'channelCount': 1
        }
    }
    await send_event(stream, audio_event)
