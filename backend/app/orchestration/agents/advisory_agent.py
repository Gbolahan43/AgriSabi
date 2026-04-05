# Advisory Chat Flow with Native Weather Tool Injection
import boto3
import os
import asyncio
from app.config import settings
from app.core.guardrails import guardrail
from app.core.prompts import ADVISORY_SYSTEM_PROMPT
from app.services import dynamo
from app.services.weather import get_current_weather
from app.services.soil import get_soil_data

bedrock_client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION", "us-east-1"))
MODEL_ID = os.getenv("FALLBACK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

TOOL_CONFIG = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_current_weather",
                "description": "Get the current weather conditions for a specific location in Nigeria.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "location_name": {
                                "type": "string",
                                "description": "The name of the city, LGA, or state in Nigeria"
                            }
                        },
                        "required": ["location_name"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "get_soil_data",
                "description": "Extract the specific soil pH and characteristics by providing exact GPS coordinates.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude coordinate of the farm"
                            },
                            "longitude": {
                                "type": "number",
                                "description": "Longitude coordinate of the farm"
                            }
                        },
                        "required": ["latitude", "longitude"]
                    }
                }
            }
        }
    ]
}

async def handle(payload: dict):
    """
    Handle advisory flow with manual Converse API tool looping.
    """
    session_id = payload.get("session_id", "default_session")
    message = payload.get("message", "")
    
    # 1. Engage Native Guardrail 
    guardrail.analyze(message)
    
    # 2. Fetch history
    history = dynamo.get_session_history(session_id)
    messages = history + [{"role": "user", "content": [{"text": message}]}]
    
    print(f"Invoking Bedrock for session: {session_id}")
    
    # 3. First Converse Pass
    try:
        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=messages,
            system=[{"text": ADVISORY_SYSTEM_PROMPT}],
            toolConfig=TOOL_CONFIG,
            inferenceConfig={"maxTokens": 1000, "temperature": 0.2}
        )
    except Exception as e:
        print(f"Bedrock Error: {e}")
        return {"error": "Failed to connect to the AI core"}

    output_message = response['output']['message']
    
    # 4. Check for Tool Use
    if any(item.get('toolUse') for item in output_message['content']):
        # Append assistant's tool-use message to history
        messages.append(output_message)
        
        tool_results = []
        for block in output_message['content']:
            if 'toolUse' in block:
                tool_use = block['toolUse']
                
                if tool_use['name'] == 'get_current_weather':
                    location = tool_use['input'].get('location_name')
                    tool_data = get_current_weather(location)
                
                elif tool_use['name'] == 'get_soil_data':
                    lat = tool_use['input'].get('latitude')
                    lon = tool_use['input'].get('longitude')
                    tool_data = get_soil_data(lat, lon)
                else:
                    tool_data = "Unknown tool requested."
                    
                tool_results.append({
                    "toolResult": {
                        "toolUseId": tool_use['toolUseId'],
                        "content": [{"json": {"result": tool_data}}]
                    }
                })
                    
        # Append tool results
        messages.append({"role": "user", "content": tool_results})
        
        # 5. Second Converse Pass
        try:
            response2 = bedrock_client.converse(
                modelId=MODEL_ID,
                messages=messages,
                system=[{"text": ADVISORY_SYSTEM_PROMPT}],
                inferenceConfig={"maxTokens": 1000, "temperature": 0.2}
            )
            final_text = response2['output']['message']['content'][0]['text']
        except Exception as e:
            print(f"Bedrock Error 2: {e}")
            final_text = "I received the data but failed to process it."
            
    else:
        final_text = output_message['content'][0]['text']

    # 6. Save State Non-Blocking
    def save_to_db():
        dynamo.save_interaction(session_id, message, final_text)
        
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, save_to_db)
    
    return {"message": final_text}
