# AgriSabi Production Deployment Guide

This document outlines the step-by-step process for deploying the AgriSabi platform to AWS production. The architecture follows a strict decoupled pattern: the Next.js frontend is distributed to the Edge for maximum speed, while the Python FastAPI backend sits in a secure containerised environment.

---

## 1. Architecture Overview 🏗️

| Component | Technology | AWS Service Target | Why? |
| :--- | :--- | :--- | :--- |
| **Frontend** | Next.js 14, Tailwind | **AWS Amplify Hosting** | Native Next.js SSR support, global CloudFront CDN caching, zero-downtime CI/CD from GitHub. |
| **Backend API** | FastAPI (Python 3.12) | **AWS App Runner / ECS** | Auto-scaling container service tailored for HTTP web APIs, native IAM integration for Bedrock. |
| **Cloud Infra**| Python AWS CDK | **CloudFormation** | Reproducible configuration for DynamoDB and IAM roles. |

---

## 2. Prerequisites 🔑
Before beginning deployment, ensure the following are configured:
1. **AWS CLI** installed and authenticated (`aws configure`).
2. An active **GitHub branch** pushing both the `frontend/` and `backend/` directories.
3. IAM Administrator Access on the AWS account.
4. AWS Bedrock Model Access granted specifically in `us-east-1` for **Claude 3.5 Sonnet**, **Nova Pro**, and **Nova Sonic**.

---

## 3. Phase A: Deploying Cloud Infrastructure (CDK)
First, we must deploy the foundational layers (DynamoDB Sessions table, IAM roles).

1. Navigate to the infrastructure folder.
   ```bash
   cd infra
   ```
2. Bootstrap the AWS environment (if this is the first time using CDK on this AWS account).
   ```bash
   npx aws-cdk bootstrap aws://YOUR_ACCOUNT_ID/us-east-1
   ```
3. Deploy the core stacks.
   ```bash
   npx aws-cdk deploy --all
   ```
*This will provision the `agrisabi_sessions` DynamoDB table and output any created IAM Role ARNs.*

---

## 4. Phase B: Deploying the Backend (AWS App Runner)
We use AWS App Runner to deploy the FastAPI backend. It pulls directly from your GitHub repository or a Docker image and creates a live HTTPS endpoint effortlessly.

### Step 4.1: Containerization
Ensure your `backend/Dockerfile` is structurally sound. 
```dockerfile
# backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 4.2: App Runner Setup
1. Navigate to **AWS App Runner** in the AWS Console.
2. Select **Create Service**.
3. Choose **Source Code Repository** and link your GitHub repo.
4. Set the source directory to `/backend`.
5. **Runtime**: Python 3.11/3.12.
6. **Build Command**: `pip install -r requirements.txt`
7. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
8. **Port**: `8000`

### Step 4.3: Environment & Security
Under *Environment Variables* in the App Runner setup array, strictly inject:
*   `AWS_REGION=us-east-1`
*   `PRIMARY_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0`
*   `KNOWLEDGE_BASE_ID=your_opensearch_kb_id`
*   `OPENWEATHER_API_KEY=your_weather_key`

> **CRITICAL**: Under *Security > Instance Role*, you MUST assign an IAM Role that has `AmazonBedrockFullAccess` and `AmazonDynamoDBFullAccess`. Without this, FastAPI cannot talk to Claude or save session history.

**Result**: AWS App Runner will spin up the server and give you a public URL (e.g., `https://xyzabc.us-east-1.awsapprunner.com`). Save this URL.

---

## 5. Phase C: Deploying the Frontend (AWS Amplify)
The Next.js frontend needs to hit the Edge CDN.

1. Navigate to **AWS Amplify** in the AWS Console.
2. Select **Host Web App** and choose GitHub.
3. Select your AgriSabi repository and branch.
4. **App Settings**: 
   When prompted for build settings, point the build directory to the `frontend/` folder.
5. **Environment Variables**:
   Inject the backend URL so Next.js knows where to point the React API layer.
   * `NEXT_PUBLIC_API_URL=https://xyzabc.us-east-1.awsapprunner.com/api/v1`
6. Click **Deploy**.

AWS Amplify will automatically run `npm run build`, build the Next.js routes, and deploy the entire UI onto Amazon CloudFront edge nodes. It will generate a live URL (e.g., `https://main.d2xyehf.amplifyapp.com`).

---

## 6. Post-Deployment Verification ✅

1. **Test the UI**: Load the live Amplify URL. Verify that CSS and images (like `harvest_mockup.png`) are loading correctly without 404s.
2. **Test the CORS**: Attempt to use the Chat or Diagnostic feature. If you receive a CORS error in the browser console, ensure your FastAPI `CORSMiddleware` in `backend/app/main.py` has the Amplify domain whitelisted.
    ```python
    origins = [
        "https://main.d2xyehf.amplifyapp.com",
    ]
    ```
3. **Test the Pipeline**: Upload a leaf image to the Diagnose Hub on the live site. Verify the AWS App Runner logs (in AWS CloudWatch) to ensure it reaches Bedrock and returns the `DiagnosisResponse` successfully.
