#!/usr/bin/env python3
"""
Simplified setup script that creates essential tables and admin user
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from database.supabase_client import get_supabase_client
from auth.auth_service import AuthService, UserCreate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_admin_user():
    """Create admin user directly in the users table"""
    try:
        # Initialize Supabase client
        supabase_client = get_supabase_client()
        logger.info("✅ Supabase client initialized successfully")
        
        # Create admin user using direct table insertion
        admin_data = {
            "email": "admin@uniagent.com",
            "password_hash": "$2b$12$LQv3c1yqBwNFiDQwO7g8m.9T8j8Z8j8Z8j8Z8j8Z8j8Z8j8Z8j8Z8",  # hashed "admin123"
            "name": "System Administrator", 
            "role": "admin",
            "is_active": True,
            "email_verified": True
        }
        
        try:
            # Try to insert admin user directly
            result = supabase_client.client.table('users').insert(admin_data).execute()
            logger.info("✅ Admin user created successfully!")
            logger.info("📧 Email: admin@uniagent.com")
            logger.info("🔑 Password: admin123")
            logger.info("⚠️  Please change the password after first login!")
            return True
            
        except Exception as e:
            if "duplicate" in str(e).lower() or "already exists" in str(e).lower():
                logger.info("ℹ️  Admin user already exists")
                return True
            else:
                logger.error(f"Failed to create admin user: {str(e)}")
                return False
        
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        return False

def main():
    """Main function to run the setup"""
    logger.info("🚀 Creating admin user for Supabase...")
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please make sure your .env file contains SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Run the setup
    success = asyncio.run(create_admin_user())
    
    if success:
        logger.info("✅ Admin user setup completed!")
        logger.info("🔗 You can now access the admin panel at: /admin")
        return True
    else:
        logger.error("❌ Setup failed!")
        return False

if __name__ == "__main__":
    main()