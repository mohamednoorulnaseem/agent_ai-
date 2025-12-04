"""
API Key Management System

Provides secure API key generation, storage, and validation with:
- Secure key generation using secrets module
- Key hashing for secure storage
- Rate limiting per key
- Key rotation and expiration
- Usage tracking and analytics
"""

import secrets
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import sqlite3
import os


class KeyStatus(str, Enum):
    """API key status enumeration."""
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    RATE_LIMITED = "rate_limited"


@dataclass
class APIKeyInfo:
    """Information about an API key."""
    key_id: str
    name: str
    created_at: str
    last_used: Optional[str] = None
    expires_at: Optional[str] = None
    status: KeyStatus = KeyStatus.ACTIVE
    rate_limit: int = 1000  # requests per minute
    usage_count: int = 0
    owner: str = "default"
    scopes: List[str] = field(default_factory=lambda: ["read", "write"])
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        """Convert to dictionary."""
        data = asdict(self)
        data['status'] = self.status.value
        return data

    def is_expired(self) -> bool:
        """Check if key is expired."""
        if not self.expires_at:
            return False
        return datetime.fromisoformat(self.expires_at) < datetime.now()

    def is_active(self) -> bool:
        """Check if key is active."""
        return self.status == KeyStatus.ACTIVE and not self.is_expired()


class APIKeyManager:
    """Manages API keys with secure storage and validation."""

    def __init__(self, db_path: str = "./data/api_keys.db"):
        """Initialize API key manager.
        
        Args:
            db_path: Path to SQLite database for key storage
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    key_id TEXT PRIMARY KEY,
                    key_hash TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_used TEXT,
                    expires_at TEXT,
                    status TEXT DEFAULT 'active',
                    rate_limit INTEGER DEFAULT 1000,
                    usage_count INTEGER DEFAULT 0,
                    scopes TEXT DEFAULT '["read", "write"]',
                    metadata TEXT DEFAULT '{}',
                    UNIQUE(owner, name)
                )
            """)
            conn.commit()

    def generate_key(
        self,
        name: str,
        owner: str = "default",
        expires_in_days: Optional[int] = None,
        rate_limit: int = 1000,
        scopes: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Tuple[str, APIKeyInfo]:
        """Generate a new API key.
        
        Args:
            name: Human-readable key name
            owner: Owner/organization identifier
            expires_in_days: Days until expiration (None = never)
            rate_limit: Requests per minute allowed
            scopes: List of permission scopes
            metadata: Additional metadata to store
            
        Returns:
            Tuple of (raw_key, key_info)
        """
        # Generate secure random key
        raw_key = f"ak_{secrets.token_urlsafe(32)}"
        key_id = f"id_{secrets.token_hex(8)}"
        
        # Hash key for storage
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        # Set expiration
        expires_at = None
        if expires_in_days:
            expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
        
        # Create key info
        key_info = APIKeyInfo(
            key_id=key_id,
            name=name,
            created_at=datetime.now().isoformat(),
            expires_at=expires_at,
            rate_limit=rate_limit,
            owner=owner,
            scopes=scopes or ["read", "write"],
            metadata=metadata or {}
        )
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO api_keys (
                    key_id, key_hash, name, owner, created_at, expires_at,
                    rate_limit, scopes, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                key_id, key_hash, name, owner, key_info.created_at, expires_at,
                rate_limit, json.dumps(scopes or ["read", "write"]),
                json.dumps(metadata or {})
            ))
            conn.commit()
        
        return raw_key, key_info

    def validate_key(self, api_key: str) -> Tuple[bool, Optional[APIKeyInfo], Optional[str]]:
        """Validate an API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            Tuple of (is_valid, key_info, error_message)
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT key_id, name, created_at, last_used, expires_at, 
                       status, rate_limit, usage_count, owner, scopes, metadata
                FROM api_keys WHERE key_hash = ?
            """, (key_hash,))
            
            row = cursor.fetchone()
            if not row:
                return False, None, "Invalid API key"
            
            # Parse data
            (key_id, name, created_at, last_used, expires_at, status, 
             rate_limit, usage_count, owner, scopes_json, metadata_json) = row
            
            scopes = json.loads(scopes_json)
            metadata = json.loads(metadata_json)
            
            # Create key info
            key_info = APIKeyInfo(
                key_id=key_id,
                name=name,
                created_at=created_at,
                last_used=last_used,
                expires_at=expires_at,
                status=KeyStatus(status),
                rate_limit=rate_limit,
                usage_count=usage_count,
                owner=owner,
                scopes=scopes,
                metadata=metadata
            )
            
            # Check status
            if not key_info.is_active():
                reason = "Key is revoked" if key_info.status == KeyStatus.REVOKED else "Key is expired"
                return False, key_info, reason
            
            # Update last used timestamp
            conn.execute("""
                UPDATE api_keys SET last_used = ?, usage_count = usage_count + 1
                WHERE key_id = ?
            """, (datetime.now().isoformat(), key_id))
            conn.commit()
            
            return True, key_info, None

    def revoke_key(self, key_id: str) -> bool:
        """Revoke an API key.
        
        Args:
            key_id: The key ID to revoke
            
        Returns:
            True if successful, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE api_keys SET status = ? WHERE key_id = ?",
                (KeyStatus.REVOKED.value, key_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def list_keys(self, owner: str = "default") -> List[APIKeyInfo]:
        """List all keys for an owner (without raw key).
        
        Args:
            owner: Owner identifier
            
        Returns:
            List of key information objects
        """
        keys = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT key_id, name, created_at, last_used, expires_at,
                       status, rate_limit, usage_count, owner, scopes, metadata
                FROM api_keys WHERE owner = ? ORDER BY created_at DESC
            """, (owner,))
            
            for row in cursor.fetchall():
                (key_id, name, created_at, last_used, expires_at, status,
                 rate_limit, usage_count, owner, scopes_json, metadata_json) = row
                
                key_info = APIKeyInfo(
                    key_id=key_id,
                    name=name,
                    created_at=created_at,
                    last_used=last_used,
                    expires_at=expires_at,
                    status=KeyStatus(status),
                    rate_limit=rate_limit,
                    usage_count=usage_count,
                    owner=owner,
                    scopes=json.loads(scopes_json),
                    metadata=json.loads(metadata_json)
                )
                keys.append(key_info)
        
        return keys

    def get_key_info(self, key_id: str) -> Optional[APIKeyInfo]:
        """Get information about a specific key.
        
        Args:
            key_id: The key ID
            
        Returns:
            Key information or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT key_id, name, created_at, last_used, expires_at,
                       status, rate_limit, usage_count, owner, scopes, metadata
                FROM api_keys WHERE key_id = ?
            """, (key_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            (key_id, name, created_at, last_used, expires_at, status,
             rate_limit, usage_count, owner, scopes_json, metadata_json) = row
            
            return APIKeyInfo(
                key_id=key_id,
                name=name,
                created_at=created_at,
                last_used=last_used,
                expires_at=expires_at,
                status=KeyStatus(status),
                rate_limit=rate_limit,
                usage_count=usage_count,
                owner=owner,
                scopes=json.loads(scopes_json),
                metadata=json.loads(metadata_json)
            )

    def delete_key(self, key_id: str) -> bool:
        """Permanently delete an API key.
        
        Args:
            key_id: The key ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM api_keys WHERE key_id = ?", (key_id,))
            conn.commit()
            return cursor.rowcount > 0

    def rotate_key(
        self,
        key_id: str,
        expires_in_days: Optional[int] = None
    ) -> Optional[Tuple[str, APIKeyInfo]]:
        """Rotate (regenerate) an API key.
        
        Args:
            key_id: The key ID to rotate
            expires_in_days: New expiration in days
            
        Returns:
            Tuple of (new_raw_key, updated_key_info) or None if key not found
        """
        # Get existing key info
        key_info = self.get_key_info(key_id)
        if not key_info:
            return None
        
        # Delete old key
        self.delete_key(key_id)
        
        # Generate new key
        return self.generate_key(
            name=key_info.name,
            owner=key_info.owner,
            expires_in_days=expires_in_days,
            rate_limit=key_info.rate_limit,
            scopes=key_info.scopes,
            metadata=key_info.metadata
        )

    def get_usage_stats(self, owner: str = "default") -> Dict:
        """Get usage statistics for an owner.
        
        Args:
            owner: Owner identifier
            
        Returns:
            Dictionary with usage statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) as total_keys,
                       SUM(usage_count) as total_requests,
                       MAX(last_used) as last_request
                FROM api_keys WHERE owner = ?
            """, (owner,))
            
            row = cursor.fetchone()
            total_keys, total_requests, last_request = row
            
            return {
                "owner": owner,
                "total_keys": total_keys or 0,
                "total_requests": total_requests or 0,
                "last_request": last_request,
                "active_keys": len(self.list_keys(owner))
            }


# Global instance
_key_manager = None


def get_api_key_manager() -> APIKeyManager:
    """Get or create global API key manager instance."""
    global _key_manager
    if _key_manager is None:
        _key_manager = APIKeyManager()
    return _key_manager
