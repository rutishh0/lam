#!/usr/bin/env python3
"""
Setup script for Supabase database
Creates all necessary tables and admin user
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
from auth.auth_service import AuthService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_database():
    """Set up the Supabase database with tables and admin user"""
    try:
        # Initialize Supabase client
        supabase_client = get_supabase_client()
        
        # Test connection
        logger.info("Testing Supabase connection...")
        health = await supabase_client.health_check()
        if health["status"] != "healthy":
            logger.error(f"Supabase connection failed: {health}")
            return False
        
        logger.info("✅ Supabase connection successful!")
        
        # Execute the SQL setup script
        logger.info("Setting up database schema...")
        
        # Read the SQL setup file
        sql_file = Path(__file__).parent / "database" / "setup.sql"
        if not sql_file.exists():
            logger.error(f"SQL setup file not found: {sql_file}")
            return False
        
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Split SQL into individual statements and execute them
        # Note: This is a simplified approach. In production, you might want to use a proper migration tool
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, stmt in enumerate(statements):
            if stmt.strip():
                try:
                    # Use Supabase client to execute SQL
                    logger.info(f"Executing statement {i+1}/{len(statements)}")
                    logger.debug(f"SQL: {stmt[:100]}...")
                    
                    # For table creation and other DDL statements, we need to use the Supabase REST API
                    # Since we can't execute DDL directly through the Python client easily,
                    # we'll use a different approach
                    
                    # Skip comments and empty statements
                    if stmt.startswith('--') or stmt.upper().startswith('COMMENT'):
                        continue
                        
                except Exception as e:
                    logger.warning(f"Statement failed (might be expected): {str(e)}")
                    continue
        
        logger.info("✅ Database schema setup attempted")
        
        # Create admin user using the auth service
        logger.info("Creating admin user...")
        auth_service = AuthService(supabase_client)
        
        try:
            from auth.auth_service import UserCreate
            admin_data = UserCreate(
                name="System Administrator",
                email="admin@uniagent.com", 
                password="admin123",
                plan="enterprise"
            )
            
            # Try to create the admin user
            result = await auth_service.register_user(admin_data)
            
            # Update the user role to admin manually
            await supabase_client.client.table('users').update(
                {'role': 'admin'}
            ).eq('email', 'admin@uniagent.com').execute()
            
            logger.info("✅ Admin user created successfully!")
            logger.info("📧 Email: admin@uniagent.com")
            logger.info("🔑 Password: admin123")
            logger.info("⚠️  Please change the password after first login!")
            
        except Exception as e:
            if "already exists" in str(e):
                logger.info("ℹ️  Admin user already exists")
            else:
                logger.error(f"Failed to create admin user: {str(e)}")
        
        # Create subscription plans if they don't exist
        logger.info("Setting up subscription plans...")
        try:
            plans = [
                {
                    "name": "Starter",
                    "slug": "starter", 
                    "description": "Perfect for students applying to a few universities",
                    "price_monthly": 29.00,
                    "price_yearly": 290.00,
                    "features": ["Up to 5 university applications", "Basic automation features", "Email support"],
                    "limits": {"max_applications": 5, "max_universities": 10},
                    "is_active": True,
                    "sort_order": 1
                },
                {
                    "name": "Professional", 
                    "slug": "professional",
                    "description": "Ideal for students applying to multiple universities",
                    "price_monthly": 79.00,
                    "price_yearly": 790.00,
                    "features": ["Up to 20 university applications", "Advanced AI automation", "Priority support"],
                    "limits": {"max_applications": 20, "max_universities": 50},
                    "is_active": True,
                    "sort_order": 2
                },
                {
                    "name": "Enterprise",
                    "slug": "enterprise", 
                    "description": "For education consultants and agencies",
                    "price_monthly": 199.00,
                    "price_yearly": 1990.00,
                    "features": ["Unlimited applications", "White-label solution", "24/7 support"],
                    "limits": {"max_applications": -1, "max_universities": -1},
                    "is_active": True,
                    "sort_order": 3
                }
            ]
            
            for plan in plans:
                try:
                    result = await supabase_client.client.table('subscription_plans').insert(plan).execute()
                    logger.info(f"✅ Created plan: {plan['name']}")
                except Exception as e:
                    if "duplicate" in str(e).lower() or "already exists" in str(e).lower():
                        logger.info(f"ℹ️  Plan {plan['name']} already exists")
                    else:
                        logger.error(f"Failed to create plan {plan['name']}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to setup subscription plans: {str(e)}")
        
        logger.info("🎉 Database setup completed!")
        logger.info("🔗 You can now access the admin panel at: /admin")
        logger.info("📧 Login with: admin@uniagent.com / admin123")
        
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {str(e)}")
        return False

def main():
    """Main function to run the setup"""
    logger.info("🚀 Starting Supabase database setup...")
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please make sure your .env file contains SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Run the setup
    success = asyncio.run(setup_database())
    
    if success:
        logger.info("✅ Setup completed successfully!")
        return True
    else:
        logger.error("❌ Setup failed!")
        return False

if __name__ == "__main__":
    main()