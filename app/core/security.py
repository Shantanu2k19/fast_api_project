"""
Security utilities for authentication and authorization.
Handles password hashing, JWT tokens, and security functions.
"""
from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from passlib.context import CryptContext
from jose import JWTError, jwt
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityManager:
    """Manages security operations including password hashing and JWT tokens."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            return pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise ValueError("Password hashing failed")
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    @staticmethod
    def create_access_token(
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(
                    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
            
            to_encode.update({"exp": expire})
            
            encoded_jwt = jwt.encode(
                to_encode, 
                settings.SECRET_KEY.get_secret_value(), 
                algorithm=settings.ALGORITHM
            )
            
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Token creation failed: {e}")
            raise ValueError("Failed to create access token")
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY.get_secret_value(), 
                algorithms=[settings.ALGORITHM]
            )
            
            email: str = payload.get("sub")
            if email is None:
                return None
                
            return email
            
        except JWTError as e:
            logger.warning(f"JWT token verification failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None


# Global security manager instance
security_manager = SecurityManager()
