"""
Authentication-related Pydantic schemas.
Defines the data structures for authentication operations.
"""
from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    """JWT token response schema."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in minutes")


class TokenData(BaseModel):
    """JWT token payload data."""
    
    email: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    """User login request schema."""
    
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class LoginResponse(BaseModel):
    """User login response schema."""
    
    access_token: str
    token_type: str
    expires_in: int
    user: dict


class RefreshTokenRequest(BaseModel):
    """Token refresh request schema."""
    
    refresh_token: str = Field(..., description="Refresh token")


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    
    email: str = Field(..., description="User's email address")


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")
