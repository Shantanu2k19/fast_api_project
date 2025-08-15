#!/usr/bin/env python3
"""
Startup script for FastAPI Blog API.
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.config import settings
from app.core.logging import setup_logging, get_logger

def main():
    """Main startup function."""
    # Setup logging
    setup_logging(
        log_level=settings.DEBUG and "DEBUG" or "INFO",
        enable_console=True,
        enable_file=False
    )
    
    logger = get_logger(__name__)
    
    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        logger.warning(".env file not found. Please create one from env.example")
        logger.info("Using default configuration")
    
    # Start the application
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()
