"""
API Key Management Routes

Provides REST endpoints for API key management:
- Generate new keys
- List keys
- Revoke/rotate keys
- View usage statistics
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from api_keys import APIKeyManager, KeyStatus, APIKeyInfo, get_api_key_manager


# Router
router = APIRouter(prefix="/api-keys", tags=["api-keys"])


# Pydantic Models
class GenerateKeyRequest(BaseModel):
    """Request to generate a new API key."""
    name: str
    expires_in_days: Optional[int] = None
    rate_limit: int = 1000
    scopes: List[str] = ["read", "write"]
    metadata: Optional[dict] = None


class GenerateKeyResponse(BaseModel):
    """Response with newly generated API key."""
    key: str  # Raw key - shown only once
    key_id: str
    name: str
    created_at: str
    expires_at: Optional[str]
    scopes: List[str]
    message: str = "Save this key securely. It will not be shown again."


class KeyInfoResponse(BaseModel):
    """Response with API key information."""
    key_id: str
    name: str
    created_at: str
    last_used: Optional[str]
    expires_at: Optional[str]
    status: str
    rate_limit: int
    usage_count: int
    owner: str
    scopes: List[str]
    is_active: bool


class KeyListResponse(BaseModel):
    """Response with list of API keys."""
    keys: List[KeyInfoResponse]
    total: int


class RevokeKeyResponse(BaseModel):
    """Response from revoking a key."""
    success: bool
    key_id: str
    message: str


class RotateKeyResponse(BaseModel):
    """Response from rotating a key."""
    key: str  # New raw key
    key_id: str
    message: str = "Old key has been revoked. Save new key securely."


class UsageStatsResponse(BaseModel):
    """Response with usage statistics."""
    total_keys: int
    total_requests: int
    last_request: Optional[str]
    active_keys: int


class ValidateKeyResponse(BaseModel):
    """Response from key validation."""
    valid: bool
    key_id: Optional[str]
    name: Optional[str]
    scopes: Optional[List[str]]
    rate_limit: Optional[int]
    usage_count: Optional[int]
    message: Optional[str]


# Dependencies
def get_key_manager() -> APIKeyManager:
    """Get API key manager instance."""
    return get_api_key_manager()


# Routes

@router.post("/generate", response_model=GenerateKeyResponse)
async def generate_key(
    request: GenerateKeyRequest,
    manager: APIKeyManager = Depends(get_key_manager)
) -> GenerateKeyResponse:
    """
    Generate a new API key.
    
    **Note**: The raw key is shown only once. Save it securely.
    """
    raw_key, key_info = manager.generate_key(
        name=request.name,
        expires_in_days=request.expires_in_days,
        rate_limit=request.rate_limit,
        scopes=request.scopes,
        metadata=request.metadata
    )
    
    return GenerateKeyResponse(
        key=raw_key,
        key_id=key_info.key_id,
        name=key_info.name,
        created_at=key_info.created_at,
        expires_at=key_info.expires_at,
        scopes=key_info.scopes
    )


@router.get("/list", response_model=KeyListResponse)
async def list_keys(
    owner: str = "default",
    manager: APIKeyManager = Depends(get_key_manager)
) -> KeyListResponse:
    """
    List all API keys for the authenticated owner.
    
    Raw key values are not returned for security.
    """
    keys = manager.list_keys(owner)
    
    key_responses = [
        KeyInfoResponse(
            key_id=key.key_id,
            name=key.name,
            created_at=key.created_at,
            last_used=key.last_used,
            expires_at=key.expires_at,
            status=key.status.value,
            rate_limit=key.rate_limit,
            usage_count=key.usage_count,
            owner=key.owner,
            scopes=key.scopes,
            is_active=key.is_active()
        )
        for key in keys
    ]
    
    return KeyListResponse(keys=key_responses, total=len(key_responses))


@router.get("/{key_id}", response_model=KeyInfoResponse)
async def get_key_info(
    key_id: str,
    manager: APIKeyManager = Depends(get_key_manager)
) -> KeyInfoResponse:
    """
    Get information about a specific API key.
    """
    key_info = manager.get_key_info(key_id)
    
    if not key_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key '{key_id}' not found"
        )
    
    return KeyInfoResponse(
        key_id=key_info.key_id,
        name=key_info.name,
        created_at=key_info.created_at,
        last_used=key_info.last_used,
        expires_at=key_info.expires_at,
        status=key_info.status.value,
        rate_limit=key_info.rate_limit,
        usage_count=key_info.usage_count,
        owner=key_info.owner,
        scopes=key_info.scopes,
        is_active=key_info.is_active()
    )


@router.post("/{key_id}/revoke", response_model=RevokeKeyResponse)
async def revoke_key(
    key_id: str,
    manager: APIKeyManager = Depends(get_key_manager)
) -> RevokeKeyResponse:
    """
    Revoke an API key (can be reactivated later).
    """
    success = manager.revoke_key(key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key '{key_id}' not found"
        )
    
    return RevokeKeyResponse(
        success=True,
        key_id=key_id,
        message=f"API key '{key_id}' has been revoked"
    )


@router.post("/{key_id}/rotate", response_model=RotateKeyResponse)
async def rotate_key(
    key_id: str,
    expires_in_days: Optional[int] = None,
    manager: APIKeyManager = Depends(get_key_manager)
) -> RotateKeyResponse:
    """
    Rotate (regenerate) an API key.
    
    The old key will be revoked and a new key generated.
    """
    result = manager.rotate_key(key_id, expires_in_days)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key '{key_id}' not found"
        )
    
    new_raw_key, new_key_info = result
    
    return RotateKeyResponse(
        key=new_raw_key,
        key_id=new_key_info.key_id
    )


@router.delete("/{key_id}", response_model=RevokeKeyResponse)
async def delete_key(
    key_id: str,
    manager: APIKeyManager = Depends(get_key_manager)
) -> RevokeKeyResponse:
    """
    Permanently delete an API key (cannot be recovered).
    """
    success = manager.delete_key(key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key '{key_id}' not found"
        )
    
    return RevokeKeyResponse(
        success=True,
        key_id=key_id,
        message=f"API key '{key_id}' has been permanently deleted"
    )


@router.get("/stats/usage", response_model=UsageStatsResponse)
async def get_usage_stats(
    owner: str = "default",
    manager: APIKeyManager = Depends(get_key_manager)
) -> UsageStatsResponse:
    """
    Get usage statistics for API keys.
    """
    stats = manager.get_usage_stats(owner)
    
    return UsageStatsResponse(
        total_keys=stats["total_keys"],
        total_requests=stats["total_requests"],
        last_request=stats["last_request"],
        active_keys=stats["active_keys"]
    )


@router.post("/validate", response_model=ValidateKeyResponse)
async def validate_key(
    api_key: str,
    manager: APIKeyManager = Depends(get_key_manager)
) -> ValidateKeyResponse:
    """
    Validate an API key without making a request.
    
    Useful for testing if a key is still valid.
    """
    is_valid, key_info, error_message = manager.validate_key(api_key)
    
    if not is_valid:
        return ValidateKeyResponse(
            valid=False,
            key_id=None,
            name=None,
            scopes=None,
            rate_limit=None,
            usage_count=None,
            message=error_message
        )
    
    return ValidateKeyResponse(
        valid=True,
        key_id=key_info.key_id,
        name=key_info.name,
        scopes=key_info.scopes,
        rate_limit=key_info.rate_limit,
        usage_count=key_info.usage_count,
        message="API key is valid"
    )
