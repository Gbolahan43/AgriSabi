# AgriSabi Advanced Integration Roadmap: MCP, Scraping & Geospatial APIs

To fully unlock AgriSabi's capabilities beyond static RAG, this implementation plan outlines how to deeply integrate the new agricultural resources—Model Context Protocol (MCP) servers, live market feeds, and geospatial data—into the backend architecture.

## 1. Model Context Protocol (MCP) Integration Strategy

Instead of hardcoding hundreds of custom API clients inside our Bedrock agents, we will deploy centralized, open-source MCP Servers that Claude 3.5 Sonnet can negotiate with natively.

### 1.1 Live Weather & Environmental Forecasts
*   **Resources Identified**: [OpenSource Weather MCP Servers](https://github.com/jezweb/weather-mcp-server), [Meteosource Local API](https://www.meteosource.com/weather-api-lagos), [WeatherSentry GA Edition](https://www.dtn.com/agriculture/agribusiness/weathersentry-global-agriculture-edition/).
*   **Implementation**: 
    - Deploy the `weather-mcp-server` via a lightweight Docker container on AWS ECS.
    - Provision Claude 3.5 Sonnet with the corresponding MCP definition.
    - *Actionable Use Case*: When a farmer asks "Should I apply pesticide today in Kano?", Claude queries the MCP tool natively for rain likelihood and instructs the farmer to postpone spraying if rain is forecasted.

### 1.2 Market Prices & Financial Data (AFEX)
*   **Resources Identified**: [AFEX Intelligence Portal/API](https://xip.afex.africa/market), [AlphaVantage MCP](https://github.com/alphavantage/alpha_vantage_mcp).
*   **Implementation**:
    - We will map the AFEX RapidAPI endpoint strictly into a custom MCP server since it represents Nigerian localized commodity prices.
    - *Actionable Use Case*: If a user queries the live price of Sorghum, the AI hits the AFEX endpoint natively via MCP to provide today's closing price.

## 2. Geospatial & Scientific API Connectors

### 2.1 Soil Mapping (iSDAsoil)
*   **Resources Identified**: [iSDAsoil API](https://www.isda-africa.com/isdasoil/), [AfSIS Maps](http://africasoils.net/).
*   **Implementation**:
    - Build a scraper/poller or direct API bridge hooking into iSDAsoil to derive local soil PH levels when a user shares their GPS zone. 
    - *Actionable Use Case*: By knowing a farmer is in Lagos (via the `user_profile` config), the Agent checks iSDAsoil parameters and tailors the optimal fertilizer N-P-K ratios required.

## 3. Web Scraping & Data Polling Architectures

### 3.1 Yielding the NAERLS Surveys
*   **Resources Identified**: [NAERLS Agricultural Performance Survey 2024](https://naerls.gov.ng/wp-content/uploads/2025/04/Agricultural-Performance-Survey-of-2024-Wet-Season-in-Nigeria.pdf)
*   **Implementation**:
    - We will write a scheduled AWS EventBridge chron job triggering a Lambda function (`agrisabi-scraper`).
    - The Lambda scans the NAERLS and NovusAgro portals looking for new PDF alerts or blog posts. It downloads them, automatically chunks them via LangChain, and injects them directly into our existing OpenSearch `agrisabi-kb` vector store.

## 4. NLP & Dialect Translation Refinements

### 4.1 Upgrading Transcribe Models (NaijaSenti & Lanfrica)
*   **Resources Identified**: [NaijaSenti Corpus](https://github.com/hausanlp/NaijaSenti), [Lanfrica Resources](https://lanfrica.com/).
*   **Implementation**:
    - Amazon Transcribe may occasionally struggle with deeply rural dialects. We can use the open-source NLP datasets gathered from Lanfrica to fine-tune a localized speech-to-text model (like taking advantage of Whisper fine-tunes mapped to Yoruba/Hausa/Igbo sentiment) if AWS Bedrock's default routing shows poor confidence levels in Tier-2 queries.
    - *Next Steps*: Investigate hosting an endpoint via AWS SageMaker loaded with a HausaNLP model as a fallback translation engine.
