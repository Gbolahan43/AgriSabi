import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AWS_REGION: str = "us-west-2"
    LOG_LEVEL: str = "INFO"
    CORS_ALLOWED_ORIGINS: str = "*"

    # Bedrock configuration
    BEDROCK_REGION: str = "us-west-2"
    BEDROCK_KB_ID: str = ""
    PRIMARY_MODEL_ID: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    FALLBACK_MODEL_ID: str = "us.amazon.nova-lite-v1:0"
    NOVA_SONIC_MODEL_ID: str = "us.amazon.nova-sonic-v1:0"
    S3_BUCKET: str = "agrisabi-audio-bucket-774305598371-us-west-2"

    # DynamoDB Tables
    AWS_TABLE_PREFIX: str = "prod_"
    DYNAMODB_SESSIONS_TABLE: str = "prod_agrisabi_sessions"
    DYNAMODB_MARKET_TABLE: str = "prod_agrisabi_market_prices"
    DYNAMODB_USERS_TABLE: str = "prod_agrisabi_users"

    @property
    def KNOWLEDGE_BASE_ID(self) -> str:
        """Alias for BEDROCK_KB_ID for compatibility with rag.py"""
        return self.BEDROCK_KB_ID

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
