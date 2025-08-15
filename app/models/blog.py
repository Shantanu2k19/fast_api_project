"""
Blog model for blog post management.
Defines the database schema for blog posts.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class Blog(Base):
    """Blog model representing blog posts."""
    
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="blogs")
    
    def __repr__(self) -> str:
        return f"<Blog(id={self.id}, title='{self.title}', creator_id={self.creator_id})>"
    
    @property
    def excerpt(self) -> str:
        """Generate a short excerpt from the content."""
        if self.summary:
            return self.summary
        return self.content[:150] + "..." if len(self.content) > 150 else self.content
