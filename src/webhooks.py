"""
Webhook system for event-driven architecture.

Supports event registration, triggering, and delivery with retry logic.
"""

import uuid
import httpx
import asyncio
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)


class EventType(Enum):
    """Event types in the system."""
    PLAN_CREATED = "plan.created"
    PLAN_STARTED = "plan.started"
    PLAN_COMPLETED = "plan.completed"
    PLAN_FAILED = "plan.failed"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    CONVERSATION_MESSAGE = "conversation.message"


@dataclass
class WebhookEvent:
    """A webhook event."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: EventType = EventType.PLAN_CREATED
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "timestamp": self.timestamp,
            "data": self.data,
            "metadata": self.metadata,
        }


@dataclass
class Webhook:
    """Webhook subscription."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    event_types: List[EventType] = field(default_factory=list)
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    secret: str = field(default_factory=lambda: str(uuid.uuid4()))
    retry_count: int = 3
    timeout_seconds: int = 30


@dataclass
class WebhookDelivery:
    """Record of webhook delivery attempt."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    webhook_id: str = ""
    event_id: str = ""
    status_code: Optional[int] = None
    error: Optional[str] = None
    attempts: int = 0
    next_retry: Optional[str] = None
    completed_at: Optional[str] = None


class WebhookManager:
    """Manage webhooks and event delivery."""

    def __init__(self):
        """Initialize webhook manager."""
        self.webhooks: Dict[str, Webhook] = {}
        self.deliveries: List[WebhookDelivery] = []
        self.event_handlers: Dict[EventType, List[Callable]] = {}

    def register_webhook(
        self,
        url: str,
        event_types: List[EventType],
        secret: Optional[str] = None
    ) -> Webhook:
        """Register a webhook."""
        webhook = Webhook(
            url=url,
            event_types=event_types,
            secret=secret or str(uuid.uuid4())
        )

        self.webhooks[webhook.id] = webhook
        logger.info(f"Webhook registered: {webhook.id} for {len(event_types)} events")

        return webhook

    def unregister_webhook(self, webhook_id: str) -> bool:
        """Unregister a webhook."""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Webhook unregistered: {webhook_id}")
            return True
        return False

    def list_webhooks(self, active_only: bool = True) -> List[Webhook]:
        """List webhooks."""
        webhooks = list(self.webhooks.values())
        if active_only:
            webhooks = [w for w in webhooks if w.active]
        return webhooks

    async def trigger_event(self, event: WebhookEvent) -> List[WebhookDelivery]:
        """Trigger event and deliver to matching webhooks."""
        deliveries: List[WebhookDelivery] = []

        for webhook in self.webhooks.values():
            # Check if webhook is active and subscribed to event
            if not webhook.active:
                continue

            if event.type not in webhook.event_types:
                continue

            # Create delivery record
            delivery = WebhookDelivery(
                webhook_id=webhook.id,
                event_id=event.id
            )

            # Try to deliver
            success = await self._deliver_webhook(webhook, event, delivery)

            if success:
                delivery.completed_at = datetime.now().isoformat()
            else:
                # Schedule retry
                delivery.next_retry = (
                    datetime.now() + timedelta(minutes=5)
                ).isoformat()

            self.deliveries.append(delivery)
            deliveries.append(delivery)

        return deliveries

    async def _deliver_webhook(
        self,
        webhook: Webhook,
        event: WebhookEvent,
        delivery: WebhookDelivery
    ) -> bool:
        """Deliver webhook to endpoint."""
        for attempt in range(webhook.retry_count):
            delivery.attempts = attempt + 1

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        webhook.url,
                        json=event.to_dict(),
                        timeout=webhook.timeout_seconds,
                        headers={
                            "X-Webhook-ID": webhook.id,
                            "X-Event-ID": event.id,
                            "X-Event-Type": event.type.value,
                            "X-Secret": webhook.secret,
                        }
                    )

                delivery.status_code = response.status_code

                if 200 <= response.status_code < 300:
                    logger.info(f"Webhook delivered: {webhook.id}")
                    return True

                # Retry on server errors
                if response.status_code >= 500 and attempt < webhook.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue

                delivery.error = f"HTTP {response.status_code}"
                return False

            except Exception as e:
                delivery.error = str(e)

                # Retry on connection errors
                if attempt < webhook.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue

                logger.error(f"Webhook delivery failed: {webhook.id} - {e}")
                return False

        return False

    def get_delivery_status(self, webhook_id: str) -> Dict[str, Any]:
        """Get delivery status for a webhook."""
        deliveries = [
            d for d in self.deliveries
            if d.webhook_id == webhook_id
        ]

        successful = len([d for d in deliveries if d.completed_at])
        failed = len([d for d in deliveries if d.error])
        pending = len([d for d in deliveries if d.next_retry])

        return {
            "webhook_id": webhook_id,
            "total_deliveries": len(deliveries),
            "successful": successful,
            "failed": failed,
            "pending": pending,
            "last_delivery": max(
                (d.completed_at for d in deliveries if d.completed_at),
                default=None
            ),
        }


class EventStream:
    """Server-sent events (SSE) stream for real-time updates."""

    def __init__(self, stream_id: str = None):
        """Initialize event stream."""
        self.stream_id = stream_id or str(uuid.uuid4())
        self.subscribers: List[Callable] = []
        self.events: List[WebhookEvent] = []

    def subscribe(self, callback: Callable) -> None:
        """Subscribe to events."""
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable) -> None:
        """Unsubscribe from events."""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def emit_event(self, event: WebhookEvent) -> None:
        """Emit event to all subscribers."""
        self.events.append(event)

        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"Error in event subscriber: {e}")

    def get_events(self, limit: int = 100) -> List[WebhookEvent]:
        """Get recent events."""
        return self.events[-limit:]

    def clear_events(self) -> None:
        """Clear event history."""
        self.events.clear()
