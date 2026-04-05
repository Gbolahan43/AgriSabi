import os
import json
import requests
from bs4 import BeautifulSoup
import boto3

KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

def fetch_naerls_news() -> list:
    """
    Scrapes the NAERLS platform for the latest warnings, subsidized fertilizer alerts, 
    and seasonal performance surveys.
    """
    base_url = "https://naerls.gov.ng/category/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        extracted_data = []
        
        # Target loop for standard WordPress/NAERLS article blocks
        for post in soup.find_all('article'):
            title_tag = post.find('h2', class_='entry-title')
            link_tag = title_tag.find('a') if title_tag else None
            excerpt_tag = post.find('div', class_='entry-content') or post.find('div', class_='entry-summary')
            
            if title_tag and link_tag:
                extracted_data.append({
                    "source": "NAERLS Agricultural Alert",
                    "title": title_tag.text.strip(),
                    "link": link_tag['href'],
                    "summary": excerpt_tag.text.strip() if excerpt_tag else "",
                    "timestamp": "Scraped Daily Run"
                })
        
        return extracted_data
    except Exception as e:
        print(f"[NAERLS Scrape Error] {e}")
        return []

def vectorize_to_opensearch(documents):
    """
    Chunks textual data and syncs it to the AWS OpenSearch Knowledge Base via Bedrock's Data Source API.
    A true implementation would push these texts to the S3 bucket tied to the KB, 
    and trigger a `start_ingestion_job`.
    """
    if not KNOWLEDGE_BASE_ID:
        print("Warning: KNOWLEDGE_BASE_ID not found. Skipping vectorization.")
        return
        
    # Standard flow:
    # 1. Save list mapping to `s3://agrisabi-documents/scraped_daily/naerls_current.json`
    # 2. boto3.client('bedrock-agent').start_ingestion_job(...)
    print(f"Simulating Bedrock Ingestion Job trigger for {len(documents)} documents.")
    pass

def handler(event, context):
    """
    AWS Lambda entry point. Triggers every 24 hours via EventBridge Cron.
    """
    print("Initiating AgriSabi Nightly Scraper...")
    
    naerls_alerts = fetch_naerls_news()
    if naerls_alerts:
        print(f"Successfully pulled {len(naerls_alerts)} articles from NAERLS.")
        vectorize_to_opensearch(naerls_alerts)
        
    # Future scaling: Add AgroNigeria, FAO, etc.
    
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "success", "articles_processed": len(naerls_alerts)})
    }
