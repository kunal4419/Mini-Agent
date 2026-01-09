import os
from google import genai
from google.genai import types
from typing import Optional


class Agent:
    """Simple AI Agent using Google Gemini API"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-3-flash-preview'
        self.system_prompt = """You are a helpful AI assistant. You provide clear, 
        concise, and accurate responses to user queries. Be friendly and professional."""
    
    async def process_message(self, message: str, context: Optional[list] = None) -> str:
        """
        Process a user message and return agent's response
        
        Args:
            message: User's message
            context: Optional conversation context (list of previous messages)
        
        Returns:
            Agent's response as string
        """
        try:
            # Build the conversation history for Gemini
            contents = []
            
            # Add system instruction as first user message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=self.system_prompt)]
            ))
            contents.append(types.Content(
                role="model",
                parts=[types.Part(text="Understood. I'll be a helpful, clear, and professional AI assistant.")]
            ))
            
            # Add context if provided
            if context:
                for msg in context:
                    role = msg.get("role")
                    content = msg.get("content")
                    if role == "user":
                        contents.append(types.Content(role="user", parts=[types.Part(text=content)]))
                    elif role == "assistant":
                        contents.append(types.Content(role="model", parts=[types.Part(text=content)]))
            
            # Add current user message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents
            )
            
            return response.text
        
        except Exception as e:
            return f"Error processing message: {str(e)}"
    
    def set_system_prompt(self, prompt: str):
        """Update the system prompt"""
        self.system_prompt = prompt


# Global agent instance
agent = None

def get_agent() -> Agent:
    """Get or create agent instance"""
    global agent
    if agent is None:
        agent = Agent()
    return agent
