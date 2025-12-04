"""
API Key Authentication Middleware

Middleware for FastAPI to validate API keys in request headers.
Supports both Bearer token and X-API-Key header formats.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Optional
import logging

from api_keys import get_api_key_manager

logger = logging.getLogger(__name__)


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate API keys in requests."""
    
    # Paths that don't require authentication
    SKIP_AUTH_PATHS = {
        "/health",
        "/status",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api-keys/validate",  # Allow validation without auth
    }
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        """Process request and validate API key if needed."""
        
        # Skip authentication for certain paths
        if self._should_skip_auth(request.url.path):
            return await call_next(request)
        
        # Try to get API key from headers
        api_key = self._extract_api_key(request)
        
        # If no API key found, allow request to proceed
        # (can be protected by JWT or other means)
        if not api_key:
            return await call_next(request)
        
        # Validate API key
        manager = get_api_key_manager()
        is_valid, key_info, error_message = manager.validate_key(api_key)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid API key: {error_message}"
            )
        
        # Attach key info to request state for downstream use
        request.state.api_key_id = key_info.key_id
        request.state.api_key_owner = key_info.owner
        request.state.api_key_scopes = key_info.scopes
        request.state.authenticated_via = "api_key"
        
        logger.info(f"API Key validated: {key_info.key_id} (owner: {key_info.owner})")
        
        # Continue to next middleware/endpoint
        response = await call_next(request)
        
        return response
    
    @staticmethod
    def _extract_api_key(request: Request) -> Optional[str]:
        """Extract API key from request headers.
        
        Supports:
        - X-API-Key header
        - Authorization: Bearer <key>
        """
        # Try X-API-Key header first
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return api_key
        
        # Try Authorization header with Bearer scheme
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        
        return None
    
    @staticmethod
    def _should_skip_auth(path: str) -> bool:
        """Check if path should skip authentication."""
        # Check exact matches
        if path in APIKeyAuthMiddleware.SKIP_AUTH_PATHS:
            return True
        
        # Check prefixes
        for skip_path in APIKeyAuthMiddleware.SKIP_AUTH_PATHS:
            if path.startswith(skip_path):
                return True
        
        return False


async def get_api_key_from_request(request: Request) -> Optional[str]:
    """Dependency to get API key ID from authenticated request."""
    return getattr(request.state, "api_key_id", None)


async def get_api_key_owner(request: Request) -> Optional[str]:
    """Dependency to get API key owner from authenticated request."""
    return getattr(request.state, "api_key_owner", None)


async def get_api_key_scopes(request: Request) -> list:
    """Dependency to get API key scopes from authenticated request."""
    return getattr(request.state, "api_key_scopes", [])


async def require_api_key_scope(required_scope: str):
    """Dependency to require specific API key scope."""
    async def _check_scope(request: Request):
        scopes = getattr(request.state, "api_key_scopes", [])
        if required_scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API key does not have required scope: {required_scope}"
            )
        return True
    
    return _check_scope


async def require_api_authentication(request: Request) -> str:
    """Dependency to require API key authentication."""
    api_key_id = getattr(request.state, "api_key_id", None)
    if not api_key_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key authentication required"
        )
    return api_key_id
