# AgriSabi: Enterprise AI for African Agriculture

**Bridging the Gap Between Research and the African Farmer.**

AgriSabi is a low-bandwidth, multilingual AI assistant designed to provide smallholder farmers in Nigeria with a highly accurate agricultural extension agent, powered by enterprise-grade AI algorithms. 

## The Problem
Nigeria’s agricultural sector operates with an extension worker to farmer ratio of approximately 1:10,000. This causes critical, high-yield agricultural research (such as manuals from the International Institute of Tropical Agriculture) to become locked away, leaving farmers to face preventable yield loss and input waste.

## The Solution
AgriSabi uses **Retrieval-Augmented Generation (RAG)** and **Model Context Protocol (MCP)** execution via models hosted on **AWS Bedrock** to ground the AI's responses exclusively in established agricultural fact and real-time weather APIs.

It is prompt-engineered to handle queries in localized languages such as Nigerian Pidgin, Hausa, Yoruba, and Igbo.

## System Architecture

1. **Frontend (TBD Phase 2):** A lightweight, browser-based chat built with Next.js, integrating the Web Speech API for voice interactions.
2. **Backend API:** Python FastAPI acting as the query orchestrator to handle contexts and coordinate RAG prompt routing. 
3. **Vector Database:** Local ChromaDB initialized `data_ingestion` pipelines processing embedded documents via `sentence-transformers`.
4. **AI Engine:** AWS Bedrock (Claude 3 Haiku) accessed via `boto3`.

## Getting Started

### 1. Requirements
* Python 3.10+
* An AWS Account with model access configured for Claude 3 Haiku via Bedrock.
* An OpenWeatherMap API Key.

### 2. Environment Setup
Configure your API keys in the `.env` file at `backend/.env` according to the template in `.env.example`.

### 3. Data Ingestion (Vector Database)
Initialize the dummy embedding database representing our "IITA Manuals":
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
Start the FastAPI orchestrator:
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```
You can then access the interactive API docs and test the RAG endpoints via Swagger at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
