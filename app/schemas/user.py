"""
User-related Pydantic schemas for request/response validation.
Defines the data structures for user operations.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserInDB(UserBase):
    """Internal user schema with database fields."""
    
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Public user response schema."""
    
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWithBlogs(UserResponse):
    """User response schema including blogs."""
    
    blogs: List['BlogResponse'] = []


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserPasswordChange(BaseModel):
    """Schema for password change."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")
    
    @validator('new_password')
    def validate_new_password_strength(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Import here to avoid circular imports
from app.schemas.blog import BlogResponse

# Update forward references
UserWithBlogs.model_rebuild()
