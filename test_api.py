#!/usr/bin/env python3
"""
Simple test script for Mini-Agent API
Run this after starting the server to test the endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_chat(message: str, user_id: str = "default"):
    """Test chat endpoint"""
    print(f"Testing chat with message: '{message}'...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message, "user_id": user_id}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_history(user_id: str = "default"):
    """Test history endpoint"""
    print(f"Testing history for user: {user_id}...")
    response = requests.get(f"{BASE_URL}/history", params={"user_id": user_id})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_info():
    """Test info endpoint"""
    print("Testing info endpoint...")
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Mini-Agent API Test")
    print("=" * 60 + "\n")
    
    # Test health
    test_health()
    
    # Test info
    test_info()
    
    # Test chat
    test_chat("Hello! What can you help me with?")
    test_chat("Tell me a fun fact about Python programming")
    
    # Test history
    test_history()
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)
