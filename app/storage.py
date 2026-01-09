from typing import List, Dict, Optional
from datetime import datetime


class InMemoryStorage:
    """Simple in-memory storage for chat history"""
    
    def __init__(self):
        self.history: List[Dict] = []
    
    def add_message(self, user_id: str, user_message: str, agent_response: str):
        """Add a conversation to history"""
        self.history.append({
            "user_id": user_id,
            "user_message": user_message,
            "agent_response": agent_response,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_history(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get chat history, optionally filtered by user_id"""
        if user_id:
            return [item for item in self.history if item["user_id"] == user_id]
        return self.history
    
    def clear_history(self, user_id: Optional[str] = None):
        """Clear chat history"""
        if user_id:
            self.history = [item for item in self.history if item["user_id"] != user_id]
        else:
            self.history = []


# Global storage instance
storage = InMemoryStorage()
