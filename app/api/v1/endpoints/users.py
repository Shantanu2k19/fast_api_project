"""
User management endpoints for CRUD operations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.exceptions import NotFoundError, ConflictError, ValidationError
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithBlogs
from app.services.user_service import UserService
from app.services.auth_service import get_current_active_user_dependency, User

logger = logging.getLogger(__name__)

router = APIRouter(tags=["users"])


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user account.
    
    Args:
        user_data: User creation data
        db: Database session
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If user creation fails
    """
    try:
        user_service = UserService(db)
        user = user_service.create_user(user_data)
        
        logger.info(f"User created successfully: {user.email}")
        return user
        
    except ConflictError as e:
        logger.warning(f"User creation conflict: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.detail
        )
    except ValidationError as e:
        logger.warning(f"User creation validation error: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"User creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user information
    """
    return UserResponse.model_validate(current_user)


@router.get("/me/blogs", response_model=UserWithBlogs, status_code=status.HTTP_200_OK)
async def get_current_user_with_blogs(
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Get current user with their blog posts.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Current user with blogs
    """
    try:
        user_service = UserService(db)
        return user_service.get_user_with_blogs(current_user.id)
        
    except NotFoundError as e:
        logger.warning(f"User blogs not found: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error fetching user blogs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user blogs"
        )


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Get user by ID (only accessible by the user themselves).
    
    Args:
        user_id: User ID to fetch
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found or access denied
    """
    try:
        # Check if user is accessing their own profile
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own profile"
            )
        
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        return user
        
    except NotFoundError as e:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )


@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Update current user information.
    
    Args:
        user_data: User update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If update fails
    """
    try:
        user_service = UserService(db)
        user = user_service.update_user(current_user.id, user_data)
        
        logger.info(f"User {current_user.id} updated successfully")
        return user
        
    except ConflictError as e:
        logger.warning(f"User update conflict: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.detail
        )
    except ValidationError as e:
        logger.warning(f"User update validation error: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"User update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_active_user_dependency),
    db: Session = Depends(get_db)
):
    """
    Delete current user account.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If deletion fails
    """
    try:
        user_service = UserService(db)
        user_service.delete_user(current_user.id)
        
        logger.info(f"User {current_user.id} deleted successfully")
        
    except NotFoundError as e:
        logger.warning(f"User not found for deletion: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"User deletion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Get all users with pagination (admin only).
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of users
        
    Raises:
        HTTPException: If access denied or operation fails
    """
    try:
        # TODO: Add admin role check
        # if not current_user.is_admin:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Admin access required"
        #     )
        
        user_service = UserService(db)
        users = user_service.get_all_users(skip=skip, limit=limit)
        
        return users
        
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )
