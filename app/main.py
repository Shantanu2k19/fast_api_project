"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging, get_logger
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.api.v1.api import api_router

# Setup logging
setup_logging(
    log_level=settings.DEBUG and "DEBUG" or "INFO",
    enable_console=True,
    enable_file=False
)

logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A scalable FastAPI blog application with authentication",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup middleware
setup_cors(app)
app.add_middleware(LoggingMiddleware)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with application information."""
    return {
        "message": "Welcome to FastAPI Blog API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION
    }

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    try:
        # Initialize database
        init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Application shutting down")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
