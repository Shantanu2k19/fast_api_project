"""
Blog-related Pydantic schemas for data validation and serialization.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class BlogBase(BaseModel):
    """Base blog schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Blog post title")
    content: str = Field(..., min_length=10, description="Blog post content")
    summary: Optional[str] = Field(None, max_length=500, description="Blog post summary")
    is_published: bool = Field(False, description="Publication status")


class BlogCreate(BlogBase):
    """Schema for creating a new blog post."""
    
    @field_validator('content')
    @classmethod
    def validate_content_length(cls, v: str) -> str:
        """Validate content length."""
        if len(v) < 10:
            raise ValueError('Content must be at least 10 characters long')
        if len(v) > 10000:
            raise ValueError('Content cannot exceed 10,000 characters')
        return v


class BlogUpdate(BaseModel):
    """Schema for updating blog post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Blog post title")
    content: Optional[str] = Field(None, min_length=10, description="Blog post content")
    summary: Optional[str] = Field(None, max_length=500, description="Blog post summary")
    is_published: Optional[bool] = Field(None, description="Publication status")


class BlogInDB(BlogBase):
    """Blog schema as stored in database."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class BlogResponse(BlogBase):
    """Blog schema for API responses."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    excerpt: str


class BlogWithCreator(BlogResponse):
    """Blog schema with creator information."""
    creator: dict = {}  # Using dict instead of UserResponse to avoid circular import


class BlogListResponse(BaseModel):
    """Paginated blog list response."""
    blogs: List[BlogResponse]
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool
