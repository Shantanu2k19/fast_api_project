"""
Logging configuration for the application.
Provides structured logging with different levels and outputs.
"""
import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to level name
        if record.levelname in self.COLORS:
            formatted = formatted.replace(
                record.levelname, 
                f"{color}{record.levelname}{reset}"
            )
        
        return formatted


def setup_logging(
    log_level: str = "INFO",
    log_file: str = None,
    enable_console: bool = True,
    enable_file: bool = False
) -> None:
    """Setup logging configuration."""
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "colored": {
                "()": ColoredFormatter,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {},
        "loggers": {
            "": {  # Root logger
                "level": log_level,
                "handlers": [],
                "propagate": True
            },
            "app": {  # Application logger
                "level": log_level,
                "handlers": [],
                "propagate": False
            },
            "uvicorn": {  # Uvicorn logger
                "level": "INFO",
                "handlers": [],
                "propagate": False
            },
            "sqlalchemy": {  # SQLAlchemy logger
                "level": "WARNING",
                "handlers": [],
                "propagate": False
            }
        }
    }
    
    # Add console handler
    if enable_console:
        config["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "colored" if sys.stdout.isatty() else "detailed",
            "stream": "ext://sys.stdout"
        }
        
        # Add console handler to all loggers
        for logger_name in config["loggers"]:
            config["loggers"][logger_name]["handlers"].append("console")
    
    # Add file handler
    if enable_file and log_file:
        config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": "json",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
        
        # Add file handler to all loggers
        for logger_name in config["loggers"]:
            config["loggers"][logger_name]["handlers"].append("file")
    
    # Apply configuration
    logging.config.dictConfig(config)
    
    # Set specific logger levels
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


def log_function_call(logger: logging.Logger, func_name: str = None):
    """Decorator to log function calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_logger = logger or get_logger(func.__module__)
            func_name_to_log = func_name or func.__name__
            
            func_logger.debug(f"Calling {func_name_to_log}")
            try:
                result = func(*args, **kwargs)
                func_logger.debug(f"Completed {func_name_to_log}")
                return result
            except Exception as e:
                func_logger.error(f"Error in {func_name_to_log}: {e}")
                raise
        return wrapper
    return decorator


def log_execution_time(logger: logging.Logger, func_name: str = None):
    """Decorator to log function execution time."""
    import time
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_logger = logger or get_logger(func.__module__)
            func_name_to_log = func_name or func.__name__
            
            start_time = time.time()
            func_logger.debug(f"Starting {func_name_to_log}")
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                func_logger.info(f"Completed {func_name_to_log} in {execution_time:.4f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                func_logger.error(f"Error in {func_name_to_log} after {execution_time:.4f}s: {e}")
                raise
        return wrapper
    return decorator


# Initialize logging on module import
if not logging.getLogger().handlers:
    setup_logging(
        log_level=settings.DEBUG and "DEBUG" or "INFO",
        enable_console=True,
        enable_file=False
    )
