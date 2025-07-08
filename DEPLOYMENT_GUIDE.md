# 🚀 Complete Deployment Guide: AI LAM

Deploy your AI-powered form automation platform with **Backend on Railway.com** and **Frontend on Vercel**.

## 📋 Deployment Overview

- **Backend** → Railway.com (Python, AI processing, browser automation)
- **Frontend** → Vercel (React app, user interface)
- **Database** → Supabase (already configured)
- **AI** → Gemini 2.5 Flash API

---

## 🚂 Part 1: Backend Deployment on Railway.com

### Step 1: Prepare Your Backend

```bash
cd backend

# Create railway.toml (if not exists)
echo '[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn server:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[env]
PYTHONPATH = "/app/backend"
PLAYWRIGHT_BROWSERS_PATH = "/usr/lib/playwright"
PLAYWRIGHT_HEADLESS = "true"' > railway.toml
```

### Step 2: Create Railway Project

1. **Go to Railway.com**
   - Visit https://railway.app
   - Click "Start a New Project"
   - Choose "Deploy from GitHub repo"

2. **Connect GitHub**
   - Authorize Railway to access your GitHub
   - Select your AI LAM repository
   - Choose the `main` branch

### Step 3: Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
# Essential Variables
JWT_SECRET=your-super-secret-jwt-key-min-32-chars-production
JWT_REFRESH_SECRET=your-super-secret-refresh-key-min-32-chars-production
GEMINI_API_KEY=AIzaSyA2piC0ztJ1_LjcxW8BA3IJFgR689jZkl0
GEMINI_MODEL=gemini-2.5-flash
ENABLE_AI_ANALYSIS=true

# Supabase (your existing config)
SUPABASE_URL=https://nwtzhzagqfuedsljngkl.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo

# Server Config
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Railway Config
RAILWAY_ENVIRONMENT=production
PYTHONPATH=/app/backend
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true
```

### Step 4: Configure Deployment Settings

1. **Root Directory**: Set to `backend`
2. **Build Command**: `pip install -r requirements.txt && playwright install chromium`
3. **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Step 5: Deploy Backend

1. Click **Deploy** in Railway dashboard
2. Wait for build to complete (5-10 minutes)
3. Railway will provide a URL like: `https://your-app.railway.app`

### Step 6: Verify Backend Deployment

Test these endpoints:
- `https://your-app.railway.app/health` → Should return status
- `https://your-app.railway.app/automation/ai-status` → Check AI capabilities

---

## ⚡ Part 2: Frontend Deployment on Vercel

### Step 1: Prepare Frontend for Production

```bash
cd frontend

# Update package.json scripts
npm run build

# Create vercel.json
echo '{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "headers": {
        "cache-control": "public, max-age=31536000, immutable"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}' > vercel.json
```

### Step 2: Update Frontend Configuration

Update your React app's API configuration:

```javascript
// src/config.js
const config = {
  apiUrl: process.env.NODE_ENV === 'production' 
    ? 'https://your-app.railway.app'  // Your Railway backend URL
    : 'http://localhost:8000'
};

export default config;
```

### Step 3: Create Vercel Project

1. **Go to Vercel.com**
   - Visit https://vercel.com
   - Click "New Project"
   - Import from GitHub

2. **Configure Project**
   - Select your AI LAM repository
   - **Root Directory**: `frontend`
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### Step 4: Configure Environment Variables

In Vercel dashboard, add:

```env
REACT_APP_API_URL=https://your-app.railway.app
REACT_APP_ENVIRONMENT=production
```

### Step 5: Deploy Frontend

1. Click **Deploy**
2. Vercel will build and deploy automatically
3. Get your URL: `https://your-app.vercel.app`

---

## 🔗 Part 3: Connect Frontend to Backend

### Step 1: Update CORS Settings

In your backend `server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your Vercel URL
        "http://localhost:3000"        # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 2: Update Frontend API Calls

Update all API calls in your React app:

```javascript
// Example API call
const response = await fetch(`${config.apiUrl}/automation/create-session`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(data)
});
```

---

## 🛠️ Part 4: Custom Domain Setup (Optional)

### For Backend (Railway):
1. Go to Railway project → Settings → Domains
2. Add your custom domain (e.g., `api.yourapp.com`)
3. Update DNS CNAME record to point to Railway

### For Frontend (Vercel):
1. Go to Vercel project → Settings → Domains
2. Add your domain (e.g., `yourapp.com`)
3. Update DNS records as instructed

---

## 🚀 Part 5: Production Optimizations

### Backend Optimizations

1. **Update requirements.txt for production:**
```txt
# Add production optimizations
gunicorn==21.2.0
uvicorn[standard]==0.24.0
```

2. **Create Dockerfile (optional):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium

COPY . .
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Optimizations

1. **Enable gzip compression** (Vercel handles this automatically)
2. **Optimize images** in public folder
3. **Add error boundaries** for production

---

## 🔍 Part 6: Testing Deployment

### Test Backend:
```bash
# Health check
curl https://your-app.railway.app/health

# AI status
curl https://your-app.railway.app/automation/ai-status

# Create session (with auth)
curl -X POST https://your-app.railway.app/automation/create-session \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"target_url":"https://example.com","automation_type":"general"}'
```

### Test Frontend:
1. Visit `https://your-app.vercel.app`
2. Test user registration/login
3. Try file upload and automation creation
4. Check WebSocket connections work

---

## 🐛 Part 7: Troubleshooting

### Common Railway Issues:
- **Build fails**: Check requirements.txt and Python version
- **Playwright errors**: Ensure `playwright install chromium` in build
- **Port issues**: Use `$PORT` environment variable
- **Memory issues**: Upgrade Railway plan if needed

### Common Vercel Issues:
- **Build fails**: Check Node.js version and build command
- **API calls fail**: Verify CORS settings and API URL
- **Static files**: Ensure correct build output directory

### Environment Variable Issues:
- **Backend**: Check Railway Variables tab
- **Frontend**: Check Vercel Environment Variables
- **API Keys**: Ensure no spaces or quotes in values

---

## 🎯 Part 8: Monitoring & Maintenance

### Set up monitoring:
1. **Railway**: Built-in metrics and logs
2. **Vercel**: Analytics and function logs
3. **Supabase**: Database monitoring
4. **Gemini API**: Usage tracking in Google Cloud Console

### Regular maintenance:
1. Update dependencies monthly
2. Monitor API usage and costs
3. Check error logs regularly
4. Update AI model if newer versions available

---

## ✅ Deployment Checklist

- [ ] Backend deployed on Railway with all env vars
- [ ] Frontend deployed on Vercel with correct API URL
- [ ] CORS configured for production domains
- [ ] Database connection working
- [ ] AI/Gemini API functioning
- [ ] File uploads working
- [ ] WebSocket connections established
- [ ] Custom domains configured (optional)
- [ ] SSL certificates active
- [ ] Error monitoring setup

## 🎉 Your AI LAM is Live!

**Backend**: `https://your-app.railway.app`
**Frontend**: `https://your-app.vercel.app`

Your universal form automation platform is now live and ready to automate any website! 🚀 