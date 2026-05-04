"""
AgriSabi — Bedrock Vision Model Tester
=======================================
Tests every vision-capable model available on AWS Bedrock against a single image.
Place your test image in the same folder as this script and run:

    python test_vision_models.py --image your_image.jpg

Requirements:
    pip install boto3 Pillow

AWS credentials must be configured:
    aws configure  (or set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars)

The script will:
  1. Try every model in the MODELS list
  2. Print whether each model can analyze images
  3. Print the first 300 characters of each response
  4. Print a final summary table showing PASS / FAIL / SKIP per model
  5. Recommend the best model for AgriSabi based on results

"""

import boto3
import base64
import json
import time
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────

DEFAULT_REGION = "us-east-1"   # Change to af-south-1 once models are available there
                                # Note: Llama 4 and some newer models are only in us-east-1 currently
                                # Claude is available in af-south-1

TEST_PROMPT = (
    "You are an agricultural AI assistant. Look at this image carefully. "
    "Describe in detail: (1) what crop or plant you can see, "
    "(2) any visible symptoms, discolouration, spots, lesions, or abnormalities, "
    "(3) what disease or condition this might indicate. "
    "Be specific and detailed about what you observe visually."
)

# ─── Models to test ───────────────────────────────────────────────────────────
# Format: (display_name, model_id, supports_vision, notes)

MODELS = [
    # ── Claude 4.x family (Anthropic) ───────────────────────────────────────────
    (
        "Claude 4.5 Sonnet (Cross-Region)",
        "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        True,
        "Next-gen primary model"
    ),
    (
        "Claude 4.0 Sonnet (Cross-Region)",
        "us.anthropic.claude-sonnet-4-20250514-v1:0",
        True,
        "Fallback next-gen model"
    ),

    # ── Claude 3.5 family (Anthropic) ─────────────────────────────────────────
    (
        "Claude 3.5 Sonnet v2 (Cross-Region)",
        "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        True,
        "Primary AgriSabi model — best multimodal accuracy"
    ),
    (
        "Claude 3.5 Sonnet v2",
        "anthropic.claude-3-5-sonnet-20241022-v2:0",
        True,
        "Primary AgriSabi model — best multimodal accuracy"
    ),
    (
        "Claude 3.5 Sonnet v1",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        True,
        "Previous Sonnet — fallback if v2 unavailable"
    ),
    (
        "Claude 3.5 Haiku",
        "anthropic.claude-3-5-haiku-20241022-v1:0",
        True,
        "Fastest Claude with vision — good for high volume"
    ),
    (
        "Claude 3 Sonnet",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        True,
        "Older Sonnet — widely available across regions"
    ),
    (
        "Claude 3 Haiku",
        "anthropic.claude-3-haiku-20240307-v1:0",
        True,
        "Fastest and cheapest Claude with vision"
    ),
    (
        "Claude 3 Opus",
        "anthropic.claude-3-opus-20240229-v1:0",
        True,
        "Most capable older Claude — expensive"
    ),

    # ── Amazon Nova family ────────────────────────────────────────────────────
    (
        "Amazon Nova Pro (Cross-Region)",
        "us.amazon.nova-pro-v1:0",
        True,
        "AWS native multimodal — text, image, video"
    ),
    (
        "Amazon Nova Pro",
        "amazon.nova-pro-v1:0",
        True,
        "AWS native multimodal — text, image, video"
    ),
    (
        "Amazon Nova Lite",
        "amazon.nova-lite-v1:0",
        True,
        "Lightweight AWS native — fast and cheap"
    ),
    (
        "Amazon Nova Micro",
        "amazon.nova-micro-v1:0",
        False,
        "Text only — no vision capability"
    ),

    # ── Meta Llama 4 family ───────────────────────────────────────────────────
    (
        "Llama 4 Maverick 17B",
        "meta.llama4-maverick-17b-instruct-v1:0",
        True,
        "Natively multimodal MoE — 400B total params, 17B active"
    ),
    (
        "Llama 4 Scout 17B",
        "meta.llama4-scout-17b-instruct-v1:0",
        True,
        "Natively multimodal — 3.5M context window"
    ),

    # ── Meta Llama 3.2 family (previous multimodal) ───────────────────────────
    (
        "Llama 3.2 90B Vision (Cross-Region)",
        "us.meta.llama3-2-90b-instruct-v1:0",
        True,
        "Large Llama vision model"
    ),
    (
        "Llama 3.2 90B Vision",
        "meta.llama3-2-90b-instruct-v1:0",
        True,
        "Large Llama vision model"
    ),
    (
        "Llama 3.2 11B Vision",
        "meta.llama3-2-11b-instruct-v1:0",
        True,
        "Efficient Llama vision model"
    ),

    # ── Google (open-weight on Bedrock) ───────────────────────────────────────
    # Note: Gemini Pro/Ultra are Google Cloud only — NOT on AWS Bedrock
    # Gemma is available via SageMaker JumpStart but NOT directly on Bedrock Converse API
    # These are listed to confirm they are not testable via this script
    (
        "Google Gemini Pro [NOT ON BEDROCK]",
        "SKIP",
        False,
        "Gemini is Google Cloud exclusive — not available on AWS Bedrock"
    ),
    (
        "Google Gemma [JUMPSTART ONLY]",
        "SKIP",
        False,
        "Gemma is on SageMaker JumpStart — not on Bedrock Converse API"
    ),

    # ── OpenAI (not on Bedrock) ───────────────────────────────────────────────
    # Note: GPT-4o and GPT-4V are NOT on AWS Bedrock
    # The AWS/OpenAI partnership only brought text-only open-weight models
    (
        "OpenAI GPT-4o [NOT ON BEDROCK]",
        "SKIP",
        False,
        "GPT-4o is OpenAI API only — not available on AWS Bedrock"
    ),
    (
        "OpenAI gpt-oss-120b [TEXT ONLY]",
        "SKIP",
        False,
        "AWS/OpenAI partnership model — text only, no vision"
    ),
]

# ─── Colour helpers ───────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def green(s):  return f"{GREEN}{s}{RESET}"
def red(s):    return f"{RED}{s}{RESET}"
def yellow(s): return f"{YELLOW}{s}{RESET}"
def cyan(s):   return f"{CYAN}{s}{RESET}"
def bold(s):   return f"{BOLD}{s}{RESET}"
def dim(s):    return f"{DIM}{s}{RESET}"

# ─── Image loading ────────────────────────────────────────────────────────────

def load_image(image_path: str) -> tuple[bytes, str]:
    """Load image bytes and determine correct media type."""
    path = Path(image_path)

    if not path.exists():
        print(red(f"\n✗ Image not found: {image_path}"))
        print(yellow("  Place your test image in the same folder as this script."))
        print(yellow("  Supported: .jpg, .jpeg, .png, .gif, .webp\n"))
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_map = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".gif":  "image/gif",
        ".webp": "image/webp",
    }

    if suffix not in mime_map:
        print(red(f"\n✗ Unsupported image format: {suffix}"))
        print(yellow("  Use .jpg, .jpeg, .png, .gif, or .webp\n"))
        sys.exit(1)

    with open(path, "rb") as f:
        image_bytes = f.read()

    file_size_kb = len(image_bytes) / 1024
    media_type = mime_map[suffix]

    print(f"\n{bold('Image loaded:')}")
    print(f"  Path:       {path.resolve()}")
    print(f"  Format:     {media_type}")
    print(f"  Size:       {file_size_kb:.1f} KB")
    print(f"  Dimensions: checking...")

    # Try to get dimensions with Pillow if available
    try:
        from PIL import Image
        with Image.open(path) as img:
            w, h = img.size
            print(f"  Dimensions: {w} × {h} px")
            if w > 4000 or h > 4000:
                print(yellow(f"  ⚠  Image is very large ({w}×{h}). Consider resizing to 1024×1024 for Bedrock."))
    except ImportError:
        print(dim("  (Install Pillow to see dimensions: pip install Pillow)"))
    except Exception:
        pass

    return image_bytes, media_type


# ─── Model testers ────────────────────────────────────────────────────────────

def test_claude(client, model_id: str, image_bytes: bytes, media_type: str) -> dict:
    """Test Anthropic Claude models using Bedrock Converse API."""

    # Bedrock format: "image/jpeg" → "jpeg"
    fmt = media_type.split("/")[1]
    if fmt == "jpg":
        fmt = "jpeg"

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": fmt,                  # "jpeg" not "image/jpeg"
                            "source": {
                                "bytes": image_bytes        # raw bytes, NOT base64
                            }
                        }
                    },
                    {
                        "text": TEST_PROMPT
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 512,
            "temperature": 0.1,
        }
    )

    text = response["output"]["message"]["content"][0]["text"]
    input_tokens  = response["usage"]["inputTokens"]
    output_tokens = response["usage"]["outputTokens"]

    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def test_nova(client, model_id: str, image_bytes: bytes, media_type: str) -> dict:
    """Test Amazon Nova models using Bedrock Converse API."""

    fmt = media_type.split("/")[1]
    if fmt == "jpg":
        fmt = "jpeg"

    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": fmt,
                            "source": {
                                "bytes": image_bytes
                            }
                        }
                    },
                    {
                        "text": TEST_PROMPT
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 512,
            "temperature": 0.1,
        }
    )

    text = response["output"]["message"]["content"][0]["text"]
    input_tokens  = response["usage"]["inputTokens"]
    output_tokens = response["usage"]["outputTokens"]

    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def test_llama4(client, model_id: str, image_bytes: bytes, media_type: str) -> dict:
    """Test Meta Llama 4 models using Bedrock Converse API."""

    fmt = media_type.split("/")[1]
    if fmt == "jpg":
        fmt = "jpeg"

    # Llama 4 on Bedrock uses the same Converse API format
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": fmt,
                            "source": {
                                "bytes": image_bytes
                            }
                        }
                    },
                    {
                        "text": TEST_PROMPT
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 512,
            "temperature": 0.1,
        }
    )

    text = response["output"]["message"]["content"][0]["text"]
    input_tokens  = response["usage"].get("inputTokens", 0)
    output_tokens = response["usage"].get("outputTokens", 0)

    return {
        "text": text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def test_llama32(client, model_id: str, image_bytes: bytes, media_type: str) -> dict:
    """Test Meta Llama 3.2 vision models using InvokeModel API.
    Llama 3.2 on Bedrock uses InvokeModel with a different payload format.
    """

    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Llama 3.2 vision uses a specific message format
    payload = {
        "prompt": (
            "<|begin_of_text|>"
            "<|start_header_id|>user<|end_header_id|>\n\n"
            f"<|image|>{TEST_PROMPT}"
            "<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n\n"
        ),
        "images": [b64_image],
        "max_gen_len": 512,
        "temperature": 0.1,
    }

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json"
    )

    body = json.loads(response["body"].read())
    text = body.get("generation", "")

    return {
        "text": text,
        "input_tokens": body.get("prompt_token_count", 0),
        "output_tokens": body.get("generation_token_count", 0),
    }


# ─── Router ───────────────────────────────────────────────────────────────────

def get_tester(model_id: str):
    """Return the correct test function for a given model ID."""
    if model_id.startswith("anthropic."):
        return test_claude
    elif "nova" in model_id:
        return test_nova
    elif "llama4" in model_id:
        return test_llama4
    elif "llama3-2" in model_id:
        return test_llama32
    elif model_id.startswith("us.anthropic."):
        return test_claude
    else:
        return None


# ─── Main runner ──────────────────────────────────────────────────────────────

def run_tests(image_path: str, region: str, models_to_test: list = None):
    print(f"\n{'═' * 70}")
    print(bold(cyan("  AgriSabi — Bedrock Vision Model Tester")))
    print(f"{'═' * 70}")
    print(f"  Region:    {region}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'═' * 70}")

    image_bytes, media_type = load_image(image_path)

    # Create Bedrock client
    try:
        client = boto3.client("bedrock-runtime", region_name=region)
        # Quick credential check
        boto3.client("sts").get_caller_identity()
        print(green("\n✓ AWS credentials valid"))
    except Exception as e:
        print(red(f"\n✗ AWS credentials error: {e}"))
        print(yellow("  Run: aws configure"))
        sys.exit(1)

    if models_to_test is None:
        models_to_test = MODELS

    # Results store
    results = []

    print(f"\n{'─' * 70}")
    print(bold("  Running tests — this may take 1–2 minutes..."))
    print(f"{'─' * 70}\n")

    for display_name, model_id, supports_vision, notes in models_to_test:

        # ── SKIP models not on Bedrock ──────────────────────────────────────
        if model_id == "SKIP":
            print(f"{dim('SKIP')}  {display_name}")
            print(f"      {dim(notes)}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "SKIP",
                "reason": notes,
                "response_preview": "",
                "latency": 0,
                "input_tokens": 0,
                "output_tokens": 0,
            })
            continue

        # ── SKIP text-only models ───────────────────────────────────────────
        if not supports_vision:
            print(f"{yellow('SKIP')}  {bold(display_name)}  {dim('(text only — no vision)')}")
            print(f"      {dim(notes)}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "TEXT_ONLY",
                "reason": "No vision capability",
                "response_preview": "",
                "latency": 0,
                "input_tokens": 0,
                "output_tokens": 0,
            })
            continue

        # ── Test the model ──────────────────────────────────────────────────
        print(f"  Testing: {bold(display_name)}")
        print(f"  Model ID: {dim(model_id)}")

        tester = get_tester(model_id)
        if tester is None:
            print(f"  {yellow('SKIP')} — no tester implemented for this model family\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "SKIP",
                "reason": "No tester implemented",
                "response_preview": "",
                "latency": 0,
                "input_tokens": 0,
                "output_tokens": 0,
            })
            continue

        start = time.time()
        try:
            result = tester(client, model_id, image_bytes, media_type)
            latency = time.time() - start

            preview = result["text"][:300].replace("\n", " ")
            if len(result["text"]) > 300:
                preview += "..."

            print(f"  {green('✓ PASS')}  ({latency:.2f}s  |  in:{result['input_tokens']} out:{result['output_tokens']} tokens)")
            print(f"  Response: {dim(preview)}\n")

            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "PASS",
                "reason": "",
                "response_preview": preview,
                "latency": latency,
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
            })

        except client.exceptions.AccessDeniedException:
            latency = time.time() - start
            msg = "Model not enabled — go to AWS Console → Bedrock → Model access → Enable this model"
            print(f"  {red('✗ FAIL')}  AccessDeniedException")
            print(f"  Fix: {yellow(msg)}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "FAIL",
                "reason": "ACCESS DENIED — model not enabled in your account",
                "response_preview": "",
                "latency": latency,
                "input_tokens": 0,
                "output_tokens": 0,
            })

        except client.exceptions.ResourceNotFoundException:
            latency = time.time() - start
            msg = f"Model not available in region {region}. Try us-east-1."
            print(f"  {red('✗ FAIL')}  ResourceNotFoundException")
            print(f"  Fix: {yellow(msg)}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "FAIL",
                "reason": f"NOT IN REGION — not available in {region}",
                "response_preview": "",
                "latency": latency,
                "input_tokens": 0,
                "output_tokens": 0,
            })

        except client.exceptions.ValidationException as e:
            latency = time.time() - start
            err = str(e)
            print(f"  {red('✗ FAIL')}  ValidationException: {err}")

            # Common causes
            if "image" in err.lower():
                hint = "Image format issue — try converting to JPEG first"
            elif "model" in err.lower():
                hint = "Model ID may be wrong — check AWS Bedrock console for exact ID"
            else:
                hint = "Request format issue — check the payload structure"

            print(f"  Hint: {yellow(hint)}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "FAIL",
                "reason": f"VALIDATION ERROR: {err}",
                "response_preview": "",
                "latency": latency,
                "input_tokens": 0,
                "output_tokens": 0,
            })

        except client.exceptions.ThrottlingException:
            latency = time.time() - start
            print(f"  {yellow('THROTTLE')}  Rate limited — wait 30s and retry\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "THROTTLE",
                "reason": "Rate limited — retry after 30 seconds",
                "response_preview": "",
                "latency": latency,
                "input_tokens": 0,
                "output_tokens": 0,
            })
            time.sleep(2)  # brief pause before next model

        except Exception as e:
            latency = time.time() - start
            err_type = type(e).__name__
            err_msg  = str(e)[:150]
            print(f"  {red('✗ FAIL')}  {err_type}: {err_msg}\n")
            results.append({
                "name": display_name,
                "model_id": model_id,
                "status": "FAIL",
                "reason": f"{err_type}: {err_msg}",
                "response_preview": "",
                "latency": latency,
                "input_tokens": 0,
                "output_tokens": 0,
            })

    # ─── Summary table ────────────────────────────────────────────────────────
    print(f"\n{'═' * 70}")
    print(bold(cyan("  RESULTS SUMMARY")))
    print(f"{'═' * 70}")

    pass_count  = sum(1 for r in results if r["status"] == "PASS")
    fail_count  = sum(1 for r in results if r["status"] == "FAIL")
    skip_count  = sum(1 for r in results if r["status"] in ("SKIP", "TEXT_ONLY"))

    print(f"\n  {green(f'✓ PASS: {pass_count}')}   {red(f'✗ FAIL: {fail_count}')}   {dim(f'– SKIP: {skip_count}')}\n")

    col1 = 30
    col2 = 10
    col3 = 10
    col4 = 45

    header = (
        f"  {'Model':<{col1}} {'Status':<{col2}} {'Latency':<{col3}} {'Notes / Error':<{col4}}"
    )
    print(bold(header))
    print(f"  {'─' * (col1 + col2 + col3 + col4 + 6)}")

    for r in results:
        if r["status"] == "PASS":
            status_str = green(f"{'PASS':<{col2}}")
            latency_str = f"{r['latency']:.2f}s"
            notes_str = f"in:{r['input_tokens']} out:{r['output_tokens']} tokens"
        elif r["status"] == "FAIL":
            status_str = red(f"{'FAIL':<{col2}}")
            latency_str = f"{r['latency']:.2f}s" if r["latency"] else "—"
            notes_str = r["reason"][:col4]
        elif r["status"] == "THROTTLE":
            status_str = yellow(f"{'THROTTLE':<{col2}}")
            latency_str = "—"
            notes_str = r["reason"][:col4]
        elif r["status"] == "TEXT_ONLY":
            status_str = yellow(f"{'TEXT ONLY':<{col2}}")
            latency_str = "—"
            notes_str = "No vision capability"
        else:
            status_str = dim(f"{'SKIP':<{col2}}")
            latency_str = "—"
            notes_str = r["reason"][:col4]

        print(f"  {r['name']:<{col1}} {status_str} {latency_str:<{col3}} {dim(notes_str)}")

    # ─── Recommendation ───────────────────────────────────────────────────────
    passing = [r for r in results if r["status"] == "PASS"]

    print(f"\n{'─' * 70}")
    print(bold("  RECOMMENDATION FOR AGRISABI"))
    print(f"{'─' * 70}")

    if not passing:
        print(red("\n  No models passed. Most likely causes:"))
        print(yellow("  1. Model access not enabled — AWS Console → Bedrock → Model access"))
        print(yellow("  2. Wrong region — newer models (Llama 4) are only in us-east-1"))
        print(yellow("  3. Image format issue — try a simple JPEG photo of a plant leaf"))
        print(yellow("  4. AWS credentials expired — run: aws sts get-caller-identity\n"))
    else:
        # Rank passing models by preference for AgriSabi
        priority_order = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "meta.llama4-maverick-17b-instruct-v1:0",
            "amazon.nova-pro-v1:0",
            "meta.llama4-scout-17b-instruct-v1:0",
            "anthropic.claude-3-5-haiku-20241022-v1:0",
            "meta.llama3-2-90b-instruct-v1:0",
            "amazon.nova-lite-v1:0",
            "meta.llama3-2-11b-instruct-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
        ]

        best = None
        for preferred_id in priority_order:
            for r in passing:
                if r["model_id"] == preferred_id:
                    best = r
                    break
            if best:
                break

        if not best:
            best = min(passing, key=lambda r: r["latency"])

        print(f"\n  {green('→')} Best model for AgriSabi: {bold(best['name'])}")
        print(f"     Model ID: {cyan(best['model_id'])}")
        print(f"     Latency:  {best['latency']:.2f}s")
        print()

        # Advice based on what passed
        claude_passed = any("claude-3-5-sonnet" in r["model_id"] for r in passing)
        llama4_passed = any("llama4" in r["model_id"] for r in passing)
        nova_passed   = any("nova-pro" in r["model_id"] for r in passing)

        if claude_passed:
            print("  Claude 3.5 Sonnet passed — this is your primary diagnosis model.")
            print("  If you were getting 'Failed to analyze image visually', the issue")
            print("  is NOT the model. The bug is in how the image bytes are passed.")
            print()
            print("  Most common fix in your diagnosis_agent.py:")
            print(cyan("    image_bytes = await file.read()"))
            print(cyan("    # Pass raw bytes to Bedrock — not base64, not the file object"))
            print(cyan("    'source': {'bytes': image_bytes}"))
            print(cyan("    'format': 'jpeg'  # not 'image/jpeg'"))
            print()

        if llama4_passed and not claude_passed:
            print("  Claude 3.5 Sonnet failed but Llama 4 passed.")
            print("  Check if Claude Sonnet is enabled in your AWS account:")
            print(cyan("  AWS Console → Bedrock → Model access → Anthropic → Claude 3.5 Sonnet"))
            print()

        if nova_passed and not claude_passed and not llama4_passed:
            print("  Only Amazon Nova Pro passed. Fallback option for diagnosis.")
            print("  Note: Nova Pro vision quality for crop disease is less tested than Claude.")
            print()

        # Latency report for passing models
        if len(passing) > 1:
            print(f"  Latency comparison (passing models only):")
            for r in sorted(passing, key=lambda x: x["latency"]):
                bar = "█" * min(int(r["latency"] * 5), 30)
                print(f"    {r['name']:<32} {r['latency']:.2f}s  {cyan(bar)}")

    print(f"\n{'═' * 70}\n")

    # ─── Save results to JSON ─────────────────────────────────────────────────
    output_file = Path("vision_test_results.json")
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "image": image_path,
            "region": region,
            "summary": {
                "pass": pass_count,
                "fail": fail_count,
                "skip": skip_count,
            },
            "results": results
        }, f, indent=2)

    print(f"  Full results saved to: {bold(str(output_file.resolve()))}\n")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test AWS Bedrock vision models for AgriSabi crop diagnosis"
    )
    parser.add_argument(
        "--image",
        type=str,
        default="test_image.jpg",
        help="Path to the test image (default: test_image.jpg)"
    )
    parser.add_argument(
        "--region",
        type=str,
        default=DEFAULT_REGION,
        help=f"AWS region (default: {DEFAULT_REGION}). Use us-east-1 for Llama 4."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Test only a specific model ID (optional)"
    )

    args = parser.parse_args()

    # Filter to a single model if requested
    models_to_test = MODELS
    if args.model:
        models_to_test = [(n, m, v, d) for n, m, v, d in MODELS if m == args.model]
        if not models_to_test:
            print(red(f"\n✗ Model ID not found in list: {args.model}"))
            print(yellow("  Run without --model to see all available models\n"))
            sys.exit(1)

    run_tests(args.image, args.region, models_to_test)