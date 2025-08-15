"""
Blog-related Pydantic schemas for request/response validation.
Defines the data structures for blog operations.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class BlogBase(BaseModel):
    """Base blog schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Blog post title")
    content: str = Field(..., min_length=1, description="Blog post content")
    summary: Optional[str] = Field(None, max_length=500, description="Blog post summary")
    is_published: bool = Field(False, description="Publication status")


class BlogCreate(BlogBase):
    """Schema for creating a new blog post."""
    
    @validator('content')
    def validate_content_length(cls, v):
        """Validate content length."""
        if len(v.strip()) < 10:
            raise ValueError('Blog content must be at least 10 characters long')
        return v


class BlogUpdate(BaseModel):
    """Schema for updating blog post."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    is_published: Optional[bool] = None


class BlogInDB(BlogBase):
    """Internal blog schema with database fields."""
    
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BlogResponse(BlogBase):
    """Public blog response schema."""
    
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    excerpt: str
    
    class Config:
        from_attributes = True


class BlogWithCreator(BlogResponse):
    """Blog response schema including creator information."""
    
    creator: 'UserResponse'


class BlogListResponse(BaseModel):
    """Schema for blog list responses."""
    
    blogs: List[BlogResponse]
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool


# Import here to avoid circular imports
from app.schemas.user import UserResponse

# Update forward references
BlogWithCreator.model_rebuild()
