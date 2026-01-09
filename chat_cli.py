#!/usr/bin/env python3
"""Terminal chat interface for Mini-Agent"""

import asyncio
import os
from dotenv import load_dotenv
from app.agent import Agent

load_dotenv()


async def main():
    print("=" * 60)
    print("Mini-Agent Terminal Chat")
    print("=" * 60)
    print("Type 'quit', 'exit', or 'q' to end the conversation\n")
    
    try:
        agent = Agent()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    context = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            response = await agent.process_message(user_input, context)
            print(f"\nAgent: {response}\n")
            
            context.append({"role": "user", "content": user_input})
            context.append({"role": "assistant", "content": response})
            
            if len(context) > 10:
                context = context[-10:]
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())