"""
Blog service for business logic operations.
Handles blog creation, management, and retrieval.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from app.models.blog import Blog
from app.models.user import User
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse, BlogWithCreator, BlogListResponse
from app.core.exceptions import (
    NotFoundError, 
    ConflictError, 
    ValidationError, 
    DatabaseError,
    AuthorizationError
)

logger = logging.getLogger(__name__)


class BlogService:
    """Service class for blog-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_blog(self, blog_data: BlogCreate, creator_id: int) -> BlogResponse:
        """Create a new blog post."""
        try:
            # Verify creator exists
            creator = self.db.query(User).filter(User.id == creator_id).first()
            if not creator:
                raise NotFoundError("User")
            
            # Create blog post
            db_blog = Blog(
                title=blog_data.title,
                content=blog_data.content,
                summary=blog_data.summary,
                is_published=blog_data.is_published,
                creator_id=creator_id
            )
            
            self.db.add(db_blog)
            self.db.commit()
            self.db.refresh(db_blog)
            
            logger.info(f"Blog created successfully: {db_blog.title} by user {creator_id}")
            return BlogResponse.model_validate(db_blog)
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error creating blog: {e}")
            raise ConflictError("Blog creation failed due to database constraints")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating blog: {e}")
            raise DatabaseError("Failed to create blog")
    
    def get_blog_by_id(self, blog_id: int) -> BlogResponse:
        """Get blog by ID."""
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise NotFoundError("Blog")
            
            return BlogResponse.model_validate(blog)
            
        except Exception as e:
            logger.error(f"Error fetching blog {blog_id}: {e}")
            raise
    
    def get_blog_with_creator(self, blog_id: int) -> BlogWithCreator:
        """Get blog with creator information."""
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise NotFoundError("Blog")
            
            return BlogWithCreator.model_validate(blog)
            
        except Exception as e:
            logger.error(f"Error fetching blog with creator {blog_id}: {e}")
            raise
    
    def get_all_blogs(
        self, 
        skip: int = 0, 
        limit: int = 20, 
        published_only: bool = True
    ) -> BlogListResponse:
        """Get all blogs with pagination and filtering."""
        try:
            query = self.db.query(Blog)
            
            if published_only:
                query = query.filter(Blog.is_published == True)
            
            total = query.count()
            blogs = query.offset(skip).limit(limit).all()
            
            blog_responses = [BlogResponse.model_validate(blog) for blog in blogs]
            
            return BlogListResponse(
                blogs=blog_responses,
                total=total,
                page=(skip // limit) + 1,
                size=limit,
                has_next=(skip + limit) < total,
                has_prev=skip > 0
            )
            
        except Exception as e:
            logger.error(f"Error fetching blogs: {e}")
            raise DatabaseError("Failed to fetch blogs")
    
    def get_blogs_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> BlogListResponse:
        """Get blogs by specific user."""
        try:
            # Verify user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("User")
            
            query = self.db.query(Blog).filter(Blog.creator_id == user_id)
            total = query.count()
            blogs = query.offset(skip).limit(limit).all()
            
            blog_responses = [BlogResponse.model_validate(blog) for blog in blogs]
            
            return BlogListResponse(
                blogs=blog_responses,
                total=total,
                page=(skip // limit) + 1,
                size=limit,
                has_next=(skip + limit) < total,
                has_prev=skip > 0
            )
            
        except Exception as e:
            logger.error(f"Error fetching blogs for user {user_id}: {e}")
            raise DatabaseError("Failed to fetch user blogs")
    
    def update_blog(
        self, 
        blog_id: int, 
        blog_data: BlogUpdate, 
        user_id: int
    ) -> BlogResponse:
        """Update blog post."""
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise NotFoundError("Blog")
            
            # Check ownership
            if blog.creator_id != user_id:
                raise AuthorizationError("You can only update your own blog posts")
            
            # Update fields if provided
            update_data = blog_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(blog, field, value)
            
            self.db.commit()
            self.db.refresh(blog)
            
            logger.info(f"Blog {blog_id} updated successfully by user {user_id}")
            return BlogResponse.model_validate(blog)
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error updating blog {blog_id}: {e}")
            raise ConflictError("Blog update failed due to database constraints")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating blog {blog_id}: {e}")
            raise
    
    def delete_blog(self, blog_id: int, user_id: int) -> bool:
        """Delete a blog post."""
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise NotFoundError("Blog")
            
            # Check ownership
            if blog.creator_id != user_id:
                raise AuthorizationError("You can only delete your own blog posts")
            
            self.db.delete(blog)
            self.db.commit()
            
            logger.info(f"Blog {blog_id} deleted successfully by user {user_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting blog {blog_id}: {e}")
            raise
    
    def publish_blog(self, blog_id: int, user_id: int) -> BlogResponse:
        """Publish a blog post."""
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise NotFoundError("Blog")
            
            # Check ownership
            if blog.creator_id != user_id:
                raise AuthorizationError("You can only publish your own blog posts")
            
            blog.is_published = True
            self.db.commit()
            self.db.refresh(blog)
            
            logger.info(f"Blog {blog_id} published successfully by user {user_id}")
            return BlogResponse.model_validate(blog)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error publishing blog {blog_id}: {e}")
            raise
    
    def search_blogs(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 20
    ) -> BlogListResponse:
        """Search blogs by title or content."""
        try:
            search_query = f"%{query}%"
            blogs = self.db.query(Blog).filter(
                Blog.is_published == True,
                (Blog.title.ilike(search_query) | Blog.content.ilike(search_query))
            ).offset(skip).limit(limit).all()
            
            total = self.db.query(Blog).filter(
                Blog.is_published == True,
                (Blog.title.ilike(search_query) | Blog.content.ilike(search_query))
            ).count()
            
            blog_responses = [BlogResponse.model_validate(blog) for blog in blogs]
            
            return BlogListResponse(
                blogs=blog_responses,
                total=total,
                page=(skip // limit) + 1,
                size=limit,
                has_next=(skip + limit) < total,
                has_prev=skip > 0
            )
            
        except Exception as e:
            logger.error(f"Error searching blogs: {e}")
            raise DatabaseError("Failed to search blogs")
