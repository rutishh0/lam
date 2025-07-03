# 🔑 Environment Variables Setup

## Backend Environment File (`backend/.env`)

Create a file called `.env` in the `backend` folder and copy this content:

```env
# AI LAM Backend Environment Variables
# Development Configuration

# JWT Configuration
JWT_SECRET=c58CLE2yElt72lnMEOPDexbElUdjIGjgX73ipSZNOkY
JWT_REFRESH_SECRET=DtEQfCVAI2wVbI2BBROx01I1NNe3GqHcRaTjLrjjUiQ
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Supabase Configuration
SUPABASE_URL=https://nwtzhzagqfuedslјngkl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo
SUPABASE_SERVICE_KEY=YOUR_SERVICE_ROLE_KEY_HERE

# Application Settings
ENVIRONMENT=development
PORT=8000
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Optional Services (uncomment when ready)
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_PUBLISHABLE_KEY=pk_test_...
# SENDGRID_API_KEY=SG.your-sendgrid-key
# TWILIO_ACCOUNT_SID=your-twilio-sid
# TWILIO_AUTH_TOKEN=your-twilio-token

# Feature Flags
ENABLE_EMAIL_VERIFICATION=false
ENABLE_SMS_NOTIFICATIONS=false
```

## Frontend Environment File (`frontend/.env`)

Create a file called `.env` in the `frontend` folder and copy this content:

```env
# AI LAM Frontend Environment Variables
# Development Configuration

# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SUPABASE_URL=https://nwtzhzagqfuedslјngkl.supabase.co
REACT_APP_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo

# Optional Payment Configuration (when ready)
# REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## 🚨 IMPORTANT: Get Your Service Role Key

You still need to get your **SUPABASE_SERVICE_KEY** from Supabase:

1. Go to your Supabase Dashboard → Settings → API
2. Look for "Project API keys" section
3. Find the **service_role** key (NOT the anon key)
4. Copy it and replace `YOUR_SERVICE_ROLE_KEY_HERE` in your backend `.env` file

## 📋 Quick Setup Steps

1. **Copy backend environment**:
   ```bash
   # Create backend/.env file and paste the backend content above
   ```

2. **Copy frontend environment**:
   ```bash
   # Create frontend/.env file and paste the frontend content above
   ```

3. **Get Service Role Key**:
   - Replace `YOUR_SERVICE_ROLE_KEY_HERE` with your actual service role key from Supabase

4. **Test locally**:
   ```bash
   # Start backend
   cd backend
   python -m uvicorn server:app --reload

   # Start frontend (new terminal)
   cd frontend
   npm start
   ```

## 🚀 For Production Deployment

When deploying to Railway/Vercel, use the same values but:
- Set `ENVIRONMENT=production`
- Update `REACT_APP_API_URL` to your Railway backend URL
- Add production CORS origins

## ⚠️ Security Notes

- Never commit `.env` files to git (they're in .gitignore)
- Keep your service role key secret
- Use different JWT secrets for production
- Enable HTTPS in production 