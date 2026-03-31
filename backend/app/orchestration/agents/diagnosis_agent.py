import json
from ...core.prompts import SYMPTOM_EXTRACTION_PROMPT, TREATMENT_SYNTHESIS_PROMPT
from ...services.bedrock import invoke_converse
from ...services.rag import symptom_query
from ...models.schemas import DiagnosisResponse
from fastapi import UploadFile
from ...services.vision import encode_image, get_image_media_type

async def handle(file: UploadFile) -> dict:
    # 1. Read and process image
    image_bytes = await encode_image(file)
    image_format = get_image_media_type(file.filename)
    
    # 2. STAGE 1 - SYMPTOM EXTRACTION (Vision)
    messages_stage_1 = [
        {
            "role": "user",
            "content": [
                {
                    "image": {
                        "format": image_format,
                        "source": {"bytes": image_bytes}
                    }
                },
                {
                    "text": "Please analyze this crop image and output the symptoms strictly according to the system prompt JSON schema."
                }
            ]
        }
    ]
    
    print("Executing Stage 1: Symptom Extraction...")
    stage_1_response = await invoke_converse(
        messages=messages_stage_1,
        system_prompt=SYMPTOM_EXTRACTION_PROMPT
    )
    
    if not stage_1_response:
        return {"error": "Failed to extract symptoms from the image"}
        
    try:
        # Claude returns markdown wrapped JSON sometimes, stripping it
        cleaned_json = stage_1_response.replace("```json", "").replace("```", "").strip()
        symptoms_data = json.loads(cleaned_json)
    except Exception as e:
        print(f"Failed to parse Stage 1 JSON: {e}")
        return {"error": "Failed to parse symptom data"}
        
    # Check image quality hook
    if symptoms_data.get("image_quality") == "poor":
        return {
            "symptoms_observed": [],
            "image_quality": "poor",
            "possible_diseases": [],
            "confidence_level": "low",
            "expert_referral_recommended": True,
            "transparency_label": "AI-assisted screening. Confirm with your extension worker before treating high-value crops.",
            "retake_guidance": "The image quality is too poor to analyze. Please retake the photo ensuring it is well-lit and the crop symptoms are clearly visible."
        }
        
    # 3. STAGE 2 - RAG DISEASE MATCHING
    symptoms_list = symptoms_data.get("symptoms", [])
    if not symptoms_list:
        return {"error": "No visible symptoms found to analyze"}
        
    symptoms_text = ", ".join(symptoms_list)
    print(f"Symptoms found: {symptoms_text}")
    print("Executing Stage 2: Knowledge Base Retrieval...")
    
    # Retrieve from ChromaDB
    context_chunks = symptom_query(symptoms_text, top_k=5)
    
    # Format the prompt
    synthesis_prompt = TREATMENT_SYNTHESIS_PROMPT.replace(
        "{context}", context_chunks
    ).replace(
        "{symptoms_text}", symptoms_text
    )
    
    messages_stage_2 = [
        {
            "role": "user",
            "content": [{"text": f"Based on these symptoms: {symptoms_text}, what diseases match from the retrieved context? Remember to output strictly matching the JSON schema."}]
        }
    ]
    
    print("Executing Stage 2: Treatment Synthesis...")
    stage_2_response = await invoke_converse(
        messages=messages_stage_2,
        system_prompt=synthesis_prompt
    )
    
    if not stage_2_response:
        return {"error": "Failed to synthesize treatment plan"}
        
    try:
        cleaned_response = stage_2_response.replace("```json", "").replace("```", "").strip()
        diagnosis_data = json.loads(cleaned_response)
        
        # Override image_quality from stage 1 just to be accurate
        diagnosis_data["image_quality"] = symptoms_data.get("image_quality", "acceptable")
        
        return diagnosis_data
    except Exception as e:
        print(f"Failed to parse Stage 2 JSON: {e}")
        return {"error": "Failed to parse diagnosis output"}
