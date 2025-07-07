#!/usr/bin/env python3
"""
Test Supabase connection
"""

import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

async def test_connection():
    """Test the Supabase connection"""
    try:
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ Missing SUPABASE_URL or SUPABASE_KEY")
            return False
        
        print(f"🔗 Connecting to: {url}")
        
        # Create Supabase client
        supabase = create_client(url, key)
        
        # Test simple query
        result = supabase.table('users').select('*').limit(1).execute()
        
        print("✅ Supabase connection successful!")
        print(f"📊 Found {len(result.data)} user(s)")
        
        if result.data:
            for user in result.data:
                print(f"👤 User: {user.get('email')} (Role: {user.get('role')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())