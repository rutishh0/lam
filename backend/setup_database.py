#!/usr/bin/env python3
"""
Database Setup Script for Autonomous University Application Agent
This script initializes the Supabase database with all necessary tables.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

def setup_database():
    """Setup Supabase database with provided credentials"""
    
    # Load environment variables
    load_dotenv()
    
    # Use provided credentials
    SUPABASE_URL = "https://nwtzhzagqfuedsljngkl.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo"
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY are required")
        sys.exit(1)
    
    try:
        # Initialize Supabase client
        print("🔌 Connecting to Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test connection
        print("🧪 Testing connection...")
        result = supabase.table('clients').select('id').limit(1).execute()
        print("✅ Connection successful!")
        
        # Read and execute SQL setup script
        setup_sql_path = Path(__file__).parent / "database" / "setup.sql"
        
        if not setup_sql_path.exists():
            print(f"❌ Error: Setup SQL file not found at {setup_sql_path}")
            sys.exit(1)
        
        print("📖 Reading database setup script...")
        with open(setup_sql_path, 'r') as f:
            sql_content = f.read()
        
        print("🗄️  Setting up database tables...")
        
        # Split SQL commands and execute them
        # Note: Supabase Python client doesn't support direct SQL execution
        # You'll need to run the SQL manually in the Supabase dashboard
        print("""
📋 DATABASE SETUP INSTRUCTIONS:

Since the Supabase Python client doesn't support direct SQL execution,
please follow these steps to set up your database:

1. Open your Supabase dashboard: https://supabase.com/dashboard
2. Navigate to your project: nwtzhzagqfuedsljngkl
3. Go to "SQL Editor" in the left sidebar
4. Copy the contents of 'backend/database/setup.sql'
5. Paste it into the SQL editor and click "Run"

This will create all necessary tables, indexes, and triggers.

Alternatively, you can use the Supabase CLI:
1. Install Supabase CLI: npm install -g supabase
2. Login: supabase login
3. Link project: supabase link --project-ref nwtzhzagqfuedsljngkl
4. Run migration: supabase db push

Your database credentials are:
- URL: {SUPABASE_URL}
- Anon Key: {SUPABASE_KEY[:20]}...
        """)
        
        # Test basic table access
        print("🔍 Testing table access...")
        
        # Try to access each table to verify they exist
        tables_to_test = ['clients', 'application_tasks', 'mock_applications', 
                         'application_status_log', 'performance_metrics']
        
        tables_exist = []
        for table in tables_to_test:
            try:
                result = supabase.table(table).select('*').limit(1).execute()
                tables_exist.append(table)
                print(f"✅ Table '{table}' is accessible")
            except Exception as e:
                print(f"❌ Table '{table}' not found or not accessible: {str(e)}")
        
        if len(tables_exist) == len(tables_to_test):
            print("\n🎉 All tables are accessible! Database setup appears complete.")
            
            # Create a sample client for testing
            print("\n📝 Creating sample data for testing...")
            try:
                sample_client = {
                    "full_name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "+44 7123 456789",
                    "date_of_birth": "2000-05-15",
                    "nationality": "British",
                    "address": "123 Main St, London, UK",
                    "personal_statement": "I am passionate about computer science and want to pursue my studies at a top university.",
                    "academic_history": [
                        {
                            "institution": "London Grammar School",
                            "qualification": "A-Levels",
                            "subjects": ["Mathematics", "Physics", "Computer Science"],
                            "grades": ["A*", "A", "A"],
                            "year": 2022
                        }
                    ],
                    "course_preferences": [
                        {
                            "university": "University of Oxford",
                            "course": "Computer Science",
                            "entry_requirements": "AAA",
                            "personal_interest": "Artificial Intelligence and Machine Learning"
                        }
                    ],
                    "documents": {}
                }
                
                result = supabase.table('clients').insert(sample_client).execute()
                if result.data:
                    print(f"✅ Sample client created with ID: {result.data[0]['id']}")
                    
                    # Clean up the test client
                    supabase.table('clients').delete().eq('id', result.data[0]['id']).execute()
                    print("🧹 Test client cleaned up")
                    
            except Exception as e:
                print(f"⚠️  Could not create sample client: {str(e)}")
                print("This is normal if tables haven't been created yet.")
        
        else:
            print(f"\n⚠️  Only {len(tables_exist)}/{len(tables_to_test)} tables are accessible.")
            print("Please run the setup.sql script in your Supabase dashboard first.")
        
        print(f"\n✅ Setup complete! Your application is configured to use Supabase.")
        print(f"🔧 Make sure to set these environment variables:")
        print(f"   SUPABASE_URL={SUPABASE_URL}")
        print(f"   SUPABASE_KEY={SUPABASE_KEY}")
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Supabase Database Setup...")
    setup_database() 