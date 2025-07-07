#!/usr/bin/env python3
"""
Test script to check what roles are allowed in the users table
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from database.supabase_client import get_supabase_client

async def test_roles():
    """Test different role values to see what's allowed"""
    try:
        client = get_supabase_client()
        
        # Try to get the table schema or constraints
        # We'll test by trying to insert users with different roles
        
        test_roles = ["user", "admin", "customer", "client", "member", "standard"]
        
        for role in test_roles:
            print(f"\nTesting role: '{role}'")
            
            test_user = {
                "name": f"Test {role}",
                "email": f"test-{role}@example.com",
                "password_hash": "testpass123",
                "role": role,
                "is_active": True,
                "email_verified": False
            }
            
            try:
                # Just try to insert - if successful, this role is allowed
                result = client.client.table('users').insert(test_user).execute()
                if result.data:
                    print(f"✅ Role '{role}' is ALLOWED")
                    # Clean up - delete the test user
                    try:
                        client.client.table('users').delete().eq('email', test_user['email']).execute()
                        print(f"   Cleaned up test user for role '{role}'")
                    except:
                        pass
                else:
                    print(f"❌ Role '{role}' failed for unknown reason")
                    
            except Exception as e:
                error_msg = str(e)
                if "users_role_check" in error_msg:
                    print(f"❌ Role '{role}' is NOT ALLOWED (constraint violation)")
                elif "duplicate key" in error_msg or "already exists" in error_msg:
                    print(f"⚠️  Role '{role}' might be allowed but email exists")
                else:
                    print(f"❌ Role '{role}' failed: {error_msg}")
        
        print("\n" + "="*50)
        print("ROLE TEST COMPLETED")
        print("="*50)
                    
    except Exception as e:
        print(f"Error in role test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_roles())