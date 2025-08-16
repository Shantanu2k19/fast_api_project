"""
Models package initialization.
Import all models here to ensure they are available when relationships are resolved.
"""

# Import models in the correct order to avoid circular dependencies
from app.models.user import User
from app.models.blog import Blog

# Now set up the relationships after both models are imported
def setup_relationships():
    """Set up model relationships after all models are imported."""
    from sqlalchemy.orm import relationship
    
    # Set up User -> Blog relationship
    User.blogs = relationship("Blog", back_populates="creator", cascade="all, delete-orphan")
    
    # Set up Blog -> User relationship
    Blog.creator = relationship("User", back_populates="blogs")

# Set up relationships
setup_relationships()

__all__ = ["User", "Blog"]
