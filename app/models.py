from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    message: str = Field(..., description="User message to send to the agent")
    user_id: Optional[str] = Field(default="default", description="User identifier")


class ChatResponse(BaseModel):
    response: str = Field(..., description="Agent's response")
    timestamp: str = Field(..., description="Response timestamp")
    user_id: str = Field(..., description="User identifier")


class HistoryItem(BaseModel):
    user_message: str
    agent_response: str
    timestamp: str
    user_id: str


class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str
