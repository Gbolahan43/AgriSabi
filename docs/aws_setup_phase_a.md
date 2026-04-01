# Phase A: Storage Base Layer (AWS Setup)

This guide walks you through setting up the foundational storage layers required by AgriSabi: Amazon S3 (for Document & Audio Storage) and Amazon DynamoDB (for Session Memory).

## 1. Amazon S3 Setup
Amazon S3 will hold the raw PDF manuals (IITA, FAO) that Bedrock's Knowledge Base will read. It will also serve as a temporary staging ground for audio files if needed by the transcription pipelines later.

### Step-by-Step Instructions:
1. Log into your [AWS Management Console](https://console.aws.amazon.com/).
2. In the top search bar, type **S3** and select it from the services list.
3. Click the orange **Create bucket** button.
4. **General Configuration**:
   - **Bucket name**: Enter `agrisabi-prod-documents-[your-random-numbers-here]` (e.g., `agrisabi-prod-documents-19348`). Bucket names must be globally unique across all of AWS.
   - **AWS Region**: Select the region that matches your `.env` file (e.g., Africa Cape Town `af-south-1` or US East N. Virginia `us-east-1`).
5. **Object Ownership**: Leave at **ACLs disabled (recommended)**.
6. **Block Public Access settings for this bucket**: Check **Block all public access**. AgriSabi's backend uses secure AWS SDK calls; the bucket itself must never be public.
7. **Bucket Versioning**: Select **Enable**. This protects against accidental document overwriting or deletion.
8. **Default encryption**: Leave as **Amazon S3 managed keys (SSE-S3)**.
9. Click **Create bucket** at the bottom of the page.
10. Once created, click on your new bucket name in the list.
11. Click the **Create folder** button. Name the folder `knowledge-base`. Click Create.
12. Click into the `knowledge-base` folder and upload your agricultural PDF manuals directly here.

---

## 2. Amazon DynamoDB Setup
AgriSabi's backend and voice agents are largely stateless. We use DynamoDB as a high-speed NoSQL cache to remember the chat history for each unique session.

### Step-by-Step Instructions:
1. In the AWS Management Console search bar, type **DynamoDB** and select it.
2. In the left-hand navigation pane, click **Tables**, then click the orange **Create table** button.
3. **Table details**:
   - **Table name**: Enter `dev_agrisabi_sessions` (Or whatever your `AWS_TABLE_PREFIX` dictates in your `.env` file; e.g., if prefix is `dev_`, the name is `dev_agrisabi_sessions`).
   - **Partition key**: Enter `session_id`. Change the type dropdown to **String**.
   - **Sort key**: Leave this blank.
4. **Table settings**:
   - Select **Default settings** (this will provision read/write capacity limits which is perfectly fine and safe for MVP testing).
5. Click **Create table** at the bottom of the page.
6. Wait roughly 1 minute for the status to change from `Creating` to `Active`.

Your entire storage layer is now provisioned and secure.
