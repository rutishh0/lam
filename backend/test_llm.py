"""
Test script to verify LLM service functionality
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from services.llm_service import get_llm_service

async def test_llm_service():
    """Test the LLM service with a simple prompt."""
    print("🧪 Testing LLM Service...")
    
    try:
        llm = get_llm_service()
        print("✅ LLM service initialized")
        
        # Test simple generation
        response = await llm.generate_response(
            prompt="Say 'Hello! I am working correctly!' and explain what you can do in one sentence.",
            model_name="gemini-2.0-flash-exp"
        )
        
        print(f"✅ LLM Response: {response}")
        print("🎉 LLM Service is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        print("💡 Make sure your GOOGLE_API_KEY is set correctly in .env")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_llm_service())
    if result:
        print("\n🚀 Your LLM integration is ready for automation tasks!")
    else:
        print("\n🔧 Please check your API key configuration") 