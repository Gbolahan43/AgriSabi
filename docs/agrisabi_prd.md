# AgriSabi — Technical Project Documentation

> **AI-Powered Agricultural Intelligence Platform**
> Built for Nigerian Smallholder Farmers
> Powered by AWS Bedrock · Claude 3.5 Sonnet · Amazon Nova Sonic · Next.js 14 · FastAPI

---

| Status | Version | Last Updated | Audience |
|---|---|---|---|
| In Development | v1.1 MVP | 2026 | Dev Team |

### Changelog from v1.0

| Section | Change |
|---|---|
| Feature 1 (Diagnosis) | Completely revised — two-stage symptom extraction + RAG matching replaces direct LLM diagnosis |
| Feature 2 (Voice) | Revised to three-tier language architecture — Nova Sonic for English/Pidgin, Transcribe pipeline for Hausa/Yoruba/Igbo |
| Feature 6 (NEW) | Amazon Nova Sonic Live Assistant — standalone S2S feature with RAG context injection |
| Section 3 (Stack) | Nova Sonic added; model-per-feature usage table added |
| Section 4 (Architecture) | Orchestration layer added; updated voice flow; updated diagnosis flow; Nova Sonic session flow added |
| Section 5 (Structure) | `orchestration/` layer added; `nova_sonic.py`; `assistant.py` route; `assistant/page.tsx`; `DiagnosisCard.tsx`; `NovaAssistant.tsx` |
| Section 6 (Services) | Diagnosis agent two-stage detail; Nova Sonic service; assistant RAG pre-fetch; diagnosis response schema; Nova Sonic prompt structure |
| Section 7 (Database) | `session_type`, `pipeline`, `nova_sonic_transcript`, `diagnosis_results` fields added to sessions table |
| Section 11 (Env Vars) | Nova Sonic variables; diagnosis threshold; RAG top-k |
| Section 12 (Testing) | Nova Sonic session tests; two-stage diagnosis accuracy tests; false confidence audit added |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Features](#2-features--complete-specification)
3. [Technology Stack](#3-technology-stack)
4. [System Architecture](#4-system-architecture)
5. [Project Structure](#5-project-structure)
6. [Core Services](#6-core-services--implementation-details)
7. [Database Design](#7-database-design)
8. [Agent Persona & System Prompt](#8-agrisabi-agent-persona--system-prompt)
9. [Security & Privacy](#9-security--privacy)
10. [Development Roadmap](#10-development-roadmap)
11. [Environment Variables](#11-environment-variables-reference)
12. [Testing & Evaluation](#12-testing--evaluation-strategy)
13. [Glossary](#13-glossary)

---

## 1. Executive Summary

AgriSabi is a multimodal AI agent built on AWS Bedrock, designed to bring enterprise-grade agricultural intelligence to Nigerian smallholder farmers. It combines two-stage crop disease diagnosis grounded in IITA/NCRI research, voice-first interaction in four local languages, a live speech-to-speech AI assistant powered by Amazon Nova Sonic with RAG context injection, weather-aware farming advice, and live market price intelligence — all accessible via a simple mobile interface with no literacy requirement.

The platform is built as a production-ready, cloud-native system targeting national scale. It operates in low-bandwidth environments, supports non-literate users through voice, delivers sub-3-second response times for all core interactions, and is honest about AI confidence levels rather than presenting uncertain diagnoses as definitive.

### The Core Problem We Solve

> - Nigeria has **15+ million smallholder farmers** who lack access to timely, accurate, localised agricultural guidance.
> - Crop disease misdiagnosis leads to avoidable losses worth **billions of naira annually** — a wrong AI diagnosis is worse than no diagnosis if the farmer acts on it.
> - **General-purpose LLM vision is not reliable for Nigerian crop disease classification.** These models have broad agricultural knowledge but are not fine-tuned on Nigerian crop varieties and growing conditions. Confident misdiagnosis destroys both crops and trust.
> - Extension workers are too few — roughly **1 per 10,000 farmers** — and cannot reach remote communities.
> - Existing solutions are English-only, text-heavy, or too expensive — **excluding the farmers who need help most**.

### 1.1 Mission Statement

To provide every Nigerian farmer — regardless of literacy level, language, or location — with the same quality of agricultural guidance that large commercial farms receive from expert agronomists, while being transparent about AI confidence levels and never replacing human expert judgment for high-stakes crop decisions.

### 1.2 Success Metrics (MVP)

| Metric | Target | How It Is Measured |
|---|---|---|
| Diagnosis — Symptom Extraction Accuracy | > 90% correct symptoms identified | Blind expert review against labeled image set |
| Diagnosis — RAG Disease Match | > 85% correct disease retrieved from KB | PlantVillage + IITA labeled test set |
| Diagnosis — False Confidence Rate | 0% | Manual audit of 20 ambiguous/blurry images — system must never be confidently wrong |
| Response Latency — Text/Voice | < 3 seconds | P95 in AWS CloudWatch |
| Nova Sonic First Response Latency | < 1.5 seconds | P95 WebSocket time-to-first-audio |
| Language Coverage | Hausa, Yoruba, Igbo, Pidgin, English | Transcribe + Polly + Nova Sonic language audit |
| Platform Uptime | 99.9% SLA | AWS Bedrock managed infrastructure |
| Guardrail Rejection Rate | 100% of off-topic queries rejected | Red-team manual audit |

---

## 2. Features — Complete Specification

### 2.1 Core MVP Features

---

#### Feature 1: Two-Stage Crop Disease Diagnosis (Revised)

> **Why this changed:** General-purpose LLM vision (Claude 3.5 Sonnet, Nova Pro) has broad agricultural knowledge but is not fine-tuned for Nigerian crop disease classification. A single LLM asked to both identify a disease from an image and prescribe treatment creates an unacceptable risk of confident misdiagnosis. The revised architecture separates these two responsibilities — visual symptom extraction (what LLM vision does reliably) from disease identification (what a RAG system grounded in IITA/NCRI documents does reliably).

**The Two-Stage Flow:**

```
Stage 1 — Symptom Extraction (LLM Vision)
  Input:  Farmer crop photo
  Task:   Describe ONLY visible symptoms — colour changes,
          spots, lesions, patterns, affected plant parts
  Output: Structured symptom description in plain language
  Rule:   The LLM NEVER names a disease in this stage

Stage 2 — Disease Matching (RAG + LLM Synthesis)
  Input:  Symptom description from Stage 1
  Task:   Query IITA/NCRI Knowledge Base using symptoms
  Output: 1–3 most likely diseases with confidence levels,
          source citations, and treatment options per disease
  Rule:   ALL disease names come from KB documents only
```

| Parameter | Detail |
|---|---|
| **Stage 1 Model** | Claude 3.5 Sonnet via Bedrock Converse API (vision input) |
| **Stage 2 Retrieval** | Bedrock Knowledge Base semantic search on symptom text |
| **Stage 2 Synthesis** | Claude 3.5 Sonnet — synthesises treatment from retrieved IITA/NCRI chunks |
| **Confidence Handling** | Ambiguous symptoms → top 3 differentials, each with likelihood and what photo angle would confirm |
| **Poor Image Quality** | Explicit retake request with specific guidance — never guess from a blurry photo |
| **Transparency Label** | Displayed on every result: *"AI-assisted screening — confirm with your extension worker before treating high-value crops"* |
| **Expert Referral Flag** | `expert_referral_recommended: true` when confidence is LOW or multiple differentials are equally likely |
| **Phase 2 Upgrade** | PlantVillage specialist classifier (SageMaker) slots in before Stage 1 — does not change downstream architecture |

**Why this is safer than direct LLM diagnosis:**
The LLM cannot confidently hallucinate a disease name because it is never asked to name one. Stage 1 only asks "what do you see?" — a reliable task for vision models. Stage 2 grounds every disease name in your verified IITA/NCRI documents. If the KB does not contain the disease, the system says so rather than inventing an answer.

---

#### Feature 2: Voice-First Interaction — Three-Tier Architecture

> **Why this changed:** Amazon Nova Sonic was tested and confirmed to support English only. Nigerian Pidgin is English-based and has been confirmed to work with Nova Sonic. Hausa, Yoruba, and Igbo require the Transcribe → Agent → Polly pipeline. The architecture routes each query to the correct pipeline based on detected language.

**Three Tiers:**

| Tier | Languages | Pipeline | Latency | Notes |
|---|---|---|---|---|
| **Tier 1** | English, Nigerian Pidgin | Nova Sonic (single model) | ~1–1.5s | Natural interruption; no STT/TTS services |
| **Tier 2** | Hausa, Yoruba, Igbo | Transcribe → Bedrock Agent → Polly | ~2.5–3s | Full RAG + Action Group access |
| **Tier 3** | Any | Text fallback prompt | Instant | Triggered when audio confidence < 0.7 |

| Parameter | Detail |
|---|---|
| **Language Detection** | First 2 seconds of audio → Transcribe `IdentifyLanguage` |
| **Routing Threshold** | Language confidence > 0.8 required; below threshold defaults to Tier 2 |
| **Silence Detection** | Client-side VAD — auto-stops after 2 seconds silence |
| **Offline Fallback** | Service Worker cached responses for most common queries |

---

#### Feature 3: Climate-Resilient Nowcasting Advisor

| Parameter | Detail |
|---|---|
| **Trigger** | Location, planting, spraying, harvesting, or watering intent |
| **Data Source** | OpenWeatherMap One Call API 3.0 — current + 5-day forecast |
| **Implementation** | Bedrock Agent Action Group → Lambda |
| **Example Output** | "Do not spray your cocoa trees today — 80% chance of rain by 3pm" |
| **Granularity** | City and LGA level via device GPS |

---

#### Feature 4: Sustainable Farming Advisor

| Parameter | Detail |
|---|---|
| **Knowledge Source** | Organic Farming Guides for Sub-Saharan Africa — Bedrock KB |
| **Query Types** | Fertilizer substitutes, composting, intercropping, organic pest control |
| **RAG Strategy** | Semantic search filtered by crop type and Nigerian region |
| **Output** | Step-by-step preparation instructions, estimated cost per hectare |

---

#### Feature 5: Live Market Price Intelligence

| Parameter | Detail |
|---|---|
| **Data Source** | Lambda refreshing DynamoDB daily from AFEX API or manual source |
| **Markets (MVP)** | Lagos Mile 12, Kano Dawanau, Onitsha, Gboko, Saki |
| **Crops (MVP)** | Maize, cassava, beans, rice, tomatoes, yam, cocoa |
| **Output** | Price table by market, trend indicator, best-market recommendation |
| **Refresh** | Daily 06:00 WAT via EventBridge scheduled Lambda |

---

#### Feature 6: Nova Sonic Live AI Assistant (NEW)

> A standalone, always-available conversational AI assistant for English-speaking farmers and extension workers. Powered by Amazon Nova Sonic for natural, low-latency bidirectional speech. Grounded in IITA/NCRI knowledge via RAG pre-fetch at session start. Accessed via a dedicated button — completely isolated from all other features.

**User Flow:**

```
Home screen → "Chat with AI Assistant Live" button
        |
        v
/assistant page  [clearly labeled: English only]
        |
Backend pre-session: RAG pre-fetch based on user crop profile
Top 10 KB chunks retrieved and formatted as session context
        |
        v
User taps "Start"
WebSocket opens → FastAPI /assistant/stream
Nova Sonic stream opens with enriched system prompt
5-minute countdown timer starts (visible on screen)
        |
        v
[Bidirectional conversation]
User speaks → Nova Sonic processes → Audio response
User can interrupt while Nova Sonic is speaking
        |
        v
Session ends (timer or user taps "End")
Transcript saved to DynamoDB
```

**RAG Context Injection:**

| User Type | Pre-Fetch Query | Chunks Injected |
|---|---|---|
| Registered user | `{primary_crops} + {lga} + {current_month} farming advice` | Top 10 KB chunks |
| Anonymous user | `Nigeria smallholder farming {month} seasonal advice common diseases` | Top 8 KB chunks |
| Token budget | Context capped at 2,000 tokens | Leaves room for conversation |

| Parameter | Detail |
|---|---|
| **Model** | Amazon Nova Sonic via Bedrock bidirectional WebSocket |
| **Language** | English only |
| **Session Timeout** | 5 minutes hard cap — visible countdown on screen |
| **Anonymous Limit** | 2 sessions per day per anonymous user (cost control) |
| **System Prompt** | AgriSabi persona + injected RAG context + Nigerian farming scope + live data redirect instructions |
| **Interruption** | Native Nova Sonic barge-in — user can speak while model is responding |
| **Live Data** | Cannot call Action Groups — weather/prices redirect to main app features |
| **Transcript** | Full session transcript saved to DynamoDB on session end |

**What Nova Sonic knows in a session:**
- General agricultural knowledge from training
- IITA/NCRI content injected at session start
- User's crop profile and region (registered users)
- Current month's Nigerian seasonal farming context

**What Nova Sonic redirects back to the main app:**
- Live weather data → "Use the Weather feature in the main app"
- Live market prices → "Use the Market Prices feature in the main app"

---

### 2.2 Suggested Additional Features (Post-MVP)

| Feature | Description |
|---|---|
| **Specialist Diagnosis Classifier** | PlantVillage fine-tuned model on SageMaker — slots into Stage 1, improves accuracy to 95%+ |
| **IITA Nigerian Dataset** | Partner with IITA to obtain Nigerian-specific crop disease image dataset for fine-tuning |
| **Nova Sonic Language Expansion** | Migrate Hausa/Yoruba/Igbo to Nova Sonic as Amazon expands language support |
| **Soil Health Scanner** | Conversational assessment → AI infers deficiency → recommends organic amendments |
| **Personalised Planting Calendar** | LGA + rainfall + variety → seasonal crop schedule |
| **Farm Diary (Voice Log)** | Farmer narrates daily observations → AI structures into searchable record |
| **Extension Worker Dashboard** | Agronomist portal — review AI diagnoses, override, add local knowledge |
| **SMS/USSD Fallback** | Africa's Talking for feature phone users |
| **WhatsApp Integration** | AgriSabi as WhatsApp Business API chatbot |

---

## 3. Technology Stack

### 3.1 Full Stack

| Layer | Technology | Purpose |
|---|---|---|
| Foundation Model — Primary | Claude 3.5 Sonnet (Bedrock) | Vision symptom extraction, RAG synthesis, complex advisory |
| Foundation Model — Fallback | Amazon Nova Pro (Bedrock) | High-volume text queries, market/weather synthesis |
| Live Voice Assistant | Amazon Nova Sonic (Bedrock) | Bidirectional S2S — English live assistant |
| Inference API | AWS Bedrock Converse API | Unified text + image endpoint |
| RAG Engine | AWS Bedrock Knowledge Bases | Managed retrieval-augmented generation |
| Vector Store | Amazon OpenSearch Serverless | Embedding storage and semantic search |
| Agent Orchestration | AWS Bedrock Agents | Multi-step reasoning, memory, Action Groups |
| Request Router | Custom orchestration layer (FastAPI) | Routes to correct agent/model/pipeline; owns fallback logic |
| Tool Functions | AWS Lambda (Python 3.12) | Weather API, Market Price refresh |
| Speech-to-Text | Amazon Transcribe (real-time) | Streaming STT — Hausa, Yoruba, Igbo |
| Text-to-Speech | Amazon Polly Neural | Voice output for indigenous languages |
| Backend API | FastAPI (Python 3.12) | REST + WebSocket + SSE |
| Frontend | Next.js 14 (TypeScript) | Mobile-first PWA |
| UI Components | Tailwind CSS + shadcn/ui | Component library |
| Database | Amazon DynamoDB | Sessions, history, market prices |
| File Storage | Amazon S3 | Documents, uploads, audio cache |
| CDN | Amazon CloudFront + WAF | Asset delivery + rate limiting |
| Authentication | Amazon Cognito | JWT auth + anonymous identity |
| Infrastructure | AWS CDK (Python) | All cloud resources as code |
| CI/CD | GitHub Actions | Test + deploy pipeline |
| Observability | CloudWatch + X-Ray | Logs, traces, latency alarms |
| Content Safety | AWS Bedrock Guardrails | Topic filtering, PII redaction |

### 3.2 Model Selection by Feature

| Feature | Primary Model | Fallback | Rationale |
|---|---|---|---|
| Diagnosis — Symptom Extraction | Claude 3.5 Sonnet | Return error + retake prompt | Vision quality required — no acceptable model fallback |
| Diagnosis — Treatment Synthesis | Claude 3.5 Sonnet | Nova Pro | Text synthesis — Nova Pro acceptable |
| Voice — English / Pidgin | Nova Sonic | Transcribe pipeline | Single hop preferred; pipeline as safety net |
| Voice — Hausa / Yoruba / Igbo | Transcribe + Sonnet + Polly | Cached common responses | Language support requires full pipeline |
| Live Assistant | Nova Sonic | Graceful session end + message | Standalone feature — no degraded mode |
| Market Intelligence | Nova Pro | Cached DynamoDB read | Price display needs no LLM synthesis |
| Weather Advice | Nova Pro | Template-based formatting | Simple structured data → plain language |
| Sustainable Farming Advisor | Claude 3.5 Sonnet | Nova Pro | Complex RAG synthesis |

---

## 4. System Architecture

### 4.1 Design Principles

- **No AWS SDK calls from the frontend.** All model calls, DynamoDB, and S3 go through FastAPI.
- **Orchestration layer owns all routing.** Routes are thin — they call the orchestrator, which decides which model, which pipeline, and what to do on failure.
- **Two-stage diagnosis — LLM never names a disease.** Stage 1 extracts symptoms only. Stage 2 matches against IITA/NCRI KB. All disease names sourced from verified documents.
- **Nova Sonic is fully isolated.** The live assistant has zero dependency on the Bedrock Agent, Transcribe, Polly, or any other feature's code path. It is additive.
- **RAG pre-fetch, not mid-conversation retrieval.** Nova Sonic sessions receive context at start — no interruption to retrieve documents during conversation.
- **Language-aware voice routing.** Detected from first 2 seconds of audio. English/Pidgin → Nova Sonic. Hausa/Yoruba/Igbo → Transcribe pipeline.

### 4.2 Orchestration Layer

```
API Route receives request
        |
        v
orchestration/router.py
        |
        ├── DIAGNOSIS REQUEST
        │       └── diagnosis_agent.py
        │               ├── Stage 1: vision.py → SYMPTOM_EXTRACTION_PROMPT
        │               └── Stage 2: rag.py symptom_query() → TREATMENT_SYNTHESIS_PROMPT
        │
        ├── VOICE REQUEST
        │       └── voice_agent.py
        │               ├── Language detection (Transcribe IdentifyLanguage, 2s)
        │               ├── English/Pidgin → nova_sonic.py stream_conversation()
        │               └── Hausa/Yoruba/Igbo → transcribe.py + bedrock.py + polly.py
        │
        ├── LIVE ASSISTANT REQUEST
        │       └── assistant_agent.py
        │               ├── Pre-session: rag.py context_prefetch()
        │               └── nova_sonic.py bidirectional_stream()
        │
        ├── ADVISORY REQUEST (chat, weather, market)
        │       └── advisory_agent.py
        │               ├── Primary: Claude 3.5 Sonnet via Bedrock Agent
        │               └── Fallback: Nova Pro (if Sonnet throttled or > 2s)
        │
        └── fallback.py — all retry and degradation logic lives here
```

### 4.3 Voice Flow — Language Routing

```
Farmer speaks
      |
      v
Client streams PCM audio → FastAPI /voice
      |
      v
First 2 seconds → Transcribe IdentifyLanguage
      |
      ├── English / Pidgin (confidence > 0.8)
      │         |
      │         v
      │   nova_sonic.py — single bidirectional stream
      │   Latency: ~1–1.5 seconds
      │         |
      │         v
      │   Audio response → client playback
      │
      └── Hausa / Yoruba / Igbo (or confidence < 0.8)
                |
                v
          transcribe.py (full STT, ha-SA / yo-NG / ig)
                |
                v
          advisory_agent.py → Bedrock Agent
          (full RAG + Action Group access)
                |
                v
          polly.py — Neural voice in detected language
                |
                v
          MP3 → client playback
```

### 4.4 Diagnosis Flow — Two-Stage

```
Farmer uploads crop photo
        |
        v
vision.py: resize to 1024×1024, strip EXIF, base64 encode
        |
        v
STAGE 1 — Symptom Extraction
Claude 3.5 Sonnet (Converse API, vision input)
SYMPTOM_EXTRACTION_PROMPT:
"Describe ONLY visible symptoms. Do not name a disease."
Output: { symptoms[], affected_parts[], severity, image_quality }
        |
        ├── image_quality == "poor" → return retake guidance, stop
        |
        v
STAGE 2 — Disease Matching
symptom text → rag.py symptom_query()
Top 5 IITA/NCRI chunks retrieved
        |
        v
TREATMENT_SYNTHESIS_PROMPT:
"Name diseases ONLY from retrieved documents. Cite source."
        |
        v
Structured response:
  symptoms_observed
  possible_diseases[] (name, likelihood, source, treatment, dosage, precautions)
  confidence_level
  expert_referral_recommended
  transparency_label (always shown)
        |
        v
Saved to DynamoDB session.diagnosis_results[]
```

### 4.5 Nova Sonic Live Assistant Flow

```
User taps "Chat with AI Assistant Live"
        |
        v
/assistant page loads
Backend: rag.py context_prefetch(user_profile)
  → top 10 KB chunks retrieved
  → enriched system prompt built
        |
        v
User taps "Start"
WebSocket: client → FastAPI /assistant/stream
nova_sonic.py opens Bedrock bidirectional stream
System prompt (persona + RAG context) injected
5-minute timer starts (visible on screen)
        |
        v
[Bidirectional conversation]
User speaks → PCM chunks → Nova Sonic
Nova Sonic → PCM chunks → client playback
Native barge-in: user can interrupt at any time
        |
        v
Session ends (5 min timer OR user taps "End")
WebSocket closes gracefully
Full transcript saved to DynamoDB
```

### 4.6 System Diagram

```
  [ Mobile PWA — Next.js ]
         |
    HTTPS + SSE + WebSocket
         v
  [ FastAPI — ECS Fargate ]  ←── Cognito JWT
         |
         v
  [ orchestration/router.py ]
    |        |         |         |
    v        v         v         v
diagnosis  voice    advisory  assistant
_agent    _agent    _agent    _agent
    |       |  |       |         |
    |   Nova  Trans  Bedrock   Nova
    |   Sonic ─cribe  Agent    Sonic
    |    (en)  (ha/   (RAG +   (S2S +
    v          yo/ig) Actions)  RAG ctx)
Claude 3.5
Sonnet
(Vision+RAG)
         |
    ┌────┴──────────────────┐
    v                       v
 KB RAG                Action Groups
(OpenSearch)             (Lambda)
                      Weather | Market

[ DynamoDB: sessions, market prices, users ]
[ S3: documents, uploads, audio cache ]
```

---

## 5. Project Structure

```
agrisabi/
├── .github/
│   └── workflows/
│       ├── deploy.yml
│       └── test.yml
│
├── infra/
│   ├── stacks/
│   │   ├── bedrock_stack.py         # Agent, KB, Guardrails
│   │   ├── lambda_stack.py          # Weather + Market Action Groups
│   │   ├── storage_stack.py         # S3 buckets, OpenSearch Serverless
│   │   ├── database_stack.py        # DynamoDB — dev_ and prod tables
│   │   ├── auth_stack.py            # Cognito User Pool + Identity Pool
│   │   └── monitoring_stack.py      # CloudWatch dashboards + alarms
│   ├── app.py
│   └── cdk.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py                # Pydantic BaseSettings — all env vars
│   │   │
│   │   ├── api/
│   │   │   ├── deps.py              # boto3 client injection
│   │   │   └── routes/
│   │   │       ├── chat.py          # POST /chat — SSE streaming
│   │   │       ├── voice.py         # POST /voice — language-routed pipeline
│   │   │       ├── diagnose.py      # POST /diagnose — two-stage diagnosis
│   │   │       ├── weather.py       # GET /weather
│   │   │       ├── market.py        # GET /market
│   │   │       ├── history.py       # GET /history/{session_id}
│   │   │       └── assistant.py     # NEW WebSocket /assistant/stream
│   │   │
│   │   ├── orchestration/           # NEW routing + fallback layer
│   │   │   ├── router.py            # Entry — routes to correct agent
│   │   │   ├── fallback.py          # Retry chains, degradation logic
│   │   │   └── agents/
│   │   │       ├── diagnosis_agent.py    # Two-stage symptom + RAG
│   │   │       ├── voice_agent.py        # Language routing
│   │   │       ├── advisory_agent.py     # Chat/weather/market (Sonnet → Nova Pro)
│   │   │       └── assistant_agent.py    # Nova Sonic pre-fetch + session
│   │   │
│   │   ├── services/                # Pure AWS service wrappers
│   │   │   ├── bedrock.py           # Low-level invoke_agent(), converse()
│   │   │   ├── nova_sonic.py        # NEW bidirectional Nova Sonic WebSocket
│   │   │   ├── rag.py               # retrieve_and_generate(), symptom_query(),
│   │   │   │                        # context_prefetch()
│   │   │   ├── transcribe.py        # Real-time STT streaming
│   │   │   ├── polly.py             # Neural TTS
│   │   │   ├── vision.py            # Resize, EXIF strip, base64 encode
│   │   │   └── dynamo.py            # All DynamoDB operations
│   │   │
│   │   ├── models/
│   │   │   ├── schemas.py           # DiagnosisResponse, AssistantSession,
│   │   │   │                        # VoiceResponse, MarketResponse
│   │   │   └── enums.py             # Language, CropType, Pipeline, SessionType
│   │   │
│   │   └── core/
│   │       ├── prompts.py           # SYMPTOM_EXTRACTION_PROMPT
│   │       │                        # TREATMENT_SYNTHESIS_PROMPT
│   │       │                        # NOVA_SONIC_SYSTEM_PROMPT (template)
│   │       │                        # ADVISORY_PROMPT
│   │       └── guardrails.py        # Topic deny-list, PII config
│   │
│   ├── tests/
│   │   ├── test_diagnosis.py        # Two-stage accuracy + false confidence audit
│   │   ├── test_voice.py            # Language routing + pipeline roundtrip
│   │   ├── test_assistant.py        # NEW Nova Sonic session + RAG injection
│   │   └── test_rag.py              # KB retrieval accuracy
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx             # Landing — language selector, feature CTAs
│   │   │   ├── chat/page.tsx
│   │   │   ├── voice/page.tsx
│   │   │   ├── diagnose/page.tsx
│   │   │   ├── market/page.tsx
│   │   │   ├── assistant/page.tsx   # NEW Live AI Assistant page
│   │   │   └── layout.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── VoiceRecorder.tsx
│   │   │   ├── ImageCapture.tsx
│   │   │   ├── LanguageSwitcher.tsx
│   │   │   ├── WeatherAlert.tsx
│   │   │   ├── MarketCard.tsx
│   │   │   ├── DiagnosisCard.tsx    # NEW two-stage result: symptoms + diseases + confidence
│   │   │   └── NovaAssistant.tsx    # NEW Start/End, waveform, 5-min countdown
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── i18n.ts
│   │   │   └── audio.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   ├── useVoice.ts
│   │   │   ├── useLocation.ts
│   │   │   └── useAssistant.ts      # NEW WebSocket + audio for Nova Sonic
│   │   │
│   │   └── locales/
│   │       ├── ha.json
│   │       ├── yo.json
│   │       ├── ig.json
│   │       └── pcm.json
│   │
│   ├── public/
│   ├── next.config.ts
│   └── tailwind.config.ts
│
├── lambdas/
│   ├── weather_action/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── market_action/
│   │   ├── handler.py
│   │   └── requirements.txt
│   └── shared/
│       └── utils.py
│
├── knowledge-base/
│   ├── documents/
│   │   ├── iita/
│   │   ├── ncri/
│   │   ├── organic-farming/
│   │   └── plant-disease/
│   ├── scripts/
│   │   ├── ingest.py
│   │   └── validate.py
│   └── chunking_config.json
│
├── agents/
│   └── agrisabi_agent/
│       ├── system_prompt.md          # Bedrock Agent persona (chat/voice advisory)
│       ├── nova_sonic_prompt.md      # NEW Nova Sonic session prompt template
│       └── action_groups.json
│
├── scripts/
│   ├── setup_aws.sh
│   ├── seed_market_prices.py
│   └── eval.py
│
├── docker-compose.yml
├── Makefile
├── .env.example
├── agrisabi_prd.md                  # This document
├── agrisabi_build_plan.md
└── README.md
```

---

## 6. Core Services — Implementation Details

### 6.1 Orchestration Router (`orchestration/router.py`)

| Parameter | Detail |
|---|---|
| **Role** | First call from every API route — owns all model selection decisions |
| **Input** | Request type, detected language, user profile, request payload |
| **Routing table** | Diagnosis → `diagnosis_agent` · Voice en/pcm → `voice_agent` Tier 1 · Voice ha/yo/ig → `voice_agent` Tier 2 · Live assistant → `assistant_agent` · Advisory → `advisory_agent` |
| **Fallback ownership** | `fallback.py` defines retry counts, timeout thresholds, and degradation behaviour per feature |
| **MVP scope** | One agent per request type — parallel multi-agent calls are Phase 2 |

### 6.2 Diagnosis Agent — Two-Stage (`orchestration/agents/diagnosis_agent.py`)

| Stage | Detail |
|---|---|
| **Stage 1 prompt** | `SYMPTOM_EXTRACTION_PROMPT` — instructs model to describe visible symptoms only, never name a disease, output structured JSON, rate image quality |
| **Stage 1 output schema** | `{ symptoms: [], affected_parts: [], severity: "mild/moderate/severe", image_quality: "good/acceptable/poor" }` |
| **Stage 1 failure** | `image_quality == "poor"` → return retake guidance immediately, skip Stage 2 |
| **Stage 2 input** | Symptom description formatted as natural language query |
| **Stage 2 retrieval** | `rag.py symptom_query()` — filtered by `document_source: [iita, ncri, plant-disease]` — top 5 chunks |
| **Stage 2 prompt** | `TREATMENT_SYNTHESIS_PROMPT` — names diseases only from retrieved documents, cites source for every claim |
| **Confidence rules** | HIGH: clear symptoms + strong KB match. MEDIUM: partial match. LOW: weak match or multiple equal differentials → always sets `expert_referral_recommended: true` |
| **Phase 2 hook** | Stub `specialist_classifier()` in `diagnosis_agent.py` — when SageMaker model is deployed it runs before Stage 1, its classification signal appended to Stage 1 context |

### 6.3 Voice Agent — Language Routing (`orchestration/agents/voice_agent.py`)

| Parameter | Detail |
|---|---|
| **Detection** | First 2 seconds → `transcribe.py identify_language()` |
| **Routing threshold** | Confidence > 0.8 required; below threshold → Tier 2 (conservative default) |
| **Tier 1** | `nova_sonic.py stream_conversation()` — English/Pidgin |
| **Tier 2** | `transcribe.py full_transcription()` → `bedrock.py invoke_agent()` → `polly.py synthesise()` |
| **Session logging** | Both tiers save to DynamoDB with `pipeline: "nova_sonic"` or `pipeline: "transcribe"` |

### 6.4 Nova Sonic Service (`services/nova_sonic.py`)

| Parameter | Detail |
|---|---|
| **Protocol** | Bedrock bidirectional WebSocket — `bedrock-runtime` `invoke_model_with_bidirectional_stream` |
| **Audio in** | PCM 16-bit 16 kHz mono — streamed in chunks from client WebSocket |
| **Audio out** | PCM 24 kHz — streamed back to client, browser plays via Web Audio API |
| **System prompt** | Injected as first message before any user audio — persona + RAG context |
| **Interruption** | Native barge-in — Nova Sonic handles at model level automatically |
| **Session cap** | 5-minute hard timeout in `assistant_agent.py` — sends end signal, closes cleanly |
| **Error handling** | WebSocket disconnect → completed turns saved, incomplete turn discarded gracefully |

### 6.5 Assistant Agent — RAG Pre-Fetch (`orchestration/agents/assistant_agent.py`)

| Parameter | Detail |
|---|---|
| **Pre-fetch timing** | Runs on WebSocket connect — before user taps Start |
| **Registered user query** | `{primary_crops} + {lga} + {current_month} farming advice Nigeria` → top 10 chunks |
| **Anonymous user query** | `Nigeria smallholder farming {month} seasonal advice common crop diseases` → top 8 chunks |
| **Context format** | `"Relevant agricultural knowledge for this session:\n\n{chunk_1}\n\n{chunk_2}..."` |
| **Token cap** | 2,000 tokens max for injected context |
| **Injection point** | Appended to Nova Sonic system prompt after AgriSabi persona block |
| **Live data redirect** | System prompt instructs Nova Sonic to redirect weather and price queries to main app |

### 6.6 Diagnosis Response Schema

```json
{
  "symptoms_observed": [
    "yellowing between leaf veins with green islands remaining",
    "small raised brown lesions on stem"
  ],
  "image_quality": "good",
  "possible_diseases": [
    {
      "name": "Cassava Mosaic Disease",
      "likelihood": "high",
      "source": "IITA Cassava Disease Management Manual, p.14",
      "treatment_organic": [
        "Remove and destroy all infected plant material",
        "Source disease-free cuttings for replanting"
      ],
      "treatment_chemical": [
        "Apply Imidacloprid 200SL to control whitefly vector"
      ],
      "dosage": "2ml per litre of water, spray every 14 days",
      "precautions": [
        "Wear gloves and face mask during application",
        "Do not spray within 7 days of harvest",
        "Keep children away from treated area for 48 hours"
      ]
    }
  ],
  "confidence_level": "high",
  "expert_referral_recommended": false,
  "transparency_label": "AI-assisted screening. Confirm with your extension worker before treating high-value crops.",
  "retake_guidance": null
}
```

### 6.7 Nova Sonic System Prompt Template (`agents/agrisabi_agent/nova_sonic_prompt.md`)

```
BLOCK 1 — Identity
You are AgriSabi, a knowledgeable and warm AI assistant for
Nigerian farmers. You speak conversational English. This is a
live voice conversation — keep every response under 30 seconds
when spoken aloud. Be direct and friendly.

BLOCK 2 — Scope
You specialise in crop diseases, organic farming, soil health,
pest management, and agricultural best practices for West Africa
and Nigeria. Only discuss agriculture. Politely redirect
anything else back to how you can help with their crops.

BLOCK 3 — Injected Knowledge (populated at session start)
Relevant agricultural knowledge for this session:
{pre_fetched_chunks}

BLOCK 4 — Live Data Redirect
If asked about today's weather or forecast:
"I don't have live weather in this assistant — tap the
Weather feature in the main AgriSabi app for real-time
farming advice based on your location."

If asked about market prices:
"For today's prices, use the Market Prices feature in the
main app — it shows prices across Lagos, Kano, Onitsha,
and other major markets."

BLOCK 5 — Conversation Style
Acknowledge what the farmer says before responding.
Express uncertainty clearly — never invent a disease name
or treatment not in your knowledge. If you are unsure,
say so and suggest they use the Diagnose feature with a photo.
```

---

## 7. Database Design

### 7.1 Table: `agrisabi_sessions` / `dev_agrisabi_sessions`

| Attribute | Type | Description |
|---|---|---|
| `session_id` (PK) | String | UUID — shared across all session types |
| `user_id` (GSI) | String | Cognito sub or `anonymous:{fingerprint}` |
| `session_type` | String | `chat`, `voice`, `diagnosis`, `assistant` |
| `pipeline` | String | `nova_sonic`, `transcribe`, `text`, `two_stage_diagnosis` |
| `language` | String | Detected or selected language code |
| `messages` | List | `{role, content, timestamp, modality, pipeline, image_s3_key?}` |
| `location` | Map | `{lat, lng, lga, state}` |
| `nova_sonic_transcript` | String | Full transcript saved on Nova Sonic session end |
| `diagnosis_results` | List | Structured `DiagnosisResponse` objects for the session |
| `ttl` | Number | Unix epoch — auto-delete after 90 days |

- **PK:** `session_id`
- **GSI:** `user_id-index`
- **TTL:** `ttl` attribute
- **Capacity:** On-demand

### 7.2 Table: `agrisabi_market_prices` / `dev_agrisabi_market_prices`

| Attribute | Type | Description |
|---|---|---|
| `crop#market` (PK) | String | e.g. `maize#kano_dawanau` |
| `price_per_kg` | Number | Naira per kilogram |
| `price_per_bag` | Number | Naira per 50 kg bag |
| `trend` | String | `up`, `down`, or `stable` |
| `market_name` | String | Human-readable market name |
| `state` | String | Nigerian state |
| `last_updated` | String (ISO) | Timestamp of last refresh |
| `source` | String | `afex`, `manual`, or `scraped` |

### 7.3 Table: `agrisabi_users` / `dev_agrisabi_users` *(Phase 2)*

| Attribute | Type | Description |
|---|---|---|
| `user_id` (PK) | String | Cognito sub |
| `preferred_language` | String | `ha`, `yo`, `ig`, `pcm`, `en` |
| `primary_crops` | List | Used for Nova Sonic RAG pre-fetch |
| `lga` | String | Used for Nova Sonic context + weather queries |
| `state` | String | Nigerian state |
| `nova_sonic_sessions_today` | Number | Daily rate limit counter |
| `farm_size_ha` | Number | Farm size in hectares |
| `created_at` | String (ISO) | Registration timestamp |

### 7.4 S3 Bucket Structure

```
agrisabi-{env}-documents/   # RAG corpus — synced to Bedrock KB
agrisabi-{env}-uploads/     # Crop images — EXIF stripped, 30-day lifecycle
agrisabi-{env}-audio/       # Polly TTS cache — 24-hour lifecycle
agrisabi-{env}-static/      # PWA assets
```

---

## 8. AgriSabi Agent Persona & System Prompt

### 8.1 Bedrock Agent Prompt (Chat / Voice Advisory)

All 8 blocks from v1.0 apply with one addition:

**Block 9 — Diagnosis Scope (NEW)**
When a farmer describes crop symptoms in text or voice, do not attempt to diagnose from the description alone. Instruct them to use the Diagnose feature with a photo for accurate two-stage analysis. You may describe what the symptoms could suggest in general terms, but always direct to the photo diagnosis feature for actionable treatment recommendations.

### 8.2 Nova Sonic Prompt

Stored in `agents/agrisabi_agent/nova_sonic_prompt.md`. See Section 6.7 for full template. Key differences from the main agent prompt:
- Conversational length limits (under 30 seconds spoken aloud)
- No tool use — cannot call Action Groups
- Live data redirect instructions for weather and prices
- RAG context injected dynamically at session start (not hardcoded)

### 8.3 Diagnosis Prompts (`core/prompts.py`)

**`SYMPTOM_EXTRACTION_PROMPT`** — Stage 1. Instructs the model to describe visible symptoms only, never name a disease, rate image quality, and output structured JSON. The phrase "do not name a disease" appears twice to reinforce the constraint.

**`TREATMENT_SYNTHESIS_PROMPT`** — Stage 2. Instructs the model to name diseases only from the retrieved document chunks provided, cite source document and page for every claim, present multiple possibilities with likelihood, include full treatment details and precautions, and always append the transparency label.

---

## 9. Security & Privacy

| Risk | Mitigation |
|---|---|
| AWS credentials in frontend | No SDK calls from browser — all via FastAPI backend |
| Prompt injection | Bedrock Guardrails on all inputs; max length enforced in FastAPI |
| Nova Sonic session abuse | 5-min hard cap; 2 sessions/day for anonymous users; Cognito rate limiting |
| LLM disease hallucination | Two-stage — LLM never names diseases; all names sourced from KB documents |
| EXIF GPS in uploaded images | `vision.py` strips all EXIF before any storage or model processing |
| PII in conversation history | Guardrails PII redaction; DynamoDB TTL 90 days |
| Nova Sonic transcript storage | Encrypted at rest in DynamoDB; same 90-day TTL policy |
| API abuse / DDoS | CloudFront WAF; 100 req/min per Cognito identity |
| Unauthorised KB access | IAM restricts KB reads to ECS task role only |
| Data residency | Primary region: `af-south-1` Cape Town |

---

## 10. Development Roadmap

### 10.1 7-Day MVP Sprint

| Day | Focus | Key Deliverables |
|---|---|---|
| Day 1–2 | Infrastructure + Data | CDK stacks deployed; S3 documents uploaded; KB synced and verified; DynamoDB tables seeded |
| Day 3 | Agent + Orchestration | Bedrock Agent live; orchestration layer scaffolded; all prompts written; Guardrails configured |
| Day 4 | Diagnosis + RAG | Two-stage endpoint tested; symptom extraction validated; RAG retrieval accuracy checked against IITA/NCRI |
| Day 5 | Voice + Nova Sonic | Voice language routing built; Nova Sonic WebSocket service built; RAG pre-fetch for assistant working |
| Day 6 | Frontend + Integration | All pages built including assistant page; full end-to-end test on real Android device |
| Day 7 | Testing + Demo | Eval harness run; guardrail red-team; voice test all 4 languages; demo recorded; staging live |

### 10.2 Phase 2 — 30 Days Post-MVP

- PlantVillage specialist classifier on SageMaker — slots into diagnosis Stage 1
- IITA partnership for Nigerian crop disease dataset
- Nova Sonic language expansion as Amazon adds support
- Extension Worker Dashboard with AI diagnosis review and override
- SMS/USSD fallback via Africa's Talking

### 10.3 Phase 3 — 90 Days Post-MVP

- Fine-tuned Nigerian crop disease model (trained on IITA dataset)
- WhatsApp Business API chatbot integration
- Offline mode — Service Worker caches common diagnoses
- Cooperative Marketplace
- Yield Prediction Model

---

## 11. Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `AWS_REGION` | Yes | `af-south-1` |
| `AWS_ACCOUNT_ID` | Yes | 12-digit account ID |
| `AWS_TABLE_PREFIX` | Yes | `dev_`, `staging_`, or `` (empty = prod) |
| `AWS_BUCKET_PREFIX` | Yes | `agrisabi-dev-`, `agrisabi-staging-`, `agrisabi-` |
| `BEDROCK_AGENT_ID` | Yes | Bedrock Agent resource ID |
| `BEDROCK_AGENT_ALIAS_ID` | Yes | Per-environment alias ID |
| `BEDROCK_KB_ID` | Yes | Knowledge Base ID |
| `BEDROCK_GUARDRAIL_ID` | Yes | Guardrails configuration ID |
| `NOVA_SONIC_MODEL_ID` | Yes | `amazon.nova-sonic-v1:0` |
| `NOVA_SONIC_SESSION_TIMEOUT_SECONDS` | No | Default `300` (5 minutes) |
| `NOVA_SONIC_ANON_DAILY_LIMIT` | No | Default `2` sessions per anonymous user per day |
| `COGNITO_USER_POOL_ID` | Yes | JWT verification |
| `COGNITO_IDENTITY_POOL_ID` | Yes | Anonymous identity tokens |
| `DYNAMODB_SESSIONS_TABLE` | Yes | `{prefix}agrisabi_sessions` |
| `DYNAMODB_MARKET_TABLE` | Yes | `{prefix}agrisabi_market_prices` |
| `DYNAMODB_USERS_TABLE` | Yes | `{prefix}agrisabi_users` |
| `S3_DOCUMENTS_BUCKET` | Yes | `{bucket_prefix}documents` |
| `S3_UPLOADS_BUCKET` | Yes | `{bucket_prefix}uploads` |
| `OPENWEATHERMAP_API_KEY` | Yes | Stored in AWS Secrets Manager |
| `DIAGNOSIS_CONFIDENCE_THRESHOLD` | No | Default `0.75` — below triggers expert referral |
| `RAG_TOP_K_DIAGNOSIS` | No | Default `5` chunks for diagnosis Stage 2 |
| `RAG_TOP_K_ASSISTANT` | No | Default `10` chunks for Nova Sonic pre-fetch |
| `CORS_ALLOWED_ORIGINS` | Yes | Comma-separated allowed frontend origins |
| `LOG_LEVEL` | No | `INFO` (default) |

---

## 12. Testing & Evaluation Strategy

| Test | Tool | What Is Tested | Pass Criteria |
|---|---|---|---|
| Diagnosis Stage 1 — Symptom Accuracy | pytest + image fixtures | Key symptoms extracted vs expert-labeled ground truth | > 90% key symptoms identified |
| Diagnosis Stage 2 — Disease Match | pytest + KB queries | Correct disease retrieved from KB for given symptoms | > 85% correct match |
| Diagnosis — False Confidence | Manual audit (20 images) | Ambiguous/blurry images — must express uncertainty | 0% confident wrong answers |
| Diagnosis — No Hallucination | Manual audit | Disease names must exist in retrieved KB chunks | 100% — zero invented disease names |
| Voice Routing — Language Detection | pytest + audio fixtures | Correct pipeline selected per language | 100% routing accuracy |
| Voice — Indigenous Roundtrip | pytest + audio fixtures | Hausa/Yoruba/Igbo WAV → MP3 out | WER < 15% |
| Nova Sonic — First Response Latency | Manual timing | Time from Start tap to first audio | P95 < 1.5 seconds |
| Nova Sonic — RAG Injection | pytest | Pre-fetched KB context referenced in first response | Context present in session |
| Nova Sonic — Session Timeout | pytest | Session closes gracefully at 5 minutes | Clean close, transcript saved to DynamoDB |
| Nova Sonic — Scope Enforcement | Manual red-team | Non-agricultural and live-data queries | 100% redirect rate |
| Guardrails — Off-Topic Rejection | Manual red-team (10 queries) | Political, medical, non-agricultural prompts | 100% rejection |
| RAG Retrieval Quality | `scripts/eval.py` | 30 symptom queries vs IITA/NCRI reference answers | > 85% relevant chunk |
| Load Test | Locust | 100 concurrent sessions (all feature types mixed) | P95 < 3s, zero 5xx errors |
| Accessibility | axe-core | Mobile PWA audit | Zero critical violations |

---

## 13. Glossary

| Term | Definition |
|---|---|
| **Two-Stage Diagnosis** | AgriSabi's disease identification approach: Stage 1 — LLM vision extracts symptoms only; Stage 2 — RAG matches symptoms against IITA/NCRI KB to produce grounded disease identification and treatment |
| **Nova Sonic** | Amazon's native speech-to-speech model — single model handles STT, reasoning, and TTS in one pass; English only at MVP |
| **RAG Pre-fetch** | KB context retrieved before a Nova Sonic session opens — injected as system prompt so conversation stays fast and uninterrupted |
| **Orchestration Layer** | `backend/app/orchestration/` — routing and fallback logic between API routes and AWS services; owns all model selection decisions |
| **Voice Tier 1** | Nova Sonic path — English and Pidgin; single model, ~1–1.5s latency |
| **Voice Tier 2** | Transcribe pipeline — Hausa, Yoruba, Igbo; three-service chain, ~2.5–3s |
| **Symptom Extraction Prompt** | Stage 1 prompt — restricts LLM to describing visible symptoms only; disease naming is forbidden |
| **Treatment Synthesis Prompt** | Stage 2 prompt — restricts disease naming to retrieved KB documents only; all claims require source citation |
| **Specialist Classifier** | Phase 2 addition — PlantVillage fine-tuned model on SageMaker; runs before Stage 1 to provide classification signal |
| **Barge-in / Interruption** | Native Nova Sonic capability — user can speak while the model is responding; conversation feels natural |
| **Session Transcript** | Full text record of a Nova Sonic conversation — saved to DynamoDB on session end |
| **RAG** | Retrieval-Augmented Generation — model fetches verified document chunks before generating a response |
| **Action Group** | Bedrock function call interface — used for Weather and Market Price Lambda invocations |
| **STT** | Speech-to-Text — Amazon Transcribe |
| **TTS** | Text-to-Speech — Amazon Polly Neural |
| **SSE** | Server-Sent Events — HTTP streaming for real-time chat token delivery |
| **VAD** | Voice Activity Detection — silence detection on client to auto-stop recording |
| **LGA** | Local Government Area — Nigeria's lowest administrative division |
| **IITA** | International Institute of Tropical Agriculture — primary RAG corpus source |
| **NCRI** | National Cereals Research Institute — RAG corpus source for rice and cereals |
| **WER** | Word Error Rate — speech recognition accuracy metric |
| **CDK** | AWS Cloud Development Kit — infrastructure as Python code |
| **ECS Fargate** | AWS serverless container hosting — runs FastAPI without server management |

---

*AgriSabi v1.1 · Technical Project Documentation · Confidential — AgriSabi Dev Team*