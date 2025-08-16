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
    OAuth2 form-based login endpoint for OAuth2 flows and future integrations.
    
    Args:
        form_data: OAuth2 form data (username=email, password=password)
        db: Database session
        
    Returns:
        Token response for OAuth2 flows
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Convert OAuth2 form data to our login format
        login_data = LoginRequest(
            email=form_data.username,  # OAuth2 uses 'username' field
            password=form_data.password
        )
        
        auth_service = AuthService(db)
        response = auth_service.login_user(login_data)
        
        logger.info(f"Successful OAuth2 form login for user: {form_data.username}")
        return Token(
            access_token=response.access_token,
            token_type=response.token_type,
            expires_in=response.expires_in
        )
        
    except AuthenticationError as e:
        logger.warning(f"OAuth2 form authentication failed for {form_data.username}: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    except Exception as e:
        logger.error(f"OAuth2 form login error for {form_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during OAuth2 login"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Logout endpoint for authenticated users.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Logout confirmation message
    """
    try:
        logger.info(f"User {current_user.email} logged out successfully")
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )


@router.get("/google/login")
async def google_login():
    """
    Initiate Google OAuth2 login flow.
    
    Returns:
        Google OAuth2 authorization URL
    """
    try:
        # TODO: Implement Google OAuth2 flow
        # This would redirect to Google's OAuth2 authorization page
        logger.info("Google OAuth2 login initiated (not yet implemented)")
        return {
            "message": "Google OAuth2 login not yet implemented",
            "status": "development"
        }
        
    except Exception as e:
        logger.error(f"Google login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during Google login"
        )


@router.get("/google/callback")
async def google_callback(code: str):
    """
    Handle Google OAuth2 callback.
    
    Args:
        code: Authorization code from Google
        
    Returns:
        Login response with access token
    """
    try:
        # TODO: Implement Google OAuth2 callback
        # This would:
        # 1. Exchange authorization code for access token
        # 2. Get user info from Google
        # 3. Create or update user in database
        # 4. Return JWT token
        
        logger.info(f"Google OAuth2 callback received (not yet implemented): {code}")
        return {
            "message": "Google OAuth2 callback not yet implemented",
            "status": "development"
        }
        
    except Exception as e:
        logger.error(f"Google callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during Google callback"
        )


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
