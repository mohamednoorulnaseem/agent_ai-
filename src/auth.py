"""
Authentication and authorization for the Agent API.
Supports JWT tokens and API keys.
"""

from fastapi import Depends, HTTPException, status, Header
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import secrets


# Configuration
SECRET_KEY: str = secrets.token_urlsafe(32)  # In production, use environment variable
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class TokenManager:
    """Manages JWT tokens."""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode: Dict[str, Any] = data.copy()
        
        if expires_delta:
            expire: datetime = datetime.utcnow() + expires_delta
        else:
            expire: datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload: Dict[str, Any] = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


class APIKeyManager:
    """Manages API keys for programmatic access."""
    
    # In production, store in database
    _api_keys: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def generate_api_key(cls, name: str) -> str:
        """Generate a new API key."""
        key: str = f"sk-{secrets.token_urlsafe(32)}"
        cls._api_keys[key] = {
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None,
            "active": True
        }
        return key
    
    @classmethod
    def validate_api_key(cls, key: str) -> bool:
        """Validate an API key."""
        if key not in cls._api_keys:
            return False
        
        key_info = cls._api_keys[key]
        if not key_info.get("active", False):
            return False
        
        # Update last used
        cls._api_keys[key]["last_used"] = datetime.utcnow().isoformat()
        return True
    
    @classmethod
    def revoke_api_key(cls, key: str) -> bool:
        """Revoke an API key."""
        if key in cls._api_keys:
            cls._api_keys[key]["active"] = False
            return True
        return False
    
    @classmethod
    def list_api_keys(cls) -> list:
        """List all API keys (without exposing the key itself)."""
        result = []
        for key, info in cls._api_keys.items():
            result.append({
                "key_preview": f"{key[:10]}...{key[-4:]}",
                "name": info["name"],
                "created_at": info["created_at"],
                "last_used": info["last_used"],
                "active": info["active"]
            })
        return result


class User:
    """Represents an authenticated user."""
    
    def __init__(self, user_id: str, username: str, email: str, roles: list = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.roles = roles or ["user"]
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.has_role("admin")


async def get_token_from_header(authorization: str = Header(None)) -> str:
    """Extract bearer token from Authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    return authorization[7:]  # Remove "Bearer " prefix


async def get_current_user(token: str = Depends(get_token_from_header)) -> User:
    """Get current authenticated user from token."""
    try:
        payload = TokenManager.verify_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return User(
            user_id=user_id,
            username=payload.get("username", "unknown"),
            email=payload.get("email", "unknown@example.com"),
            roles=payload.get("roles", ["user"])
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Get current user if they are an admin."""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# Demo credentials for development
DEMO_CREDENTIALS = {
    "demo": {
        "password": "demo123",
        "user_id": "user_1",
        "username": "Demo User",
        "email": "demo@example.com",
        "roles": ["user"]
    },
    "admin": {
        "password": "admin123",
        "user_id": "admin_1",
        "username": "Admin User",
        "email": "admin@example.com",
        "roles": ["admin", "user"]
    }
}


def verify_credentials(username: str, password: str) -> Optional[Dict]:
    """Verify username and password."""
    if username in DEMO_CREDENTIALS:
        creds = DEMO_CREDENTIALS[username]
        if creds["password"] == password:
            return {
                "sub": creds["user_id"],
                "username": creds["username"],
                "email": creds["email"],
                "roles": creds["roles"]
            }
    return None
