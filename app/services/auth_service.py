"""
Authentication service for user authentication and token management.
Handles login, token creation, and user verification.
"""
from datetime import timedelta
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security import security_manager
from app.core.config import settings
from app.core.exceptions import AuthenticationError, NotFoundError
from app.models.user import User
from app.schemas.auth import Token, LoginRequest, LoginResponse
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

# HTTP Bearer scheme for JWT token authentication
http_bearer_scheme = HTTPBearer()

# OAuth2 scheme for password-based authentication (useful for OAuth2 flows)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login-form")


class AuthService:
    """Service class for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def authenticate_user(self, login_data: LoginRequest) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            return self.user_service.authenticate_user(
                email=login_data.email,
                password=login_data.password
            )
        except Exception as e:
            logger.error(f"Authentication error for {login_data.email}: {e}")
            return None
    
    def create_access_token(self, user: User) -> Token:
        """Create access token for authenticated user."""
        try:
            # Create token data
            token_data = {"sub": user.email, "user_id": user.id}
            
            # Create access token
            access_token = security_manager.create_access_token(
                data=token_data,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            
        except Exception as e:
            logger.error(f"Token creation error for user {user.id}: {e}")
            raise AuthenticationError("Failed to create access token")
    
    def login_user(self, login_data: LoginRequest) -> LoginResponse:
        """Authenticate user and return login response."""
        try:
            # Authenticate user
            user = self.authenticate_user(login_data)
            if not user:
                raise AuthenticationError("Invalid email or password")
            
            # Create access token
            token = self.create_access_token(user)
            
            # Create user response
            user_response = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active
            }
            
            logger.info(f"User {user.email} logged in successfully")
            
            return LoginResponse(
                access_token=token.access_token,
                token_type=token.token_type,
                expires_in=token.expires_in,
                user=user_response
            )
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise
    
    def get_current_user(
        self, 
        credentials = Depends(http_bearer_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        """Get current authenticated user from JWT Bearer token."""
        try:
            # Extract token from HTTPBearer credentials
            token = credentials.credentials
            
            # Verify token
            email = security_manager.verify_token(token)
            if not email:
                raise AuthenticationError("Invalid or expired token")
            
            # Get user from database
            user = self.user_service.get_user_by_email(email)
            if not user:
                raise AuthenticationError("User not found")
            
            if not user.is_active:
                raise AuthenticationError("User account is deactivated")
            
            return user
            
        except Exception as e:
            logger.error(f"Current user retrieval error: {e}")
            raise
    
    def get_current_user_from_oauth2(
        self, 
        token: str,
        db: Session
    ) -> User:
        """Get current authenticated user from OAuth2 token."""
        try:
            # Validate OAuth2 token with provider
            user = self.validate_oauth2_token(token)
            if not user:
                raise AuthenticationError("Invalid OAuth2 token")
            
            if not user.is_active:
                raise AuthenticationError("User account is deactivated")
            
            return user
            
        except Exception as e:
            logger.error(f"OAuth2 current user retrieval error: {e}")
            raise
    
    def get_current_active_user(
        self, 
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current active user."""
        if not current_user.is_active:
            raise AuthenticationError("User account is deactivated")
        return current_user
    
    def verify_user_permissions(
        self, 
        user: User, 
        resource_owner_id: int
    ) -> bool:
        """Verify if user has permission to access/modify a resource."""
        # Admin users can access all resources
        if hasattr(user, 'is_admin') and user.is_admin:
            return True
        
        # Users can only access their own resources
        return user.id == resource_owner_id
    
    def validate_oauth2_token(
        self, 
        oauth2_token: str
    ) -> Optional[User]:
        """
        Validate OAuth2 token (for future Google login integration).
        
        Args:
            oauth2_token: OAuth2 access token from provider
            
        Returns:
            User object if token is valid, None otherwise
        """
        try:
            # TODO: Implement OAuth2 provider token validation
            # This is where you would:
            # 1. Validate token with Google OAuth2 API
            # 2. Extract user information from Google
            # 3. Find or create user in your database
            # 4. Return user object
            
            logger.info("OAuth2 token validation called (not yet implemented)")
            return None
            
        except Exception as e:
            logger.error(f"OAuth2 token validation error: {e}")
            return None


# Dependency functions for use in routers
async def get_current_user_dependency(
    credentials = Depends(http_bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency function to get current user from JWT Bearer token."""
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials, db)


async def get_current_user_oauth2_dependency(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency function to get current user from OAuth2 token."""
    auth_service = AuthService(db)
    return auth_service.get_current_user_from_oauth2(token, db)


async def get_current_active_user_dependency(
    current_user: User = Depends(get_current_user_dependency)
) -> User:
    """Dependency function to get current active user."""
    return current_user
