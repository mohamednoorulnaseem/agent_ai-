"""
WebSocket support for real-time agent updates.
Enables live task execution monitoring and instant notifications.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from typing import Dict, List, Set
from datetime import datetime


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.client_subscriptions: Dict[WebSocket, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        
        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()
        
        self.active_connections[client_id].add(websocket)
        self.client_subscriptions[websocket] = set()
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            self.active_connections[client_id].discard(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        
        self.client_subscriptions.pop(websocket, None)
    
    async def subscribe(self, websocket: WebSocket, topic: str):
        """Subscribe to a topic (e.g., plan_123, execution)."""
        self.client_subscriptions[websocket].add(topic)
        await websocket.send_json({
            "type": "subscription",
            "topic": topic,
            "status": "subscribed",
            "timestamp": datetime.now().isoformat()
        })
    
    async def broadcast(self, topic: str, data: Dict):
        """Broadcast message to all subscribers of a topic."""
        message = {
            "type": "update",
            "topic": topic,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        for client_connections in self.active_connections.values():
            for connection in client_connections:
                if topic in self.client_subscriptions.get(connection, set()):
                    try:
                        await connection.send_json(message)
                    except Exception:
                        pass
    
    async def send_personal(self, websocket: WebSocket, data: Dict):
        """Send message to specific connection."""
        try:
            await websocket.send_json(data)
        except Exception:
            pass


# Global connection manager
manager = ConnectionManager()


# WebSocket router
ws_router = APIRouter()


@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe":
                # Subscribe to a topic
                await manager.subscribe(websocket, message.get("topic"))
            
            elif message.get("type") == "ping":
                # Respond to ping
                await manager.send_personal(websocket, {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif message.get("type") == "execute_task":
                # Trigger task execution
                plan_id = message.get("plan_id")
                task_id = message.get("task_id")
                
                # Broadcast that execution started
                await manager.broadcast(f"plan_{plan_id}", {
                    "event": "task_started",
                    "task_id": task_id,
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


class EventBroadcaster:
    """Broadcasts real-time events to connected clients."""
    
    @staticmethod
    async def task_started(plan_id: int, task_id: int, description: str):
        """Broadcast task started event."""
        await manager.broadcast(f"plan_{plan_id}", {
            "event": "task_started",
            "plan_id": plan_id,
            "task_id": task_id,
            "description": description,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    async def task_progress(plan_id: int, task_id: int, progress: int, message: str):
        """Broadcast task progress update."""
        await manager.broadcast(f"plan_{plan_id}", {
            "event": "task_progress",
            "plan_id": plan_id,
            "task_id": task_id,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    async def task_completed(plan_id: int, task_id: int, result: str):
        """Broadcast task completion."""
        await manager.broadcast(f"plan_{plan_id}", {
            "event": "task_completed",
            "plan_id": plan_id,
            "task_id": task_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    async def task_failed(plan_id: int, task_id: int, error: str):
        """Broadcast task failure."""
        await manager.broadcast(f"plan_{plan_id}", {
            "event": "task_failed",
            "plan_id": plan_id,
            "task_id": task_id,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    async def plan_updated(plan_id: int, status: str, summary: str):
        """Broadcast plan update."""
        await manager.broadcast(f"plan_{plan_id}", {
            "event": "plan_updated",
            "plan_id": plan_id,
            "status": status,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
