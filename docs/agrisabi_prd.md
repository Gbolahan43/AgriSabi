# AgriSabi — Technical Project Documentation

> **AI-Powered Agricultural Intelligence Platform**
> Built for Nigerian Smallholder Farmers
> Powered by AWS Bedrock · Claude 3.5 Sonnet · Next.js 14 · FastAPI

---

| Status | Version | Sprint | Audience |
|---|---|---|---|
| In Development | v1.0 MVP | 7 Days | Dev Team |

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

AgriSabi is a multimodal AI agent built on AWS Bedrock, designed to bring enterprise-grade agricultural intelligence to Nigerian smallholder farmers. It combines real-time visual crop disease diagnosis, voice-first interaction in local languages, weather-aware farming advice, and verified scientific knowledge — all accessible via a simple mobile interface, with no literacy requirement.

The platform is built as a production-ready, cloud-native system targeting national scale. It is designed to work in low-bandwidth environments, support non-literate users through voice, and deliver sub-3-second response times for all core interactions.

### The Core Problem We Solve

> - Nigeria has **15+ million smallholder farmers** who lack access to timely, accurate, localised agricultural guidance.
> - Crop disease misdiagnosis leads to avoidable losses worth **billions of naira annually**.
> - Extension workers are too few — roughly **1 per 10,000 farmers** — and cannot reach remote communities.
> - Existing solutions are English-only, text-heavy, or too expensive — **excluding the farmers who need help most**.

### 1.1 Mission Statement

To provide every Nigerian farmer — regardless of literacy level, language, or location — with the same quality of agricultural guidance that large commercial farms receive from expert agronomists.

### 1.2 Success Metrics (MVP)

| Metric | Target | How It Is Measured |
|---|---|---|
| Disease Diagnosis Accuracy | > 90% on top 5 Nigerian crop diseases | PlantVillage dataset + human expert review |
| Response Latency | < 3 seconds for all voice and text queries | P95 latency in AWS CloudWatch |
| Language Coverage | 4 major languages plus English | Transcribe + Polly language audit |
| Platform Uptime | 99.9% SLA | AWS Bedrock managed infrastructure |
| Hallucination Rate | < 2% on agricultural queries | Guardrails eval + red-team testing |

---

## 2. Features — Complete Specification

### 2.1 Core MVP Features

---

#### Feature 1: Multimodal Crop Disease Diagnosis

A farmer photographs an affected plant with their mobile phone. The vision model analyses visible symptoms and queries the Bedrock Knowledge Base — loaded with IITA and NCRI research manuals — to return a specific treatment protocol recommended for Nigerian growing conditions.

| Parameter | Detail |
|---|---|
| **Input** | Photo (JPG/PNG) of leaf, stem, or fruit captured via mobile camera or gallery upload |
| **Model** | AWS Bedrock Claude 3.5 Sonnet via Converse API (multimodal) |
| **RAG Source** | IITA and NCRI disease manuals stored in Bedrock Knowledge Base |
| **Output** | Disease name, confidence score, organic treatment, chemical treatment, dosage, precautions |
| **Languages** | Response localised to selected language: Hausa, Yoruba, Igbo, Pidgin, or English |
| **Latency Target** | Under 4 seconds end-to-end including image upload, inference, and RAG retrieval |
| **Error Handling** | Low-confidence diagnosis prompts farmer to retake photo with better lighting |

---

#### Feature 2: Voice-First Interaction (Speech-to-Speech)

Non-literate farmers press a microphone button, speak their question in their native language, and receive a spoken response. Pipeline: device microphone → Amazon Transcribe (STT) → Bedrock Agent (reasoning) → Amazon Polly (TTS) → audio playback.

| Parameter | Detail |
|---|---|
| **Languages Supported** | Hausa, Yoruba, Igbo, Nigerian Pidgin, English |
| **STT Engine** | Amazon Transcribe real-time streaming |
| **Reasoning Engine** | AWS Bedrock Agent (Claude 3.5 Sonnet) |
| **TTS Engine** | Amazon Polly Neural voices |
| **Silence Detection** | Client-side Voice Activity Detection (VAD) — auto-stops after 2 seconds of silence |
| **Audio Format** | PCM 16-bit 16 kHz input; MP3 output from Polly for browser playback |
| **Offline Fallback** | Cached common responses served from Service Worker when network is unavailable |

---

#### Feature 3: Climate-Resilient Nowcasting Advisor

When a farmer's query contains location or farming activity intent, the Bedrock Agent automatically calls the Weather Action Group Lambda, fetches the forecast, and translates raw data into plain-language farming instructions.

| Parameter | Detail |
|---|---|
| **Trigger** | Any query with location, planting, spraying, harvesting, or watering intent |
| **Data Source** | OpenWeatherMap One Call API 3.0 — current conditions + 5-day forecast |
| **Implementation** | Bedrock Agent Action Group invoking AWS Lambda |
| **Example Output** | "Do not spray your cocoa trees today — 80% chance of rain by 3pm will wash the chemicals away" |
| **Granularity** | City and LGA level using device GPS coordinates |

---

#### Feature 4: Sustainable Farming Advisor

Surfaces organic and low-cost alternatives to synthetic fertilizers, grounded in verified research documents for Nigerian and Sub-Saharan African soil conditions.

| Parameter | Detail |
|---|---|
| **Knowledge Source** | Organic Farming Guides for Sub-Saharan Africa ingested into Bedrock KB |
| **Query Types** | Fertilizer substitutes, composting, intercropping advice, organic pest control |
| **RAG Strategy** | Semantic search with metadata filtering by crop type and Nigerian region |
| **Output** | Step-by-step preparation instructions, estimated cost per hectare |

---

#### Feature 5: Live Market Price Intelligence

Farmers and traders query current commodity prices across major Nigerian markets and receive a best-market recommendation factoring in weather and transport conditions.

| Parameter | Detail |
|---|---|
| **Data Source** | AWS Lambda refreshing DynamoDB daily from AFEX API or public market price sources |
| **Markets Covered (MVP)** | Lagos Mile 12, Kano Dawanau, Onitsha, Gboko, Saki |
| **Crops Covered (MVP)** | Maize, cassava, beans, rice, tomatoes, yam, cocoa |
| **Output** | Price table by market, trend indicator, recommendation for best selling location |
| **Refresh Frequency** | Daily at 06:00 WAT via EventBridge scheduled Lambda |

---

### 2.2 Suggested Additional Features (Post-MVP)

| Feature | Description |
|---|---|
| **Soil Health Scanner** | Farmer describes soil colour and texture conversationally; AI infers deficiency and recommends amendments |
| **Personalised Planting Calendar** | Crop schedule based on LGA, rainfall patterns, and crop variety selection |
| **Farm Diary (Voice Log)** | Farmer narrates daily observations; AI structures them into a searchable farm record |
| **SMS/USSD Fallback** | Stripped-down interaction via Twilio + Africa's Talking for feature phone users |
| **Extension Worker Dashboard** | Web portal for government agronomists to review AI recommendations and add local overrides |
| **Yield Prediction Model** | Input planting date, soil type, variety, and weather to get predicted yield per hectare |
| **Pest Early Warning Network** | Aggregate diagnosis data to detect and alert on regional outbreaks |
| **WhatsApp Integration** | AgriSabi as a WhatsApp Business API chatbot (90%+ of Nigerian smartphone users are on WhatsApp) |
| **Cooperative Marketplace** | Peer-to-peer bulk-buying groups and commodity price negotiation within the platform |

---

## 3. Technology Stack

### 3.1 Full Stack Overview

| Layer | Technology | Purpose |
|---|---|---|
| Foundation Model | Claude 3.5 Sonnet (Bedrock) | Primary multimodal reasoning — vision, text, tool use |
| Cost Fallback Model | Amazon Nova Pro (Bedrock) | High-volume, cost-optimised text queries |
| Inference API | AWS Bedrock Converse API | Unified endpoint for text, image, and document inputs |
| RAG Engine | AWS Bedrock Knowledge Bases | Managed retrieval-augmented generation |
| Vector Store | Amazon OpenSearch Serverless | Embedding storage and semantic search |
| Agent Orchestration | AWS Bedrock Agents | Multi-step reasoning, memory, tool calling |
| Tool Functions | AWS Lambda (Python 3.12) | Weather API integration, Market Price refresh and lookup |
| Speech-to-Text | Amazon Transcribe (real-time) | Streaming STT for 4 Nigerian languages |
| Text-to-Speech | Amazon Polly Neural | Natural voice output in local languages |
| Backend API | FastAPI (Python 3.12) | REST API + SSE streaming; Bedrock orchestration layer |
| Frontend Framework | Next.js 14 (TypeScript) | Mobile-first PWA with App Router and Server Components |
| UI Components | Tailwind CSS + shadcn/ui | Component library and utility styling |
| Database | Amazon DynamoDB | User sessions, conversation history, market prices |
| File Storage | Amazon S3 | Document corpus, uploaded crop images, audio cache |
| CDN | Amazon CloudFront | Global asset delivery with WAF integration |
| Authentication | Amazon Cognito | JWT auth for registered users; anonymous identity for guests |
| Infrastructure as Code | AWS CDK (Python) | All cloud resources defined and deployed as code |
| CI/CD | GitHub Actions | Automated test and deploy pipeline on merge to main |
| Observability | CloudWatch + AWS X-Ray | Logs, distributed traces, latency alarms, dashboards |
| Content Safety | AWS Bedrock Guardrails | Topic filtering, PII redaction, hallucination controls |

### 3.2 Why AWS Bedrock

| Criterion | AWS Bedrock | Direct API (Anthropic/OpenAI) | Self-Hosted |
|---|---|---|---|
| Uptime SLA | 99.9% managed | 99.9% managed | Requires own infra team |
| RAG Integration | Native Knowledge Bases | Requires LangChain or custom build | Full custom build required |
| Voice Pipeline | Transcribe + Polly bundled | Requires separate third-party services | Requires separate third-party services |
| Nigerian Language STT | Hausa, Yoruba, Igbo in Transcribe | Limited or none | Model dependent |
| Data Residency | af-south-1 Cape Town region | US or EU data centres only | Flexible but complex |
| Guardrails | Native configurable filters | Custom implementation required | Custom implementation required |
| Operational Overhead | Fully managed | Partial | Very high |

---

## 4. System Architecture

### 4.1 Design Principles

- **No AWS SDK calls from the frontend.** All Bedrock, Transcribe, Polly, and DynamoDB calls are made server-side through FastAPI. Credentials never touch the browser.
- **Streaming first.** Chat responses are streamed via Server-Sent Events (SSE) so the user sees tokens as they are generated — critical for perceived latency on slow mobile connections.
- **Bedrock Agents, not LangChain.** The native AWS orchestration layer provides built-in retries, X-Ray tracing, memory, and Action Groups without adding dependency complexity.
- **Infrastructure as code for everything.** Every AWS resource is declared in CDK stacks, making the full environment reproducible across dev, staging, and production.

### 4.2 Request Flow — Voice Query Example

```
Step 1   Farmer presses mic button on the Next.js PWA (mobile browser)
Step 2   Audio streamed as PCM via HTTPS to POST /voice on FastAPI (ECS Fargate)
Step 3   FastAPI opens a real-time WebSocket to Amazon Transcribe and streams audio chunks
Step 4   Transcribe returns partial and final transcripts; language is auto-detected
Step 5   Final transcript sent to Bedrock Agent via invoke_agent()
Step 6   Agent reasons about the query — if weather intent detected, calls Weather Lambda Action Group
Step 7   Weather Lambda fetches OpenWeatherMap data, returns structured JSON to agent
Step 8   Agent synthesises final response in the farmer's detected language
Step 9   FastAPI sends response text to Amazon Polly for neural TTS synthesis
Step 10  MP3 audio stream returned to frontend for immediate playback
Step 11  Full conversation turn saved to DynamoDB (session_id, messages, timestamp)
```

### 4.3 Architecture Diagram

```
  [ Mobile PWA — Next.js ]
         |  HTTPS + SSE streaming
         v
  [ FastAPI Backend — ECS Fargate ]  <──  Cognito JWT auth
    |           |              |
    v           v              v
 Transcribe  Bedrock Agent  Polly TTS
  (STT)      /    |    \      (TTS)
            v     v     v
         KB RAG  LLM  Action Groups
       (OpenSearch)(Sonnet)(Lambda)
                        |        |
                     Weather   Market
                      API       API

  [ DynamoDB: sessions, history, market prices ]
  [ S3: documents corpus, image uploads, audio cache ]
```

### 4.4 Architecture Highlights

| Decision | Rationale |
|---|---|
| Bedrock Agents over LangChain | Native AWS integration, automatic retries, built-in X-Ray tracing, no external dependency management |
| FastAPI as the orchestration boundary | Centralises credentials, request validation, rate limiting, and structured logging |
| SSE streaming for chat responses | Users see tokens as they arrive — critical for perceived speed on 2G/3G mobile in rural Nigeria |
| DynamoDB for conversation history | Serverless millisecond reads, no RDS provisioning, scales to zero when idle |
| OpenSearch Serverless for vectors | Fully managed vector store — no cluster sizing, patching, or capacity planning |
| Cognito anonymous identity | Farmers use AgriSabi immediately without registration; session history preserved via anonymous Cognito identity |
| CDK for all infrastructure | Resources are version-controlled, environment-promotable, and reproducible in one command |
| Bedrock Guardrails at agent level | Prevents the agent from answering non-agricultural queries, protecting brand integrity |
| Primary region: af-south-1 Cape Town | Closest AWS region to Nigeria — lowest latency for audio streaming, reduces data residency concerns |

---

## 5. Project Structure

AgriSabi uses a **monorepo**. All application code, infrastructure definitions, AI agent configuration, and evaluation scripts live in a single repository.

```
agrisabi/
├── .github/
│   └── workflows/
│       ├── deploy.yml              # CDK deploy on merge to main
│       └── test.yml                # pytest + Jest on all PRs
│
├── infra/                          # AWS CDK stacks (Python)
│   ├── stacks/
│   │   ├── bedrock_stack.py        # Bedrock Agent, Knowledge Base, Guardrails
│   │   ├── lambda_stack.py         # Action Group Lambdas + shared layer
│   │   ├── storage_stack.py        # S3 buckets, OpenSearch Serverless collection
│   │   ├── auth_stack.py           # Cognito User Pool, Identity Pool, IAM roles
│   │   └── monitoring_stack.py     # CloudWatch dashboards, alarms, X-Ray config
│   ├── app.py                      # CDK entry point
│   └── cdk.json                    # CDK app configuration
│
├── backend/                        # FastAPI application
│   ├── app/
│   │   ├── main.py                 # Entry point — mounts routers, configures CORS
│   │   ├── config.py               # Pydantic BaseSettings — reads all env vars
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py         # POST /chat — text + image, SSE streaming
│   │   │   │   ├── voice.py        # POST /voice — audio → STT → agent → TTS → MP3
│   │   │   │   ├── diagnose.py     # POST /diagnose — multimodal image + disease RAG
│   │   │   │   ├── weather.py      # GET /weather?lat=&lng=
│   │   │   │   ├── market.py       # GET /market?crop=&region=
│   │   │   │   └── history.py      # GET /history/{session_id}
│   │   │   └── deps.py             # FastAPI dependency injection (boto3 clients)
│   │   ├── services/
│   │   │   ├── bedrock_agent.py    # invoke_agent() + SSE EventStream consumer
│   │   │   ├── bedrock_kb.py       # retrieve_and_generate() for direct RAG queries
│   │   │   ├── transcribe.py       # Real-time streaming STT WebSocket session
│   │   │   ├── polly.py            # Neural TTS — voice selection by language, MP3 stream
│   │   │   ├── vision.py           # Image resize, EXIF strip, base64 encode
│   │   │   └── dynamo.py           # save_message(), get_history(), create_session()
│   │   ├── models/
│   │   │   ├── schemas.py          # Pydantic request/response models for all routes
│   │   │   └── enums.py            # Language, CropType, DiseaseCategory, NigerianRegion
│   │   └── core/
│   │       ├── prompts.py          # AgriSabi system prompt + few-shot templates
│   │       ├── guardrails.py       # Guardrails IDs, topic deny-list, PII config
│   │       └── logger.py           # Structured JSON logging for CloudWatch Logs Insights
│   ├── tests/
│   │   ├── test_diagnose.py        # PlantVillage image diagnosis accuracy tests
│   │   ├── test_voice.py           # STT/TTS roundtrip tests with audio fixtures
│   │   └── test_rag.py             # IITA/NCRI knowledge retrieval accuracy tests
│   ├── Dockerfile                  # Container for ECS Fargate deployment
│   └── requirements.txt
│
├── lambdas/                        # Bedrock Agent Action Group functions
│   ├── weather_action/
│   │   ├── handler.py              # Calls OpenWeatherMap → returns farming advice JSON
│   │   └── requirements.txt
│   ├── market_action/
│   │   ├── handler.py              # Reads DynamoDB market prices → returns comparison
│   │   └── requirements.txt
│   └── shared/
│       └── utils.py                # Lambda layer: response formatting, error handling
│
├── knowledge-base/                 # RAG document corpus + ingestion scripts
│   ├── documents/
│   │   ├── iita/                   # IITA crop disease and management PDFs
│   │   ├── ncri/                   # NCRI rice and cereal research manuals
│   │   ├── organic-farming/        # Organic farming guides for Sub-Saharan Africa
│   │   └── plant-disease/          # PlantVillage disease description documents
│   ├── scripts/
│   │   ├── ingest.py               # Upload docs to S3 + sync Bedrock Knowledge Base
│   │   └── validate.py             # Test retrieval accuracy on sample queries
│   └── chunking_config.json        # Semantic chunking strategy (512 tokens, 20% overlap)
│
├── frontend/                       # Next.js 14 mobile-first PWA
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Landing — language selector + feature CTAs
│   │   │   ├── chat/page.tsx       # Main chat interface — text + image + SSE streaming
│   │   │   ├── voice/page.tsx      # Voice-first mode — mic button + waveform + playback
│   │   │   ├── diagnose/page.tsx   # Camera capture → disease result card
│   │   │   ├── market/page.tsx     # Live price dashboard — crop + region filter
│   │   │   └── layout.tsx          # Root layout — i18n, Cognito session, PWA metadata
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui base components
│   │   │   ├── ChatBubble.tsx      # Message renderer (text, image, audio, cards)
│   │   │   ├── VoiceRecorder.tsx   # MediaRecorder + VAD silence detection
│   │   │   ├── ImageCapture.tsx    # Camera/upload → compress → base64 submit
│   │   │   ├── LanguageSwitcher.tsx# Hausa / Yoruba / Igbo / Pidgin / English toggle
│   │   │   ├── WeatherAlert.tsx    # Proactive farming alert banner
│   │   │   └── MarketCard.tsx      # Price card with trend arrow + recommendation chip
│   │   ├── lib/
│   │   │   ├── api.ts              # Typed fetch wrappers for all backend routes + SSE
│   │   │   ├── i18n.ts             # next-intl config — loads locale JSON files
│   │   │   └── audio.ts            # Web Audio API — decodes and plays Polly MP3 streams
│   │   ├── hooks/
│   │   │   ├── useChat.ts          # Chat state + SSE EventSource consumer
│   │   │   ├── useVoice.ts         # State machine: idle → recording → responding → playing
│   │   │   └── useLocation.ts      # Geolocation permission + lat/lng for weather queries
│   │   └── locales/
│   │       ├── ha.json             # Hausa UI strings
│   │       ├── yo.json             # Yoruba UI strings
│   │       ├── ig.json             # Igbo UI strings
│   │       └── pcm.json            # Nigerian Pidgin UI strings
│   ├── public/                     # PWA icons, manifest.json, offline fallback page
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   └── Dockerfile                  # Next.js container for CloudFront + ECS
│
├── agents/
│   └── agrisabi_agent/
│       ├── system_prompt.md        # Master AgriSabi persona — identity, rules, tool use
│       ├── action_groups.json      # OpenAPI 3.0 schema for Weather + Market actions
│       └── guardrails_config.json  # Topic filters, PII types, grounding thresholds
│
├── scripts/
│   ├── setup_aws.sh                # Bootstrap AWS environment (IAM, S3, CDK bootstrap)
│   ├── local_dev.sh                # docker-compose up: FastAPI + Next.js + LocalStack
│   └── eval_agent.py               # Full evaluation harness — 50 image + 30 RAG tests
│
├── docker-compose.yml              # Local dev: FastAPI + Next.js + LocalStack
├── Makefile                        # make deploy | make test | make ingest-kb | make eval | make dev
├── .env.example                    # All required env vars with inline documentation
└── README.md                       # Setup guide, architecture diagram, demo video link
```

---

## 6. Core Services — Implementation Details

### 6.1 Bedrock Agent Service

The Bedrock Agent is the central orchestrator. It receives every user message, decides whether to query the Knowledge Base, invoke an Action Group Lambda, or respond directly, and produces the final answer.

| Parameter | Detail |
|---|---|
| **Agent ID** | Provisioned by CDK `bedrock_stack.py`; stored in `BEDROCK_AGENT_ID` env var |
| **Agent Alias** | Separate aliases for dev, staging, and prod — safe version promotion without downtime |
| **Streaming** | `invoke_agent()` with `enableTrace=True`; EventStream forwarded as SSE to frontend |
| **Session Management** | `sessionId` = Cognito identity sub + timestamp; enables multi-turn context |
| **Agent Memory** | Bedrock Agent memory enabled — retains last 20 turns within a session window |
| **Request Timeout** | 30 second invoke timeout; frontend shows animated typing indicator |
| **Retry Logic** | Exponential backoff — 3 retries on `ThrottlingException`: 1s, 2s, 4s delays |
| **Trace Logging** | All agent trace events logged to CloudWatch for latency analysis and debugging |

### 6.2 Knowledge Base (RAG) Service

| Parameter | Detail |
|---|---|
| **KB ID** | Provisioned by CDK; stored in `BEDROCK_KB_ID` env var |
| **Embedding Model** | Amazon Titan Embeddings v2 — 1536 dimensions |
| **Chunking Strategy** | Semantic chunking — max 512 tokens per chunk, 20% overlap |
| **Data Sources** | S3 bucket with four prefixes: `/iita/`, `/ncri/`, `/organic-farming/`, `/plant-disease/` |
| **Sync Trigger** | Lambda triggers KB sync on S3 `PutObject` events for new documents |
| **Retrieval Config** | Top 5 most relevant chunks; minimum relevance score threshold of 0.6 |
| **Metadata Filtering** | Filter by `crop_type`, `region`, and `document_source` at retrieval time |
| **Direct RAG Route** | `bedrock_kb.py` `retrieve_and_generate()` — used by extension worker dashboard |

### 6.3 Voice Pipeline

The voice pipeline chains four AWS services in sequence and must complete within 3 seconds total.

| Step | Detail |
|---|---|
| **1. Capture** | MediaRecorder API on device; PCM 16 kHz 16-bit mono; max 60 seconds |
| **2. STT** | Amazon Transcribe `StartStreamTranscription` WebSocket — real-time partial results |
| **3. Language Detection** | Transcribe `IdentifyLanguage` with `LanguageOptions`: `ha-SA`, `yo-NG`, `ig`, `en-NG` |
| **4. Reasoning** | Bedrock Agent `invoke_agent()` with transcript text; full KB and Action Group access |
| **5. TTS** | Amazon Polly `SynthesizeSpeech` with `Engine=neural`; voice selected by detected language |
| **6. Playback** | FastAPI streams MP3 bytes; frontend Web Audio API decodes and plays immediately |
| **Polly Voice Mapping** | Hausa: Zeina · Yoruba: Ola · Igbo: Eze (custom neural voice planned for Phase 2) |
| **Fallback** | Transcribe confidence below 0.7 → prompt farmer to speak more clearly and retry |

### 6.4 Vision and Diagnosis Service

| Parameter | Detail |
|---|---|
| **Image Input** | Multipart form upload; max 5 MB; JPEG and PNG only; auto-compressed on client |
| **Preprocessing** | `vision.py`: resize to 1024×1024 max, strip all EXIF metadata, base64 encode |
| **Prompt Strategy** | Two-stage: (1) describe visible symptoms; (2) RAG lookup to match symptoms to treatment |
| **Converse API Format** | `[{role: user, content: [{type: image, source: {type: base64}}, {type: text}]}]` |
| **Confidence Handling** | Model uncertainty → return 3 differential diagnoses with probability estimates |
| **Response Schema** | `disease_name`, `confidence`, `symptoms_observed`, `treatment_organic`, `treatment_chemical`, `dosage`, `precautions` |
| **Image Storage** | Uploaded to `agrisabi-uploads/` S3; EXIF stripped; 30-day auto-delete lifecycle |

### 6.5 Action Group Lambda Functions

#### Weather Action Group

| Parameter | Detail |
|---|---|
| **Trigger** | Agent detects location intent + weather, spray, plant, harvest, or watering keywords |
| **Lambda Input** | `{ latitude, longitude, query_type: spray \| plant \| harvest \| general }` |
| **External API** | OpenWeatherMap One Call API 3.0 — current conditions + hourly + daily forecast |
| **Output Schema** | `{ recommendation, raw_forecast, risk_level, advice_localized }` |
| **Advice Templates** | Hardcoded per `query_type` × weather condition combination for reliable localisation |

#### Market Price Action Group

| Parameter | Detail |
|---|---|
| **Trigger** | Agent detects price, market, sell, buy, or profit keywords |
| **Data Source** | DynamoDB `agrisabi_market_prices` table — refreshed daily at 06:00 WAT |
| **Price Refresh** | EventBridge rule triggers Lambda fetching AFEX API or scraped public price sources |
| **Output Schema** | `{ crop, prices_by_market: [{market, price_per_kg, price_per_bag, trend}], recommendation }` |

---

## 7. Database Design

### 7.1 Why DynamoDB

AgriSabi's access patterns are simple and key-based: fetch a session, append a message, or look up a market price. DynamoDB's sub-millisecond reads, zero idle cost on on-demand mode, and native AWS integration make it the right choice. No complex relational queries are needed in MVP scope.

### 7.2 Table: `agrisabi_sessions`

Stores all conversation sessions and full message history per session.

| Attribute | Type | Description |
|---|---|---|
| `session_id` **(PK)** | String | UUID generated on first visit; stored in browser and Cognito identity |
| `user_id` (GSI) | String | Cognito sub for registered users; `anonymous:{fingerprint}` for guests |
| `created_at` | String (ISO) | Session start timestamp |
| `updated_at` | String (ISO) | Timestamp of last message — used for TTL calculation |
| `language` | String | User selected language code: `ha`, `yo`, `ig`, `pcm`, or `en` |
| `messages` | List | Array of `{ role, content, timestamp, modality, image_s3_key? }` |
| `location` | Map | Last known `{ lat, lng, lga, state }` — updated on each weather query |
| `ttl` | Number (Unix) | Epoch timestamp — sessions auto-deleted after 90 days via DynamoDB TTL |

- **Partition Key:** `session_id`
- **GSI:** `user_id-index` — fetch all sessions for a registered user
- **TTL Attribute:** `ttl`
- **Capacity Mode:** On-demand

### 7.3 Table: `agrisabi_market_prices`

Stores current commodity prices by crop and market. Refreshed daily.

| Attribute | Type | Description |
|---|---|---|
| `crop#market` **(PK)** | String | Composite key e.g. `maize#kano_dawanau` |
| `price_per_kg` | Number | Price in Nigerian Naira per kilogram |
| `price_per_bag` | Number | Price per 50 kg bag — standard trading unit |
| `trend` | String | `up`, `down`, or `stable` compared to previous day |
| `market_name` | String | Human-readable market name for display |
| `state` | String | Nigerian state where market is located |
| `last_updated` | String (ISO) | Timestamp of last price refresh |
| `source` | String | `afex`, `manual`, or `scraped` |

### 7.4 Table: `agrisabi_users` *(Phase 2 — Registered Users)*

| Attribute | Type | Description |
|---|---|---|
| `user_id` **(PK)** | String | Cognito user sub |
| `phone_number` | String | E.164 format — for SMS fallback notifications |
| `preferred_language` | String | `ha`, `yo`, `ig`, `pcm`, or `en` |
| `lga` | String | Local Government Area for hyper-local advice |
| `state` | String | Nigerian state |
| `primary_crops` | List | Crops the farmer grows — personalises default context |
| `farm_size_ha` | Number | Estimated farm size in hectares |
| `created_at` | String (ISO) | Registration timestamp |

### 7.5 S3 Bucket Structure

```
agrisabi-documents/     # RAG corpus — IITA, NCRI, organic farming PDFs → synced to KB
agrisabi-uploads/       # Farmer image uploads — EXIF stripped, 30-day auto-delete
agrisabi-audio/         # Polly TTS cache — keyed by text hash, 24-hour auto-delete
agrisabi-static/        # Frontend PWA static assets
agrisabi-exports/       # Extension worker CSV/PDF exports (Phase 2)
```

---

## 8. AgriSabi Agent Persona & System Prompt

The system prompt is the most critical configuration in the product. It defines the agent's identity, knowledge scope, response style, language behaviour, tool use logic, and safety guardrails.

**Location in repo:** `agents/agrisabi_agent/system_prompt.md`  
**Injected at:** Agent creation time via CDK `bedrock_stack.py`

### 8.1 Prompt Design Principles

- **Localisation first.** Always respond in the user's detected or selected language. Never switch to English unless explicitly asked.
- **Simplicity over complexity.** "My cassava leaves are turning yellow" → actionable steps, not a biochemistry lecture.
- **Confidence calibration.** Express uncertainty clearly. Never hallucinate a treatment. If unsure, say so and defer to an extension worker.
- **Agricultural scope only.** Politely decline non-agricultural queries. Redirect medical, legal, or political questions to appropriate authorities.
- **Safety first.** Always include PPE and dosage precautions when recommending chemical treatments — even when not asked.
- **Source attribution.** Cite IITA or NCRI when using their data to build trust and credibility.

### 8.2 System Prompt Structure

| Block | Content |
|---|---|
| **Identity Block** | Who AgriSabi is, its purpose, its audience, and what it will and will not answer |
| **Language Block** | Language detection logic — how to identify query language and match response language |
| **Persona Block** | Tone: warm and knowledgeable, like a trusted uncle who is both a farmer and an agronomist |
| **Domain Rules Block** | Stay within agriculture; always query KB before answering; cite sources when possible |
| **Safety Block** | Mandatory PPE and dosage warnings; defer to extension worker for ambiguous edge cases |
| **Tool Use Block** | When to invoke Weather Action Group vs Market Action Group vs direct KB retrieval |
| **Format Rules Block** | Max 200 words per response; numbered lists for multi-step instructions; avoid jargon |
| **Fallback Block** | Unrecognised diseases, low image quality, no internet, ambiguous location queries |

---

## 9. Security & Privacy

| Risk | Mitigation |
|---|---|
| AWS credentials exposed in frontend | No SDK calls from the browser — all Bedrock, DynamoDB, and S3 calls made server-side by FastAPI |
| Unauthenticated access to session data | Cognito anonymous identity scopes each user to their own `session_id`; registered users need valid JWT |
| Prompt injection via user input | Bedrock Guardrails evaluate all inputs; FastAPI enforces max input length and regex sanitisation |
| PII stored in conversation history | Guardrails redact phone numbers and names; DynamoDB TTL auto-deletes sessions after 90 days |
| GPS location exposed via EXIF | `vision.py` strips all EXIF metadata from every uploaded image before storage or model processing |
| Hallucinated treatment advice | Guardrails confidence thresholds; system prompt enforces citation and uncertainty acknowledgement |
| API abuse and DDoS | CloudFront WAF rate limiting; per-Cognito-identity limit of 100 requests/minute via FastAPI middleware |
| Unauthorised Knowledge Base access | IAM resource policies restrict Bedrock KB read access to the ECS task role only |
| Harmful Action Group outputs | Bedrock Guardrails evaluate all Lambda Action Group outputs before returning to the user |
| Data residency | Primary deployment in `af-south-1` Cape Town — closest AWS region to Nigeria |

---

## 10. Development Roadmap

### 10.1 7-Day MVP Sprint

| Day | Focus Area | Key Deliverables |
|---|---|---|
| Day 1–2 | Infrastructure & Data | CDK stacks deployed to dev; S3 buckets created; IITA/NCRI PDFs ingested into Bedrock KB; OpenSearch provisioned |
| Day 3 | Agent Configuration | Bedrock Agent created via CDK; system prompt finalised; Action Group schemas registered; Guardrails configured |
| Day 4 | Multimodal Testing | Vision endpoint tested on 50 PlantVillage images; RAG retrieval validated on 30 sample queries |
| Day 5 | Frontend Development | Next.js PWA scaffolded; chat, voice, and diagnose pages connected to backend; i18n for all 4 languages wired |
| Day 6 | Guardrails & Edge Cases | Off-topic rejection tested; hallucination red-team complete; low-bandwidth simulation; anonymous sessions validated |
| Day 7 | Demo & Polish | Voice-to-voice demo recorded; disease diagnosis walkthrough recorded; README complete; staging live |

### 10.2 Phase 2 — 30 Days Post-MVP

- SMS and USSD fallback via Africa's Talking for feature phone users
- Soil Health Advisor — qualitative assessment via conversational prompts
- Personalised Planting Calendar — seasonal schedule based on LGA and rainfall
- Push notifications via Firebase Cloud Messaging for weather and pest alerts
- Extension Worker Portal — agronomist dashboard with recommendation review and override
- Custom Amazon Polly voices — fine-tuned Yoruba and Igbo neural voices

### 10.3 Phase 3 — 90 Days Post-MVP

- Pest Early Warning Network — aggregate diagnosis data to detect regional outbreaks
- Cooperative Marketplace — peer-to-peer trading and bulk-buying groups
- Yield Prediction Model — trained on Nigerian farm data
- Offline Mode — Service Worker caching of common diagnoses for zero-network use
- WhatsApp Integration — AgriSabi as a WhatsApp Business API chatbot
- Multi-region failover — `af-south-1` primary, `eu-west-1` Bedrock failover

---

## 11. Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `AWS_REGION` | Yes | AWS deployment region e.g. `af-south-1` |
| `AWS_ACCOUNT_ID` | Yes | AWS account ID for CDK deploy bootstrap |
| `BEDROCK_AGENT_ID` | Yes | Bedrock Agent resource ID from CDK output |
| `BEDROCK_AGENT_ALIAS_ID` | Yes | Agent alias ID — separate value per environment |
| `BEDROCK_KB_ID` | Yes | Knowledge Base ID from CDK output |
| `BEDROCK_GUARDRAIL_ID` | Yes | Guardrails configuration ID from CDK output |
| `COGNITO_USER_POOL_ID` | Yes | For JWT signature verification on protected routes |
| `COGNITO_IDENTITY_POOL_ID` | Yes | For issuing anonymous identity tokens to guest users |
| `DYNAMODB_SESSIONS_TABLE` | Yes | Table name: `agrisabi_sessions` |
| `DYNAMODB_MARKET_TABLE` | Yes | Table name: `agrisabi_market_prices` |
| `S3_DOCUMENTS_BUCKET` | Yes | Bucket containing the RAG corpus documents |
| `S3_UPLOADS_BUCKET` | Yes | Bucket for farmer-uploaded crop images |
| `OPENWEATHERMAP_API_KEY` | Yes | Stored in AWS Secrets Manager; referenced by Lambda ARN |
| `POLLY_DEFAULT_VOICE_ID` | No | Fallback voice if language detection fails (default: `Joanna`) |
| `MAX_TOKENS` | No | Bedrock max tokens per response (default: `1024`) |
| `LOG_LEVEL` | No | `INFO`, `DEBUG`, or `WARNING` (default: `INFO`) |
| `CORS_ALLOWED_ORIGINS` | Yes | Comma-separated list of allowed frontend origins |

### 11.1 Local Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/agrisabi/agrisabi.git && cd agrisabi

# 2. Set up environment variables
cp .env.example .env
# Fill in all required values in .env

# 3. Install CDK and configure AWS credentials
npm install -g aws-cdk
aws configure

# 4. Bootstrap the AWS environment
make setup
# Runs scripts/setup_aws.sh — creates IAM roles and S3 bootstrap bucket

# 5. Ingest knowledge base documents
make ingest-kb
# Uploads PDFs to S3 and triggers Bedrock Knowledge Base sync

# 6. Start local development
make dev
# docker-compose up: FastAPI + Next.js + LocalStack

# 7. Run the full test suite
make test
# pytest for backend + Jest for frontend

# 8. Deploy to staging
make deploy ENV=staging
```

---

## 12. Testing & Evaluation Strategy

| Test Type | Tool | What Is Tested | Pass Criteria |
|---|---|---|---|
| Unit Tests | pytest | FastAPI route handlers, service functions, DynamoDB operations | 100% of critical paths |
| Integration Tests | pytest + moto | Bedrock mock responses, S3 uploads, DynamoDB read/write | Zero regressions on deploy |
| Voice Pipeline E2E | pytest + audio fixtures | WAV file in → MP3 out; transcript accuracy on Nigerian speech | Word Error Rate < 15% |
| Disease Diagnosis Eval | `scripts/eval_agent.py` | 50 PlantVillage images across 5 Nigerian crop disease classes | Accuracy > 90% |
| RAG Retrieval Eval | `scripts/eval_agent.py` | 30 sample queries matched against IITA/NCRI reference answers | Correct retrieval > 85% |
| Guardrails Red-Team | Manual | Political, medical, off-topic, and adversarial prompts | 100% rejection rate |
| Load Testing | Locust | 100 concurrent voice + text sessions | P95 < 3s, zero errors |
| Frontend Unit Tests | Jest + React Testing Library | All components, hooks, and API client functions | All critical flows covered |
| Accessibility Audit | axe-core | Mobile PWA keyboard nav + screen reader compatibility | Zero critical violations |

### Evaluation Harness

```bash
make eval
```

Runs the full harness: **50 disease image tests + 30 RAG retrieval tests + 10 guardrail red-team prompts**.

- Results written to CloudWatch as custom metrics and printed as a terminal pass/fail summary
- GitHub Actions runs `make eval` automatically before any promotion to production
- A single failing test blocks the deploy and opens a GitHub issue with the failing case logged

---

## 13. Glossary

| Term | Definition |
|---|---|
| **RAG** | Retrieval-Augmented Generation — the model fetches relevant document chunks before generating an answer, grounding the response in verified sources |
| **Action Group** | A set of functions a Bedrock Agent can call to retrieve live data or perform external actions — similar to tool use in LLMs |
| **Bedrock Agent** | AWS managed orchestration layer handling multi-step reasoning, session memory, and Action Group invocations |
| **Knowledge Base (KB)** | AWS Bedrock managed document store with semantic search — the agent queries it to retrieve agricultural research before responding |
| **Converse API** | Unified AWS Bedrock API accepting text, images, and documents in a single request |
| **STT** | Speech-to-Text — Amazon Transcribe converts spoken audio to a text transcript in real-time |
| **TTS** | Text-to-Speech — Amazon Polly converts a text response to natural spoken audio using neural voices |
| **SSE** | Server-Sent Events — an HTTP protocol that streams data tokens from the server to the browser as they are generated |
| **Guardrails** | AWS Bedrock feature that filters both inputs and outputs for topic relevance, PII presence, and harmful content |
| **Session** | A conversation context identified by a unique `session_id`, enabling the agent to maintain multi-turn memory |
| **LGA** | Local Government Area — the lowest administrative division in Nigeria, used for hyper-local farming advice |
| **IITA** | International Institute of Tropical Agriculture — primary source of crop disease and management research for West Africa |
| **NCRI** | National Cereals Research Institute — Nigerian government research body for rice and cereal crops |
| **CDK** | AWS Cloud Development Kit — framework for defining cloud infrastructure as Python code |
| **WER** | Word Error Rate — standard metric for speech recognition accuracy |
| **VAD** | Voice Activity Detection — algorithm that detects when a speaker has stopped talking, used to auto-stop mobile recording |
| **ECS Fargate** | AWS serverless container hosting — runs the FastAPI Docker container without server management |

---

*AgriSabi v1.0 · Technical Project Documentation · Confidential — AgriSabi Dev Team*
