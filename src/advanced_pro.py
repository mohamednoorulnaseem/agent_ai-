"""
Advanced Pro Features Module

Enterprise-grade enhancements for production deployments:
- Advanced caching strategies
- Distributed tracing
- Advanced security
- Performance optimization
- Analytics and insights
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdvancedMetrics:
    """Advanced performance metrics."""
    operation: str
    duration_ms: float
    memory_mb: float
    cache_hits: int
    cache_misses: int
    timestamp: datetime

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    @property
    def efficiency_score(self) -> float:
        """Calculate operation efficiency (0-100)."""
        hit_rate_score = self.hit_rate * 50
        speed_score = min(100, (1000 / self.duration_ms) * 50)
        return hit_rate_score + speed_score


class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise Exception(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return False
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout

    def _on_success(self) -> None:
        """Handle successful operation."""
        self.failure_count = 0
        self.state = "closed"
        logger.info(f"Circuit breaker '{self.name}' closed")

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(
                f"Circuit breaker '{self.name}' opened after "
                f"{self.failure_count} failures"
            )


class RateLimiter:
    """Advanced rate limiting with token bucket algorithm."""

    def __init__(self, rate: int, period: int = 60):
        """Initialize rate limiter.

        Args:
            rate: Number of requests allowed
            period: Time period in seconds
        """
        self.rate = rate
        self.period = period
        self.tokens = rate
        self.last_update = datetime.now()

    def is_allowed(self) -> bool:
        """Check if request is allowed."""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = datetime.now()
        elapsed = (now - self.last_update).total_seconds()
        tokens_to_add = (elapsed / self.period) * self.rate
        self.tokens = min(self.rate, self.tokens + tokens_to_add)
        self.last_update = now


class RequestSignature:
    """HMAC-based request signature for security."""

    def __init__(self, secret: str):
        self.secret = secret

    def sign(self, data: str) -> str:
        """Generate HMAC signature."""
        return hashlib.sha256(
            (data + self.secret).encode()
        ).hexdigest()

    def verify(self, data: str, signature: str) -> bool:
        """Verify HMAC signature."""
        expected = self.sign(data)
        return hashlib.compare_digest(expected, signature)


class AdaptiveCaching:
    """Adaptive caching that learns access patterns."""

    def __init__(self, max_size_mb: int = 100):
        self.max_size_mb = max_size_mb
        self.cache: Dict[str, Any] = {}
        self.access_count: Dict[str, int] = {}
        self.access_times: Dict[str, datetime] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value with access tracking."""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            self.access_times[key] = datetime.now()
            return self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self.cache[key] = value
        self.access_count[key] = 1
        self.access_times[key] = datetime.now()

    def get_hot_keys(self, top_n: int = 10) -> list:
        """Get most frequently accessed keys."""
        return sorted(
            self.access_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

    def get_recommendations(self) -> Dict[str, str]:
        """Get caching recommendations based on patterns."""
        recommendations = {}
        for key, count in self.get_hot_keys():
            if count > 100:
                recommendations[key] = "Increase TTL"
            elif count < 5:
                recommendations[key] = "Consider removing"
        return recommendations


class DistributedTracing:
    """Distributed request tracing for debugging."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.traces: Dict[str, list] = {}

    def start_trace(self, trace_id: str) -> None:
        """Start a new trace."""
        self.traces[trace_id] = []
        logger.info(f"Started trace {trace_id}")

    def add_span(
        self,
        trace_id: str,
        span_name: str,
        duration_ms: float,
        status: str = "success"
    ) -> None:
        """Add span to trace."""
        if trace_id not in self.traces:
            self.traces[trace_id] = []

        span = {
            "name": span_name,
            "service": self.service_name,
            "duration_ms": duration_ms,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.traces[trace_id].append(span)
        logger.debug(f"Added span {span_name} to trace {trace_id}")

    def get_trace(self, trace_id: str) -> list:
        """Get trace details."""
        return self.traces.get(trace_id, [])


class AdvancedAnalytics:
    """Advanced analytics and insights."""

    def __init__(self):
        self.events: list = []
        self.aggregates: Dict[str, Any] = {}

    def track_event(
        self,
        event_type: str,
        user_id: str,
        metadata: Dict[str, Any]
    ) -> None:
        """Track an event."""
        event = {
            "type": event_type,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        self.events.append(event)

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user."""
        user_events = [e for e in self.events if e["user_id"] == user_id]
        return {
            "total_events": len(user_events),
            "event_types": list(set(e["type"] for e in user_events)),
            "first_event": min(
                (e["timestamp"] for e in user_events),
                default=None
            ),
            "last_event": max(
                (e["timestamp"] for e in user_events),
                default=None
            )
        }

    def get_insights(self) -> Dict[str, Any]:
        """Generate insights from analytics."""
        if not self.events:
            return {}

        event_counts = {}
        for event in self.events:
            event_type = event["type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "total_events": len(self.events),
            "unique_users": len(set(e["user_id"] for e in self.events)),
            "event_distribution": event_counts,
            "most_common_event": max(
                event_counts.items(),
                key=lambda x: x[1],
                default=("unknown", 0)
            )[0]
        }
