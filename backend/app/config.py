import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "af-south-1"
    LOG_LEVEL: str = "INFO"
    CORS_ALLOWED_ORIGINS: str = "*"

    # Bedrock configuration
    BEDROCK_KB_ID: str = ""
    PRIMARY_MODEL_ID: str = "anthropic.claude-sonnet-4-5-20250929-v1:0"
    FALLBACK_MODEL_ID: str = "anthropic.claude-opus-4-6-v1:0"
    NOVA_SONIC_MODEL_ID: str = "amazon.nova-sonic-v1:0"

    # DynamoDB Tables
    AWS_TABLE_PREFIX: str = "dev_"
    DYNAMODB_SESSIONS_TABLE: str = f"{AWS_TABLE_PREFIX}agrisabi_sessions"
    DYNAMODB_MARKET_TABLE: str = f"{AWS_TABLE_PREFIX}agrisabi_market_prices"
    DYNAMODB_USERS_TABLE: str = f"{AWS_TABLE_PREFIX}agrisabi_users"

    class Config:
        env_file = ".env"

settings = Settings()
