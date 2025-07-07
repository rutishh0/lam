#!/usr/bin/env python3
"""
Script to create necessary database tables in Supabase
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from database.supabase_client import get_supabase_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all necessary tables in Supabase"""
    try:
        client = get_supabase_client()
        
        # Note: In Supabase, you typically create tables through the dashboard or SQL editor
        # Let's try to create tables using raw SQL if the client supports it
        
        # Check if users table exists
        try:
            result = client.table('users').select('*').limit(1).execute()
            logger.info("✓ Users table exists")
        except Exception as e:
            logger.error(f"❌ Users table does not exist or has issues: {str(e)}")
            logger.info("Please create the users table manually in your Supabase dashboard")
            
        # Check if other tables exist
        tables_to_check = [
            'clients',
            'application_tasks', 
            'subscription_plans',
            'user_subscriptions',
            'usage_tracking'
        ]
        
        for table_name in tables_to_check:
            try:
                result = client.table(table_name).select('*').limit(1).execute()
                logger.info(f"✓ {table_name} table exists")
            except Exception as e:
                logger.warning(f"⚠️  {table_name} table may not exist: {str(e)}")
        
        # Let's print the SQL schema that should be created
        print("\n" + "="*60)
        print("SQL SCHEMA TO CREATE IN SUPABASE DASHBOARD:")
        print("="*60)
        print("""
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Clients table
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    date_of_birth TEXT,
    nationality TEXT,
    address TEXT,
    personal_statement TEXT,
    academic_history JSONB,
    course_preferences JSONB,
    documents JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Application tasks table
CREATE TABLE application_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    university_name TEXT NOT NULL,
    course_name TEXT NOT NULL,
    course_code TEXT,
    application_url TEXT,
    status TEXT DEFAULT 'pending',
    credentials JSONB,
    application_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    last_checked TIMESTAMP WITH TIME ZONE,
    error_log JSONB
);

-- Subscription plans table
CREATE TABLE subscription_plans (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL,
    features JSONB,
    limits JSONB
);

-- User subscriptions table
CREATE TABLE user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    plan_id TEXT REFERENCES subscription_plans(id),
    status TEXT DEFAULT 'active',
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE
);

-- Usage tracking table
CREATE TABLE usage_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_tracking ENABLE ROW LEVEL SECURITY;

-- Basic policies (adjust as needed)
CREATE POLICY "Users can view own data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Clients can view own data" ON clients FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Applications for own clients" ON application_tasks FOR SELECT USING (
    client_id IN (SELECT id FROM clients WHERE user_id = auth.uid())
);
""")
        print("="*60)
        print("\nPlease copy this SQL and run it in your Supabase SQL Editor.")
        print("You can access it at: https://app.supabase.com/project/nwtzhzagqfuedsljngkl/sql")
        
    except Exception as e:
        logger.error(f"Error checking tables: {str(e)}")

if __name__ == "__main__":
    create_tables()