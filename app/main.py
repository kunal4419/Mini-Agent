from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

from .models import ChatMessage, ChatResponse, HistoryItem, HealthResponse
from .agent import get_agent
from .storage import storage

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Mini-Agent API",
    description="A simple AI agent bot built with FastAPI and Google Gemini API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the static directory path
STATIC_DIR = Path(__file__).parent.parent / "static"

# Mount static files
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def serve_chat():
    """Serve the chat interface"""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HealthResponse(
        status="healthy",
        message="Mini-Agent is running with Google Gemini!",
        timestamp=datetime.now().isoformat()
    )


@app.head("/", include_in_schema=False)
def head_home():
    # Render health checks may use HEAD
    return Response(status_code=200)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Mini-Agent is running with Google Gemini!",
        timestamp=datetime.now().isoformat()
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Send a message to the AI agent and get a response
    
    - **message**: The user's message
    - **user_id**: Optional user identifier (default: "default")
    """
    try:
        # Get agent instance
        agent = get_agent()
        
        # Get conversation history for context
        history = storage.get_history(message.user_id)
        context = []
        
        # Add last 5 messages as context
        for item in history[-5:]:
            context.append({"role": "user", "content": item["user_message"]})
            context.append({"role": "assistant", "content": item["agent_response"]})
        
        # Process message
        response_text = await agent.process_message(message.message, context)
        
        # Store in history
        storage.add_message(
            user_id=message.user_id,
            user_message=message.message,
            agent_response=response_text
        )
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            user_id=message.user_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=list[HistoryItem])
async def get_history(user_id: str = "default"):
    """
    Get chat history for a specific user
    
    - **user_id**: User identifier (default: "default")
    """
    history = storage.get_history(user_id)
    return [
        HistoryItem(
            user_message=item["user_message"],
            agent_response=item["agent_response"],
            timestamp=item["timestamp"],
            user_id=item["user_id"]
        )
        for item in history
    ]


@app.delete("/history")
async def clear_history(user_id: str = "default"):
    """
    Clear chat history for a specific user
    
    - **user_id**: User identifier (default: "default")
    """
    storage.clear_history(user_id)
    return {"message": f"History cleared for user: {user_id}"}


@app.get("/info")
async def info():
    """Get API information"""
    return {
        "name": "Mini-Agent",
        "version": "1.0.0",
        "description": "A simple AI agent bot powered by Google Gemini",
        "model": "gemini-2.0-flash-exp",
        "endpoints": {
            "health": "GET /",
            "chat": "POST /chat",
            "history": "GET /history",
            "clear_history": "DELETE /history",
            "docs": "GET /docs"
        }
    }
