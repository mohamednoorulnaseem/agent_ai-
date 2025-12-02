"""
Caching system for API responses and LLM outputs.

Provides multi-level caching with TTL, size limits, and cache warming.
Supports both in-memory and persistent caching.
"""

import hashlib
import json
import time
import pickle
from typing import Any, Dict, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading


@dataclass
class CacheEntry:
    """Individual cache entry with metadata."""
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    hits: int = 0
    size_bytes: int = 0

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def record_hit(self) -> None:
        """Record a cache hit."""
        self.hits += 1


class MemoryCache:
    """In-memory cache with TTL and size limits."""

    def __init__(self, max_size_mb: int = 100, default_ttl_seconds: int = 3600):
        """
        Initialize memory cache.

        Args:
            max_size_mb: Maximum cache size in MB
            default_ttl_seconds: Default TTL for entries (None = never expires)
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl_seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.current_size = 0
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def _calculate_size(self, value: Any) -> int:
        """Calculate size of value in bytes."""
        try:
            return len(pickle.dumps(value))
        except Exception:
            return 1000  # Fallback estimate

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            entry = self.cache.get(key)

            if entry is None:
                self.misses += 1
                return None

            if entry.is_expired():
                self._evict(key)
                self.misses += 1
                return None

            entry.record_hit()
            self.hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in cache."""
        with self.lock:
            # Remove old entry if exists
            if key in self.cache:
                self._evict(key)

            # Calculate size
            size = self._calculate_size(value)

            # Check if value fits
            if size > self.max_size_bytes:
                return  # Value too large to cache

            # Evict oldest entries if needed
            while self.current_size + size > self.max_size_bytes and self.cache:
                oldest_key = min(
                    self.cache.keys(),
                    key=lambda k: self.cache[k].created_at
                )
                self._evict(oldest_key)

            # Create entry
            expires_at = None
            if ttl_seconds is not None:
                expires_at = time.time() + ttl_seconds
            elif self.default_ttl is not None:
                expires_at = time.time() + self.default_ttl

            entry = CacheEntry(
                key=key,
                value=value,
                expires_at=expires_at,
                size_bytes=size
            )

            self.cache[key] = entry
            self.current_size += size

    def delete(self, key: str) -> None:
        """Delete entry from cache."""
        with self.lock:
            self._evict(key)

    def _evict(self, key: str) -> None:
        """Evict entry from cache (must hold lock)."""
        if key in self.cache:
            entry = self.cache[key]
            self.current_size -= entry.size_bytes
            del self.cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.current_size = 0

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = self.hits / total_requests if total_requests > 0 else 0

            return {
                "entries": len(self.cache),
                "size_bytes": self.current_size,
                "size_mb": self.current_size / (1024 * 1024),
                "max_size_mb": self.max_size_bytes / (1024 * 1024),
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate,
                "total_requests": total_requests,
            }


class PersistentCache:
    """Persistent cache backed by file system."""

    def __init__(self, cache_dir: str = ".cache"):
        """
        Initialize persistent cache.

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.cache"

    def get(self, key: str) -> Optional[Any]:
        """Get value from persistent cache."""
        path = self._get_cache_path(key)

        if not path.exists():
            return None

        try:
            with open(path, "rb") as f:
                data = pickle.load(f)

            # Check expiration
            if data.get("expires_at") is not None:
                if time.time() > data["expires_at"]:
                    path.unlink()  # Delete expired entry
                    return None

            return data.get("value")
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in persistent cache."""
        path = self._get_cache_path(key)

        expires_at = None
        if ttl_seconds is not None:
            expires_at = time.time() + ttl_seconds

        data = {
            "key": key,
            "value": value,
            "created_at": time.time(),
            "expires_at": expires_at,
        }

        try:
            with open(path, "wb") as f:
                pickle.dump(data, f)
        except Exception:
            pass  # Silently fail on write errors

    def delete(self, key: str) -> None:
        """Delete entry from persistent cache."""
        path = self._get_cache_path(key)
        try:
            path.unlink()
        except Exception:
            pass

    def clear(self) -> None:
        """Clear all persistent cache entries."""
        try:
            for cache_file in self.cache_dir.glob("*.cache"):
                cache_file.unlink()
        except Exception:
            pass


class CacheDecorator:
    """Decorator for caching function results."""

    def __init__(self, cache: MemoryCache, ttl_seconds: Optional[int] = None):
        """
        Initialize cache decorator.

        Args:
            cache: Cache instance to use
            ttl_seconds: TTL for cached results
        """
        self.cache = cache
        self.ttl = ttl_seconds

    def __call__(self, func: Callable) -> Callable:
        """Decorate function with caching."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{json.dumps([args, kwargs], default=str)}"

            # Try to get from cache
            result = self.cache.get(cache_key)
            if result is not None:
                return result

            # Call function and cache result
            result = func(*args, **kwargs)
            self.cache.set(cache_key, result, self.ttl)

            return result

        return wrapper
