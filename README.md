# 🚜 AgriSabi: Enterprise AI for African Agriculture

**Bridging the Gap Between Research and the African Farmer.**

AgriSabi is a robust, multilingual AI assistant designed to provide smallholder farmers in Nigeria with a highly accurate agricultural extension agent, powered by enterprise-grade AI algorithms. 

---

## 🌍 The Problem
Nigeria’s agricultural sector operates with an extension worker to farmer ratio of approximately 1:10,000. This massive labor deficit causes critical, high-yield agricultural research (such as field manuals from the International Institute of Tropical Agriculture or ISDA soil databases) to become locked away in data silos. This vacuum of personalized advisory leaves rural farmers to face preventable yield loss, biological devastation, and input waste.

## 💡 System Functionality & Expectations
AgriSabi is expected to operate as a low-bandwidth, highly intelligent **Level 1 Agronomic Diagnostic Tool**. 

**Core System Functionality:**
* **Deep Diagnosis Hub:** Uses multi-modal vision models to allow farmers to upload photos of sick crops. The system physically extracts symptoms and cross-references them against institutional disease databases to present confidence-graded organic and chemical treatments.
* **Omni-Chat Advisory:** An interactive semantic chat built to interface natively with the user. It grounds its advice in agricultural fact architectures and live-fetches weather or soil data in the background seamlessly.
* **Localized Intelligence:** Prompt-engineered to securely handle and translate agricultural terminology effectively across Nigerian Pidgin, Hausa, Yoruba, and Igbo.

---

## 🤖 AI-Assisted System Development & Workflow
This project heavily leveraged autonomous **Agentic AI Coding workflows** to achieve rapid prototyping, complex cloud infrastructure deployment, and iterative debugging in record time.

* **Agentic Workflows:** The entire Next.js frontend, Python FastAPI orchestration layer, and infrastructure configuration were synthesized through active pair-programming with advanced AI Developer Agents possessing terminal and filesystem capabilities.
* **Tool Usage:** The AI agent utilized specialized developer tools, specifically:
  * **Automated Code Editing Tools:** Employed `replace_file_content` to semantically refactor complex files, inject trailing slashes for CORS bug fixing, and bind centralized `pydantic` configuration objects across multiple backend agents seamlessly.
  * **Shell & AWS CLI Tools:** The AI agent independently ran `aws amplify` and `aws apprunner` bash scripts directly from the workspace terminal. It diagnosed server logs (`aws logs`), caught AWS Bedrock Legacy Model exceptions automatically, patched Cross-Region Inference profile aliases (`us.anthropic...`), and configured continuous deployment pipelines—all without human keyboard intervention.

---

## 🏗️ Technology Stack & Architecture

AgriSabi utilizes a highly decoupled, serverless microservice architecture to easily scale across thousands of concurrent users while keeping costs extremely marginal.

### 1. Frontend Interface
* **Technologies:** Next.js 14, React, TailwindCSS, Zustand (State Management).
* **Architecture:** Deployed as a "Vibrant Glassmorphism" web application. It uses Server-Side Rendering (SSR) for blazing fast initial loads.

### 2. Backend Orchestration
* **Technologies:** Python, FastAPI, Pydantic, Boto3.
* **Architecture:** A rigid, strict, layered API routing environment.
  * `app/api`: Handles incoming REST queries from the Next.js client.
  * `app/orchestration`: The intelligent "Agents" (e.g., `advisory_agent`, `diagnosis_agent`) that build dynamic prompt injections, handle tool-use validation, and intercept multi-modal parameters.
  * `app/services`: Clean abstractions bridging the backend immediately to AWS Bedrock Converse endpoints and DynamoDB layers.

### 3. Databases & Context
* **AWS DynamoDB:** Utilized for high-throughput, low-latency session caching and market price tracking.
* **AWS OpenSearch Serverless (via Bedrock KB):** Fast, scalable vector database utilized underneath the architecture to parse through hundreds of ingested agronomic research papers instantaneously during Retrieval-Augmented Generation (RAG).

### 4. Containerization & CI/CD
* **Docker:** The backend relies entirely on `requirements.txt` build structures inside internal AWS Docker environments.
* **AWS App Runner Webhooks:** CI/CD is fully automated. Every `git push` to the `master` repository triggers an AWS CodeConnection webhook that instructs App Runner to securely containerize the deployment via GitHub instantly, applying active Environment Variable overrides dynamically.
* **AWS Amplify Pipelines:** The frontend UI automatically intercepts `master` commits and triggers a Node.js compilation pipeline deploying the updated static and SSR endpoints seamlessly to Edge CDNs.

### 5. Cloud Infrastructure (AWS Native)
* **Amazon Bedrock:** Powers the core AI capabilities securely without exposing API keys:
  * *Claude 3.7 Sonnet* (Cross-Region Inference) to synthesize complex multimodal logic routing.
  * *Amazon Nova Sonic* for potential rapid bidirectional speech inference.
  * *Bedrock Knowledge Bases* for seamless document ingestion protocols.

---

## 🚀 Getting Started

### 1. Requirements
* Git
* An AWS Account configured with IAM permissions for App Runner, Amplify, and Bedrock (Bedrock Model access for Claude 3.7 Sonnet must be actively requested safely via the AWS Console).

### 2. Deployment
Because the project's CI/CD relies directly on AWS App Runner and AWS Amplify:
1. Fork this repository.
2. Link your AWS Amplify Hosting console to the `frontend/` directory (ensure you add the `AMPLIFY_MONOREPO_APP_ROOT=frontend` variable).
3. Link AWS App Runner to the `backend/` directory providing it with your Bedrock KB string and IAM Instance roles.
