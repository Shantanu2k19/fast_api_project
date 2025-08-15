"""
Blog management endpoints for CRUD operations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.exceptions import NotFoundError, ConflictError, ValidationError, AuthorizationError
from app.schemas.blog import (
    BlogCreate, 
    BlogUpdate, 
    BlogResponse, 
    BlogWithCreator, 
    BlogListResponse
)
from app.services.blog_service import BlogService
from app.services.auth_service import get_current_active_user_dependency, User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog_data: BlogCreate,
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Create a new blog post.
    
    Args:
        blog_data: Blog creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created blog information
        
    Raises:
        HTTPException: If blog creation fails
    """
    try:
        blog_service = BlogService(db)
        blog = blog_service.create_blog(blog_data, current_user.id)
        
        logger.info(f"Blog created successfully: {blog.title} by user {current_user.id}")
        return blog
        
    except ValidationError as e:
        logger.warning(f"Blog creation validation error: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Blog creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create blog"
        )


@router.get("/", response_model=BlogListResponse, status_code=status.HTTP_200_OK)
async def get_blogs(
    skip: int = Query(0, ge=0, description="Number of blogs to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of blogs to return"),
    published_only: bool = Query(True, description="Show only published blogs"),
    db: Session = Depends(get_db)
):
    """
    Get all blogs with pagination and filtering.
    
    Args:
        skip: Number of blogs to skip
        limit: Maximum number of blogs to return
        published_only: Show only published blogs
        db: Database session
        
    Returns:
        Paginated list of blogs
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        blog_service = BlogService(db)
        blogs = blog_service.get_all_blogs(
            skip=skip, 
            limit=limit, 
            published_only=published_only
        )
        
        return blogs
        
    except Exception as e:
        logger.error(f"Error fetching blogs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch blogs"
        )


@router.get("/search", response_model=BlogListResponse, status_code=status.HTTP_200_OK)
async def search_blogs(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0, description="Number of blogs to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of blogs to return"),
    db: Session = Depends(get_db)
):
    """
    Search blogs by title or content.
    
    Args:
        q: Search query
        skip: Number of blogs to skip
        limit: Maximum number of blogs to return
        db: Database session
        
    Returns:
        Paginated search results
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        blog_service = BlogService(db)
        blogs = blog_service.search_blogs(
            query=q,
            skip=skip,
            limit=limit
        )
        
        return blogs
        
    except Exception as e:
        logger.error(f"Error searching blogs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search blogs"
        )


@router.get("/my-blogs", response_model=BlogListResponse, status_code=status.HTTP_200_OK)
async def get_my_blogs(
    skip: int = Query(0, ge=0, description="Number of blogs to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of blogs to return"),
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Get current user's blog posts.
    
    Args:
        skip: Number of blogs to skip
        limit: Maximum number of blogs to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Paginated list of user's blogs
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        blog_service = BlogService(db)
        blogs = blog_service.get_blogs_by_user(
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        
        return blogs
        
    except Exception as e:
        logger.error(f"Error fetching user blogs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user blogs"
        )


@router.get("/{blog_id}", response_model=BlogWithCreator, status_code=status.HTTP_200_OK)
async def get_blog(
    blog_id: int,
    db: Session = Depends(get_db)
):
    """
    Get blog by ID with creator information.
    
    Args:
        blog_id: Blog ID to fetch
        db: Database session
        
    Returns:
        Blog with creator information
        
    Raises:
        HTTPException: If blog not found
    """
    try:
        blog_service = BlogService(db)
        blog = blog_service.get_blog_with_creator(blog_id)
        
        return blog
        
    except NotFoundError as e:
        logger.warning(f"Blog not found: {blog_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error fetching blog {blog_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch blog"
        )


@router.put("/{blog_id}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Update a blog post.
    
    Args:
        blog_id: Blog ID to update
        blog_data: Blog update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated blog information
        
    Raises:
        HTTPException: If update fails
    """
    try:
        blog_service = BlogService(db)
        blog = blog_service.update_blog(blog_id, blog_data, current_user.id)
        
        logger.info(f"Blog {blog_id} updated successfully by user {current_user.id}")
        return blog
        
    except NotFoundError as e:
        logger.warning(f"Blog not found for update: {blog_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AuthorizationError as e:
        logger.warning(f"Authorization error updating blog {blog_id}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )
    except ValidationError as e:
        logger.warning(f"Blog update validation error: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Blog update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update blog"
        )


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Delete a blog post.
    
    Args:
        blog_id: Blog ID to delete
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If deletion fails
    """
    try:
        blog_service = BlogService(db)
        blog_service.delete_blog(blog_id, current_user.id)
        
        logger.info(f"Blog {blog_id} deleted successfully by user {current_user.id}")
        
    except NotFoundError as e:
        logger.warning(f"Blog not found for deletion: {blog_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AuthorizationError as e:
        logger.warning(f"Authorization error deleting blog {blog_id}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Blog deletion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete blog"
        )


@router.post("/{blog_id}/publish", response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def publish_blog(
    blog_id: int,
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Publish a blog post.
    
    Args:
        blog_id: Blog ID to publish
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Published blog information
        
    Raises:
        HTTPException: If operation fails
    """
    try:
        blog_service = BlogService(db)
        blog = blog_service.publish_blog(blog_id, current_user.id)
        
        logger.info(f"Blog {blog_id} published successfully by user {current_user.id}")
        return blog
        
    except NotFoundError as e:
        logger.warning(f"Blog not found for publishing: {blog_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except AuthorizationError as e:
        logger.warning(f"Authorization error publishing blog {blog_id}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Blog publishing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish blog"
        )
