"""
Configuration management for the application.
Handles environment variables, database settings, and JWT configuration.
"""
import os
from typing import Optional
from pydantic import BaseSettings, validator
from pydantic.types import SecretStr


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "FastAPI Blog API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./blog.db"
    DATABASE_ECHO: bool = False
    
    # Security
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: list = ["*"]
    
    @validator("SECRET_KEY", pre=True)
    def validate_secret_key(cls, v):
        if not v:
            raise ValueError("SECRET_KEY must be set")
        return v
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
