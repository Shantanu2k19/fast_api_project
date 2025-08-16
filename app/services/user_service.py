"""
User service for business logic operations.
Handles user creation, authentication, and management.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserWithBlogs
from app.core.security import security_manager
from app.core.exceptions import (
    NotFoundError, 
    ConflictError, 
    ValidationError, 
    DatabaseError
)

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise ConflictError("User with this email already exists")
            
            # Hash password and create user
            hashed_password = security_manager.hash_password(user_data.password)
            
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=hashed_password,
                is_verified=True  # For simplicity, set as verified
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            logger.info(f"User created successfully: {db_user.email}")
            return UserResponse.model_validate(db_user)
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error creating user: {e}")
            raise ConflictError("User creation failed due to database constraints")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {e}")
            raise DatabaseError("Failed to create user")
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user by ID."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("User")
            
            return UserResponse.model_validate(user)
            
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (internal use)."""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None
    
    def get_user_with_blogs(self, user_id: int) -> UserWithBlogs:
        """Get user with their blogs."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("User")
            
            return UserWithBlogs.model_validate(user)
            
        except Exception as e:
            logger.error(f"Error fetching user with blogs {user_id}: {e}")
            raise
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user information."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("User")
            
            # Update fields if provided
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User {user_id} updated successfully")
            return UserResponse.model_validate(user)
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error updating user {user_id}: {e}")
            raise ConflictError("User update failed due to database constraints")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise DatabaseError("Failed to update user")
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError("User")
            
            self.db.delete(user)
            self.db.commit()
            
            logger.info(f"User {user_id} deleted successfully")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {e}")
            raise DatabaseError("Failed to delete user")
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = self.get_user_by_email(email)
            if not user:
                return None
            
            if not security_manager.verify_password(password, user.password_hash):
                return None
            
            if not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination."""
        try:
            users = self.db.query(User).offset(skip).limit(limit).all()
            return [UserResponse.model_validate(user) for user in users]
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            raise DatabaseError("Failed to fetch users")
