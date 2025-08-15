"""
Authentication API endpoints.
Handles user login, logout, and current user information.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.schemas.auth import LoginRequest, LoginResponse, Token
from app.services.auth_service import AuthService, get_current_user_dependency
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint for JSON-based authentication.
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        Login response with access token and user info
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        auth_service = AuthService(db)
        response = auth_service.login_user(login_data)
        
        logger.info(f"Successful login for user: {login_data.email}")
        return response
        
    except AuthenticationError as e:
        logger.warning(f"Authentication failed for {login_data.email}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except Exception as e:
        logger.error(f"Login error for {login_data.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/login-form", response_model=Token, status_code=status.HTTP_200_OK)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint for OAuth2 form-based authentication.
    
    Args:
        form_data: OAuth2 form data
        db: Database session
        
    Returns:
        Token response
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        login_data = LoginRequest(
            email=form_data.username,
            password=form_data.password
        )
        
        auth_service = AuthService(db)
        response = auth_service.login_user(login_data)
        
        logger.info(f"Successful form login for user: {form_data.username}")
        return Token(
            access_token=response.access_token,
            token_type=response.token_type,
            expires_in=response.expires_in
        )
        
    except AuthenticationError as e:
        logger.warning(f"Form authentication failed for {form_data.username}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    except Exception as e:
        logger.error(f"Form login error for {form_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout endpoint (client-side token removal).
    
    Returns:
        Success message
    """
    # Note: JWT tokens are stateless, so logout is handled client-side
    # by removing the token from storage
    return {"message": "Successfully logged out"}


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }
