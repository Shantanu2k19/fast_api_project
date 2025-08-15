"""
Main API router that includes all endpoint modules.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, blogs

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
