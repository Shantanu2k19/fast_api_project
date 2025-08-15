"""
Application configuration settings.
Uses Pydantic BaseSettings for environment variable management.
"""
from typing import List
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )
    
    # Application settings
    APP_NAME: str = "FastAPI Blog API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./blog.db"
    DATABASE_ECHO: bool = False
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate that SECRET_KEY is provided and has minimum length."""
        if not v:
            raise ValueError("SECRET_KEY must be provided")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v:
            raise ValueError("DATABASE_URL must be provided")
        return v
    
    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_token_expiry(cls, v: int) -> int:
        """Validate token expiry time."""
        if v < 1:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be at least 1")
        if v > 1440:  # 24 hours
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES cannot exceed 1440 (24 hours)")
        return v
    
    @field_validator("ALLOWED_HOSTS")
    @classmethod
    def validate_allowed_hosts(cls, v: List[str]) -> List[str]:
        """Validate allowed hosts list."""
        if not v:
            return ["*"]
        return v


# Global settings instance
settings = Settings()
