# Supabase Database Setup Instructions

## Quick Setup Guide

Your Supabase project is already configured with the following credentials:
- **Project URL**: `https://nwtzhzagqfuedsljngkl.supabase.co`
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo`

## Step 1: Create the Database Tables

1. **Go to your Supabase Dashboard**:
   - Visit: https://supabase.com/dashboard
   - Navigate to your project: `nwtzhzagqfuedsljngkl`

2. **Open SQL Editor**:
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Copy and Run the SQL**:
   - Copy the entire contents of `backend/database/setup.sql`
   - Paste it into the SQL editor
   - Click "Run" to execute

## Step 2: Create Environment File

Create a `.env` file in the `backend` directory with these contents:

```env
# Supabase Database Configuration
SUPABASE_URL=https://nwtzhzagqfuedsljngkl.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo

# Encryption Configuration
ENCRYPTION_MASTER_KEY=your-32-char-encryption-key-here

# Email Configuration (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Twilio Configuration (for SMS)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_FROM_NUMBER=+1234567890

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Application Settings
LOG_LEVEL=INFO
MAX_CONCURRENT_BROWSERS=3
BROWSER_TIMEOUT=30000
DAILY_CHECK_TIME=09:00

# Security Settings
JWT_SECRET=your-jwt-secret-key
SESSION_SECRET=your-session-secret
```

## Step 3: Test the Setup

Run the database setup script to verify everything is working:

```bash
cd backend
python setup_database.py
```

You should see a success message indicating all tables are accessible.

## Step 4: Start the Application

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn server:app --reload
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access Dashboard**:
   Open http://localhost:3000 in your browser

## What Tables Are Created?

The setup script creates these tables:

- **clients**: Stores encrypted client information
- **application_tasks**: Tracks individual application submissions  
- **mock_applications**: Testing and mock university data
- **application_status_log**: Audit trail of status changes
- **performance_metrics**: System performance and analytics

## Troubleshooting

**If you see "relation does not exist" errors:**
- Make sure you ran the SQL script in the Supabase dashboard
- Check that you're connected to the correct project
- Verify the SQL script ran without errors

**If connection fails:**
- Double-check the SUPABASE_URL and SUPABASE_KEY in your .env file
- Ensure your Supabase project is active
- Check your internet connection

**For permission errors:**
- Make sure you're using the correct API key (anon key for development)
- Check if Row Level Security (RLS) is enabled (disable for development)

## Next Steps

Once the database is set up:
1. Create your first client through the dashboard
2. Set up university applications
3. Monitor progress through the analytics dashboard
4. Configure email/SMS notifications for updates

For production deployment, remember to:
- Enable Row Level Security (RLS) 
- Use service role key for server-side operations
- Set up proper backup and monitoring
- Configure environment-specific settings 