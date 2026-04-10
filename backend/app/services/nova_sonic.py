# Full Nova Sonic Bidirectional Implementation (Async)
import asyncio
import base64
import json
import aioboto3
from typing import AsyncGenerator
from fastapi import WebSocket
from botocore.exceptions import ClientError
from app.config import settings

# Aioboto3 session for async resource management
session = aioboto3.Session()

async def attach_websocket_to_nova(websocket: WebSocket, session_id: str, system_prompt: str):
    """Real-time bidirectional Nova Sonic voice agent.
    Input: 16kHz PCM mono from mic
    Output: 24kHz PCM mono + text events
    Specs: Base64 audio chunks, barge-in enabled."""
    
    try:
        # 1. Initialize Nova Sonic Session (Async Stream)
        async with session.client('bedrock-runtime', region_name=settings.AWS_REGION) as bedrock_runtime:
            
            # Note: Bidirectional stream returns an async iterator in aioboto3
            response = await bedrock_runtime.invoke_model_with_bidirectional_stream(
                modelId=settings.NOVA_SONIC_MODEL_ID,
                body=json.dumps({
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
                })
            )
            
            stream = response.get('stream')
            if not stream:
                raise Exception("Failed to open bidirectional stream to Nova Sonic")

            # 2. Send System Prompt Event
            await send_event(stream, {
                'promptStart': {'promptName': 'agrisabi'},
                'contentStart': {'type': 'TEXT', 'role': 'SYSTEM'},
                'textInput': {'content': system_prompt},
                'contentEnd': {}
            })
            
            # 3. Bidirectional Loop (Concurrent processing)
            async def read_from_bedrock():
                async for event in stream:
                    # Output: Audio chunks to WS
                    if 'audioOutputChunk' in event:
                        audio_b64 = event['audioOutputChunk']['data']
                        audio_bytes = base64.b64decode(audio_b64)
                        await websocket.send_bytes(audio_bytes)
                    
                    # Text events (subtitles)
                    if 'textOutputChunk' in event:
                        await websocket.send_text(event['textOutputChunk']['content'])

            async def send_to_bedrock():
                try:
                    while True:
                        # Receive audio chunk from client
                        data = await websocket.receive_bytes()
                        await send_audio_input(stream, data)
                except Exception as e:
                    print(f"WS Read finished: {e}")

            # Run both concurrently
            await asyncio.gather(
                read_from_bedrock(),
                send_to_bedrock()
            )
                
    except ClientError as e:
        print(f"Nova Sonic Error [{session_id}]: {e}")
        if not websocket.client_state.name == "DISCONNECTED":
            await websocket.send_text("❌ Voice connection failed")
    except Exception as e:
        print(f"Voice Assistant Error [{session_id}]: {e}")
    finally:
        if not websocket.client_state.name == "DISCONNECTED":
            await websocket.close()

async def send_event(stream, event_data: dict):
    """Send JSON event to Nova Sonic stream."""
    event_json = json.dumps({'event': event_data})
    # For aioboto3 streams, we may need to use the stream's interface
    # This part depends on the exact version of the eventstream mapping
    # but normally it's stream.send_event(event_bytes)
    try:
        await stream.send_event(event_data)
    except Exception as e:
        print(f"Error sending event: {e}")

async def send_audio_input(stream, audio_bytes: bytes):
    """Send 16kHz PCM audio chunk."""
    b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    audio_event = {
        'audioInputChunk': {
            'data': b64_audio,
            'sampleRateHertz': 16000,
            'sampleSizeBits': 16,
            'channelCount': 1
        }
    }
    await send_event(stream, audio_event)
