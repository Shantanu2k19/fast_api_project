"""
Custom exceptions and error handling for the application.
Provides consistent error responses and exception handling.
"""
from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class AppException(HTTPException):
    """Base application exception."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthenticationError(AppException):
    """Authentication related errors."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(AppException):
    """Authorization related errors."""
    
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class NotFoundError(AppException):
    """Resource not found errors."""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )


class ValidationError(AppException):
    """Data validation errors."""
    
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class ConflictError(AppException):
    """Resource conflict errors."""
    
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class DatabaseError(AppException):
    """Database operation errors."""
    
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


def handle_exception(exc: Exception) -> Dict[str, Any]:
    """Handle exceptions and return consistent error response."""
    if isinstance(exc, AppException):
        return {
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    
    # Handle unexpected exceptions
    return {
        "error": True,
        "message": "An unexpected error occurred",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }
