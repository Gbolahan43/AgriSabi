import os
import json
import base64
import io
import boto3
from PIL import Image
from fastapi import UploadFile
from app.config import settings
from ...services.rag import symptom_query
from app.services.vision import encode_image, get_image_media_type

SONNET_MODEL = settings.PRIMARY_MODEL_ID

def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION", "us-west-2"))

SYMPTOM_EXTRACTION_PROMPT = """
You are an expert crop pathologist. You are looking at a photo taken by a farmer.
Your task is ONLY to extract visual symptoms. DO NOT name a disease. DO NOT offer arbitrary treatment.
Describe color changes, spots, lesions, patterns, and which parts of the plant are affected.

You must reply strictly in the following JSON format:
{
  "symptoms": ["list", "of", "raw", "visual", "observations"],
  "affected_parts": ["leaves", "stem", "fruit"],
  "severity": "mild/moderate/severe",
  "image_quality": "good/acceptable/poor"
}
"""

TREATMENT_SYNTHESIS_PROMPT = """
You are AgriSabi, a trusted agricultural AI. Given the following raw symptoms extracted from a crop, 
and the retrieved knowledge snippets below (which come from verified IITA/NCRI agricultural manuals), 
determine the most likely disease(s) and provide the correct organic and chemical treatments.

RULES:
1. You may ONLY name diseases that are mentioned in the retrieved knowledge snippets. If the symptoms don't match anything in the snippets, admit that the disease is not in your current agricultural database.
2. Provide a single structured JSON response exactly matching the defined schema.
3. Your tone should be serious and helpful.
4. Provide a confidence percentage between 0 and 100 based on how well the symptoms match the retrieved documents.

Retrieved KB Snippets:
{kb_context}

Raw Symptoms:
{raw_symptoms}

Respond strictly in the following JSON schema:
{{
    "disease": "string",
    "confidence": 0,
    "scientific_name": "string",
    "symptoms": ["string"],
    "organic_treatments": ["string"],
    "chemical_treatments": ["string"]
}}
"""

async def handle(file: UploadFile) -> dict:
    image_bytes = await encode_image(file)  
    media_type = get_image_media_type(file.filename)  
    
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((1024, 1024), Image.Resampling.LANCZOS)  
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=85)  
    img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    fmt = media_type.split("/")[-1]
    if fmt == "jpg":
        fmt = "jpeg"
        
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "image": {
                        "format": fmt,
                        "source": {
                            "bytes": buffered.getvalue()
                        }
                    }
                },
                {
                    "text": SYMPTOM_EXTRACTION_PROMPT
                }
            ]
        }
    ]
    
    try:
        response = get_bedrock_client().converse(
            modelId=SONNET_MODEL,
            messages=messages,
            inferenceConfig={"maxTokens": 500, "temperature": 0.1}
        )
        stage1_output = response['output']['message']['content'][0]['text'].strip()
        
        if "```json" in stage1_output:
            stage1_output = stage1_output.split("```json")[1].split("```")[0].strip()
        elif "```" in stage1_output:
            stage1_output = stage1_output.split("```")[1].split("```")[0].strip()
            
        extraction = json.loads(stage1_output)
        
        if extraction.get("image_quality") == "poor":
            return {"error": "Image is too blurry..."}
        
        symptom_string = ", ".join(extraction.get("symptoms", []))
        
    except Exception as e:  # KEEP
        print(f"Stage 1 Error: {e}")
        return {"error": "Failed to analyze image visually."}
    
    try: 
        
        kb_context = symptom_query(symptom_string)

        synthesis_prompt = TREATMENT_SYNTHESIS_PROMPT.format(
            kb_context=kb_context,
            raw_symptoms=symptom_string
        )
        
        response2 = get_bedrock_client().converse(
            modelId=SONNET_MODEL,
            messages=[{"role": "user", "content": [{"text": synthesis_prompt}]}],
            inferenceConfig={"maxTokens": 1000, "temperature": 0.2}
        )
        
        final_diagnosis_str = response2['output']['message']['content'][0]['text'].strip()
        
        if "```json" in final_diagnosis_str:
            final_diagnosis_str = final_diagnosis_str.split("```json")[1].split("```")[0].strip()
        elif "```" in final_diagnosis_str:
            final_diagnosis_str = final_diagnosis_str.split("```")[1].split("```")[0].strip()
            
        return json.loads(final_diagnosis_str)
        
    except Exception as e:
        print(f"Stage 2 Error: {e}")
        return {"error": "Failed to resolve symptoms against the knowledge base."}
