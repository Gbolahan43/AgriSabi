
---

# 📄 Product Requirements Document (PRD): AgriSabi v1.0

## 1. Executive Summary

**AgriSabi** is a multimodal AI agent built on AWS Bedrock designed to provide Nigerian smallholder farmers with real-time, expert agricultural guidance. By leveraging **RAG** for localized research and **MCP** for real-time utility, AgriSabi bridges the gap between scientific agricultural research and rural field execution.

---

## 2. Target Features (MVP Scope)

### **A. Multimodal Disease Diagnosis (Vision-to-Text)**

* **Feature:** A farmer snaps a photo of a diseased leaf; the AI identifies the disease and prescribes a treatment.
* **Tech Stack:** AWS Bedrock **Claude 3.5 Sonnet** or **Amazon Nova Pro**.
* **RAG Integration:** The model identifies symptoms visually, then queries the **Bedrock Knowledge Base** (containing IITA/NCRI manuals) to fetch the specific chemical or organic treatment recommended for Nigeria.

### **B. Voice-First Interaction (Speech-to-Speech)**

* **Feature:** Non-literate farmers can speak in Hausa, Yoruba, Igbo, or Pidgin and receive a spoken response in the same language.
* **Tech Stack:** * **Input:** **Amazon Transcribe** (Real-time) to convert local dialects to text.
* **Reasoning:** **AWS Bedrock** (Text-to-Text).
* **Output:** **Amazon Polly** (using Neural voices) or **Bedrock Data Automation** for expressive, natural local language speech.



### **C. Climate-Resilient "Nowcasting" (MCP Tooling)**

* **Feature:** Proactive alerts based on micro-local weather.
* **Tech Stack:** **Bedrock Agent Action Groups (MCP)**.
* **Implementation:** The agent calls a **Weather API** (via Lambda) when it detects a location-based query. It translates "80% chance of rain" into "Do not spray your cocoa trees this afternoon; the rain will wash the chemicals away."

### **D. Sustainable Farming Advisor**

* **Feature:** Provides low-cost, organic alternatives to expensive synthetic fertilizers.
* **RAG Source:** Ingested "Organic Farming Guides for Sub-Saharan Africa."

---

## 3. Technical Architecture

### **The Stack Components:**

1. **Foundational Model:** **Claude 3.5 Sonnet** (for high-reasoning multimodal tasks) or **Amazon Nova** (for cost-optimized scaling).
2. **Knowledge Base (RAG):** **Amazon Bedrock Knowledge Bases** using **Amazon OpenSearch Serverless** or **S3 Vectors**.
3. **Action Groups (MCP):** **AWS Lambda** functions that connect the agent to:
* Live Weather Data (OpenWeatherMap).
* Live Market Prices (via a custom scraper or API).


4. **Security & Privacy:** **AWS IAM** and **Bedrock Guardrails** to filter out non-agricultural queries (e.g., ensuring the bot doesn't answer political questions).

---

## 4. User Personas & Use Cases

| User | Use Case | AgriSabi Value |
| --- | --- | --- |
| **Smallholder Farmer** | "Wetin dey worry my maize?" | Visual diagnosis + Pidgin audio explanation. |
| **Extension Worker** | "Give me the latest IITA treatment for Tuta Absoluta." | Rapid retrieval of verified scientific data (RAG). |
| **Market Trader** | "Should I buy beans from Kano or Benue today?" | Live price comparison and weather-based logistics advice. |

---

## 5. Development Roadmap (7-Day Sprint)

* **Day 1-2: Infrastructure & Data.** Set up AWS Environment. Create S3 buckets. Ingest IITA/NCRI PDFs into **Bedrock Knowledge Base**.
* **Day 3: Agent Configuration.** Create the **Bedrock Agent**. Write the "AgriSabi" System Prompt. Configure **Action Groups** for Weather.
* **Day 4: Multimodal Testing.** Test the model’s ability to recognize crop diseases using the **PlantVillage dataset**.
* **Day 5: Interface Development.** Build the mobile-first UI (Next.js/FastAPI) and connect the **AWS SDK (Boto3)**.
* **Day 6: Guardrails & Edge Cases.** Implement **Bedrock Guardrails** to prevent hallucinations and off-topic conversations.
* **Day 7: Final Demo & Polish.** Record the walkthrough video showcasing the **Voice-to-Voice** and **Vision** features.

---

## 6. Success Metrics

* **Accuracy:** >90% correct diagnosis of top 5 Nigerian crop diseases.
* **Latency:** <3 seconds for voice/text responses.
* **Inclusion:** 100% support for the 4 major Nigerian languages.

---