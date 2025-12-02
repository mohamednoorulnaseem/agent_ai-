"""
Conversation history tracking for the AI agent.
Manages messages and context across agent sessions.
"""

from typing import List, Dict, Any
from datetime import datetime


class ConversationMessage:
    """Represents a single message in the conversation."""
    
    def __init__(self, role: str, content: str, timestamp: datetime = None):
        self.role = role  # "user", "assistant", "system"
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


class ConversationHistory:
    """Manages conversation history."""
    
    def __init__(self, max_messages: int = 100):
        self.messages: List[ConversationMessage] = []
        self.max_messages = max_messages
        self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str):
        """Add a message to the history."""
        message = ConversationMessage(role, content)
        self.messages.append(message)
        
        # Keep only recent messages if exceeding limit
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self, last_n: int = None) -> List[Dict[str, str]]:
        """
        Get messages formatted for LLM API.
        
        Args:
            last_n: Number of recent messages to return. If None, returns all.
            
        Returns:
            List of messages formatted as {role, content}
        """
        if last_n:
            messages = self.messages[-last_n:]
        else:
            messages = self.messages
        
        return [{"role": m.role, "content": m.content} for m in messages]
    
    def get_full_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history with timestamps."""
        return [m.to_dict() for m in self.messages]
    
    def clear(self):
        """Clear all messages."""
        self.messages = []
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation."""
        return {
            "total_messages": len(self.messages),
            "created_at": self.created_at.isoformat(),
            "last_message": self.messages[-1].to_dict() if self.messages else None,
            "user_messages": sum(1 for m in self.messages if m.role == "user"),
            "assistant_messages": sum(1 for m in self.messages if m.role == "assistant"),
        }
