# 🚜 AgriSabi: Enterprise AI for African Agriculture

**Bridging the Gap Between Research and the African Farmer.**

AgriSabi is a low-bandwidth, multilingual AI assistant designed to provide smallholder farmers in Nigeria with a highly accurate agricultural extension agent, powered by enterprise-grade AI algorithms. 

## The Problem
Nigeria’s agricultural sector operates with an extension worker to farmer ratio of approximately 1:10,000. This causes critical, high-yield agricultural research (such as manuals from the International Institute of Tropical Agriculture) to become locked away, leaving farmers to face preventable yield loss and input waste.

## The Solution
AgriSabi uses **Retrieval-Augmented Generation (RAG)** hosted on **AWS Bedrock** to ground the AI's responses exclusively in established agricultural fact and real-time weather APIs. 

It is prompt-engineered to handle queries in localized languages such as Nigerian Pidgin, Hausa, Yoruba, and Igbo natively.

---

## 🏗️ System Architecture (v1.1)

### 1. Frontend (Next.js 14 App Router)
A "Vibrant Glassmorphism" Progressive Web App (PWA) built with **Tailwind CSS**, **Shadcn UI**, and **Zustand**. It features realtime Voice Visualizers and allows offline-caching for rural low-bandwidth areas.

### 2. Backend Orchestration (FastAPI)
A strict, layered Python API that intelligently routes multi-modal requests:
- `api/`: REST and WebSocket endpoints.
- `orchestration/`: Agents handling business logic (advisory, voice routing, context enrichment).
- `services/`: Wrappers for AWS services (Bedrock, Transcribe, Polly).

### 3. Core AI Features
- **Two-Stage Crop Diagnosis**:
  1. *Vision Pass*: Claude 3.5 Sonnet extracts exact physical symptoms from an uploaded image without hallucinating a disease name.
  2. *RAG Pass*: Symptoms trigger a semantic search in ChromaDB, retrieving verified treatment manuals to synthesize a grounded diagnosis.
- **Three-Tier Voice Ecosystem**:
  1. *Nova Sonic Live Assistant*: A low-latency, bidirectional Bedrock WebSocket stream for real-time conversational English/Pidgin.
  2. *Native Language Router*: Audio is intercepted by Amazon Transcribe, identified by language, processed via text, and synthesized back to speech via Amazon Polly (Hausa, Yoruba, Igbo).

---

## 🚀 Getting Started

### 1. Requirements
* Python 3.10+
* Node.js & npm (for Frontend)
* An AWS Account configured with:
  * Claude 3.5 Sonnet
  * Amazon Nova Sonic
  * Bedrock Knowledge Base (Optional for direct OpenSearch integration)
* An OpenWeatherMap API Key.

### 2. Environment Setup
Configure your API keys in the `.env` file at `backend/.env` utilizing the template provided in `backend/.env.example`.

### 3. Initialize the Vector Database (Local RAG)
Populate the dummy ChromaDB embedding database representing our "IITA Manuals":
```bash
cd data_ingestion
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python ingest.py
```

### 4. Running the Backend API
Start the FastAPI orchestrator running on port `8000`:
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
Access the interactive API docs and test the RAG endpoints via Swagger at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Running the Frontend Server
Navigate to the frontend directory to run the Next.js development server on port `3000`:
```bash
cd frontend
npm install
npm run dev
```
