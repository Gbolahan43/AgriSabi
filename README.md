# 🚜 AgriSabi: Enterprise AI for African Agriculture

**Bridging the Gap Between Research and the African Farmer.**

AgriSabi is a low-bandwidth, multilingual AI assistant designed to provide smallholder farmers in Nigeria with a highly accurate agricultural extension agent, powered natively by enterprise-grade AI algorithms securely housed in AWS.

---

## 🌍 The Problem
Nigeria’s agricultural sector operates with an extension worker to farmer ratio of approximately 1:10,000. This massive labor deficit causes critical, high-yield agricultural research (such as field manuals from the International Institute of Tropical Agriculture or ISDA soil databases) to become locked away in data silos. This vacuum of personalized advisory leaves rural farmers to face preventable yield loss, biological devastation, and input waste.

## 💡 System Functionality & How It Works
AgriSabi operates as a highly intelligent agronomic diagnostic tool. It relies deeply on **Retrieval-Augmented Generation (RAG)** hosted natively via **AWS Bedrock Knowledge Bases** to ground the AI's responses exclusively in established agricultural fact and real-time APIs.

**How It Works:**
* **Two-Stage Crop Diagnosis**:
  1. *Vision Pass*: A farmer uploads an image. Claude 3.7 Sonnet executes a Computer Vision protocol to extract exact physical symptoms (e.g., "yellowing leaf edges", "brown spots") *without* hallucinating a random condition.
  2. *RAG Resolution*: The extracted symptoms trigger a semantic database search directly into AWS Bedrock Knowledge Bases, retrieving verified agronomic research records to synthesize a highly accurate, confidence-graded organic and chemical treatment response.
* **Omni-Chat Advisory**:
  An interactive semantic chat interface that guides the farmer. To increase accuracy, this conversational agent holds the capability to autonomously trigger background Live APIs (such as OpenWeather APIs for hyper-local rain contexts or ISDA Soil API extraction) dynamically before replying to the farmer.
* **Localized Intelligence**:
  The system is prompt-engineered to securely handle, translate, and synthesize agricultural terminology seamlessly across English, Nigerian Pidgin, Hausa, Yoruba, and Igbo.

---

## 🤖 AI-Assisted System Development & Workflow
This project heavily leveraged autonomous **Agentic AI Coding workflows** to achieve rapid prototyping, complex cloud infrastructure deployment, and iterative debugging in record time.

* **Agentic Workflows:** The entire Next.js frontend, Python FastAPI orchestration layer, and infrastructure cloud configuration were synthesized through active pair-programming with advanced AI Developer Agents possessing terminal and filesystem capabilities.
* **Tool Usage & Capabilities:** The AI agent utilized specialized context tools, specifically:
  * **Automated Code Editing Tools:** Employed semantic edit routines to refactor complex files, inject API routing fixes, and bind centralized `pydantic` configuration objects dynamically across multiple Python agents seamlessly.
  * **Shell & AWS CLI Automation:** The AI agent independently executed `aws amplify` and `aws apprunner` bash scripts directly from the workspace IDE terminal. It diagnosed real-time cloud server logs, caught AWS Bedrock Legacy Model migration constraints autonomously, patched Cross-Region Inference profile aliases (`us.anthropic...`), and managed CI/CD deployment logic—all without human keyboard intervention.

---

## 🏗️ Technology Stack & System Architecture

AgriSabi utilizes a highly decoupled, serverless microservice architecture configured to scale automatically while keeping baseline costs extremely marginal.

### 1. Frontend Interface (Next.js 14 App Router)
* **Technologies:** Next.js 14, React, TailwindCSS, Zustand (State Management), Shadcn UI.
* **Architecture:** Deployed as a "Vibrant Glassmorphism" Progressive Web App (PWA). It features offline-caching capability for rural low-bandwidth areas and strict Server-Side Rendering (SSR) for robust initial distribution.

### 2. Backend Orchestration (FastAPI)
* **Technologies:** Python 3.11, FastAPI, Pydantic, Boto3.
* **Architecture:** A rigid, layered Python API that intelligently routes multi-modal requests:
  * `app/api`: Handles incoming REST queries and network handshakes.
  * `app/orchestration/agents`: The core AI engine managing AWS architecture. Builds dynamic prompt injections, manages Bedrock tool-use arrays (Weather/Soil schema extraction), and resolves the two-stage visual diagnosis flow safely.

### 3. Databases & Serverless Context
* **AWS DynamoDB:** Utilized securely for high-throughput, low-latency session conversation caching and fast market price iteration.
* **AWS Bedrock Knowledge Base (OpenSearch Serverless):** Fast, scalable vector storage intrinsically managed by AWS Bedrock. Used to parse thousands of semantic vectors of ingested agronomic research papers instantaneously without managing a standalone local database.

### 4. Continuous Deployment & Cloud Infrastructure
* **AWS App Runner (Serverless Containers):** The backend relies entirely on `requirements.txt` container deployments scaling massively on AWS App Runner triggered organically through Git Webhooks.
* **AWS Amplify (Edge Deployments):** The frontend UI intercepts `master` commits actively, compiling Next.js React bundles dynamically on Edge CDNs.
* **Amazon Bedrock Core:** Powers intelligence without exposing API logic directly. Relies strictly on *Claude 3.7 Sonnet* (Cross-Region Inference) to synthesize complex logic workflows automatically.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Node.js v18+ & npm
* Git
* An AWS Account configured with IAM permissions for App Runner, Amplify, and Bedrock.
  * **Critical:** Amazon Bedrock access for Claude 3.7 Sonnet must be actively requested safely via the AWS Console in your cross-region zone setup.
  * **Critical:** An active AWS Bedrock Knowledge Base (backed by OpenSearch) must be fully indexed with agronomic PDFs.
* An OpenWeatherMap API Key.

### 2. Environment Setup
Configure your API keys seamlessly. Locate the backend directory and duplicate the local `.env` file:
```bash
cp backend/.env.example backend/.env
```
Ensure your `BEDROCK_KB_ID` accurately matches the Knowledge Base string found in your AWS console.

### 3. Running the Backend API
Start the FastAPI orchestrator running on port `8080`:
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
Access the interactive API docs to test backend endpoints via Swagger at [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs).

### 4. Running the Frontend Server
Navigate to the frontend directory to run the Next.js development server on port `3000`. Ensure you have `.env.local` configured.
```bash
cd frontend
npm install
npm run dev
```

### 5. Cloud Deployment (CI/CD)
Because the project's CI/CD natively relies directly on AWS App Runner and AWS Amplify:
1. Push your stable workflow code to GitHub `master`.
2. Link your AWS Amplify Hosting console securely to your `/frontend` directory map (*ensure you explicitly inject the `AMPLIFY_MONOREPO_APP_ROOT=frontend` build logic string securely*).
3. Connect AWS App Runner to the GitHub `/backend` source, providing the deployment with identical AWS Bedrock Model Strings and App Runner IAM cross-service Roles to access DynamoDB and Bedrock seamlessly.
