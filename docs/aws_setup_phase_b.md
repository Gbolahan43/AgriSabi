# Phase B: Core AI Engine (AWS Bedrock Setup)

This guide walks you through standing up AgriSabi's intelligence layer. We will set up Model Access, Guardrails for safety, a Knowledge Base for RAG (Retrieval-Augmented Generation), and an Orchestration Agent.

## 1. Enable Model Access
Before you can use Bedrock, you must request access to the foundation models.
1. Log into your AWS Console and search for **Amazon Bedrock**.
2. In the left-hand navigation pane, scroll to the bottom and select **Model access**.
3. Click the orange **Modify model access** button in the top right.
4. Check the boxes for:
   - **Amazon Titan Embeddings G1 - Text** (Used for vectorizing your PDFs).
   - **Amazon Nova Sonic** (Used for Live Assistant voice interactions).
   - **Anthropic Claude 3.5 Sonnet** (Used for Two-Stage Crop Diagnosis).
5. Scroll down to the bottom right and click **Next / Submit**.
   *Note: Anthropic models often require filling out a brief use-case form.*

---

## 2. Create Bedrock Guardrails
AgriSabi must be restricted strictly to agricultural advice to prevent hallucinations, political debate, or medical diagnoses.
1. In Bedrock, go to **Safeguards** -> **Guardrails** in the left menu.
2. Click **Create guardrail**.
3. **Name**: Enter `agrisabi-agricultural-guardrail`. Click Next.
4. **Content filters**: Maximize filtering levels (High) for Hate, Insults, Sexual, and Prompt Attack blocks. Click Next.
5. **Denied topics**: 
   - Add a topic named `Non_Agricultural_Advice`.
   - Definition: `Any topic universally unrelated to crops, farming, market prices, livestock, or agricultural science. Specifically deny human medical advice, legal advice, or politics.`
   - Click Next.
6. **Word filters**: Skip / Leave blank. Click Next.
7. **PII filters**: Skip / Leave blank. Click Next.
8. **Review and create**: Review your settings and click Create.
9. **CRITICAL**: Once created, look at the Guardrail details page and copy the **Guardrail ID**. Paste this into your `backend/.env` file as `BEDROCK_GUARDRAIL_ID`.

---

## 3. Create the Knowledge Base (RAG)
This seamlessly connects your S3 PDFs to an OpenSearch Vector database.
1. In Bedrock, go to **Builder tools** -> **Knowledge bases**.
2. Click **Create knowledge base**.
3. **Name**: Enter `agrisabi-kb`. Let AWS create a new IAM role. Click Next.
4. **Data source**: 
   - Select **Amazon S3**.
   - Browse S3 and select the `knowledge-base` folder inside the bucket you created in Phase A. 
   - Click Next.
5. **Embeddings model**: Select **Titan Embeddings G1 - Text**.
6. **Vector store**: Leave it on **Quick create a new vector store**. (AWS will automatically spin up an Amazon OpenSearch Serverless collection in the background for you). Click Next.
7. Click **Create knowledge base** (This takes a few minutes as OpenSearch is provisioned).
8. Once finished, click the **Data source** tab on the KB page and click **Sync**. This reads your PDFs and vectorizes them.
9. **CRITICAL**: Copy the **Knowledge base ID** at the top of the page. Paste this into your `backend/.env` file as `BEDROCK_KB_ID`.

---

## 4. Create the Bedrock Agent
1. In Bedrock, go to **Builder tools** -> **Agents**. click **Create agent**.
2. **Name**: Enter `agrisabi-core-agent`.
3. **Model details**: Select **Anthropic Claude 3.5 Sonnet**.
4. **Instructions**: Copy the entire underlying text from our `TREATMENT_SYNTHESIS_PROMPT` (located in `app/core/prompts.py`) into this box. Add: *"You are an expert Nigerian agricultural extension worker."*
5. **Knowledge bases**: Click Add, and select the `agrisabi-kb` you just made. Write the instruction: *"Use this knowledge base to find treatment instructions for crop diseases based on symptoms."*
6. Click **Save** at the top.
7. **CRITICAL**: Click **Prepare** in the top right corner. Wait for the green success banner.
8. **Alias**: Click the **Create Alias** button. Name the alias `production` or `v1`.
9. **CRITICAL**: On the main Agent page, copy the **Agent ID**. Then, copy the **Alias ID**. Paste these into your `.env` file as `BEDROCK_AGENT_ID` and `BEDROCK_AGENT_ALIAS_ID`.
