# 🚀 Enhanced Eko Automation Deployment Guide

## Overview

This guide covers deploying your **Elevate Ed** platform with the new **multi-browser Eko automation** capabilities. The enhanced system requires specific infrastructure to support multiple browser sessions and Node.js integration.

## 🏗️ Architecture Overview

```
Production Environment:
┌─────────────────────────────────────────────────────────────┐
│                     Load Balancer                          │
│                    (Cloudflare/AWS ALB)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (React)                         │
│              Vercel / Netlify / AWS S3                     │
│         - EnhancedEkoPanel.js                             │
│         - Multi-browser UI components                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ API Calls
┌─────────────────────────────────────────────────────────────┐
│                Backend (Python FastAPI)                    │
│            Railway / AWS EC2 / Digital Ocean               │
│         - Enhanced Eko Automation Service                  │
│         - Multi-browser session management                 │
│         - Node.js subprocess integration                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Database Layer                           │
│              Supabase / PostgreSQL                         │
│         - Session tracking                                 │
│         - Workflow history                                 │
│         - Performance metrics                              │
└─────────────────────────────────────────────────────────────┘
```

## 🖥️ Backend Deployment

### **Option 1: Railway (Recommended)**

Railway is perfect for your enhanced backend because it supports both Python and Node.js in the same environment.

#### **1. Setup Railway Project**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
cd backend
railway init
```

#### **2. Configure Railway Environment**
```bash
# Add environment variables
railway variables set ANTHROPIC_API_KEY=your_anthropic_key
railway variables set OPENAI_API_KEY=your_openai_key
railway variables set SUPABASE_URL=your_supabase_url
railway variables set SUPABASE_KEY=your_supabase_key
railway variables set NODE_ENV=production
```

#### **3. Create Railway Configuration**
```toml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python server.py"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"

[[services]]
name = "enhanced-eko-backend"

[services.variables]
PORT = "8000"
PYTHONPATH = "."
```

#### **4. Update Requirements**
```txt
# requirements.txt - Add these new dependencies
fastapi==0.104.1
uvicorn==0.24.0
asyncio
subprocess
playwright==1.40.0
nodejs>=18.0.0

# Existing dependencies...
supabase
python-multipart
python-jose[cryptography]
passlib[bcrypt]
```

#### **5. Deploy to Railway**
```bash
# Deploy
railway up

# Monitor deployment
railway logs

# Get deployment URL
railway status
```

### **Option 2: AWS EC2 (For Advanced Users)**

For maximum control and scalability.

#### **1. Launch EC2 Instance**
```bash
# Amazon Linux 2 instance (t3.large or larger for multi-browser)
# Install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip nodejs npm git

# Install Chrome for Playwright
sudo yum install -y google-chrome-stable
```

#### **2. Setup Application**
```bash
# Clone your repository
git clone https://github.com/yourusername/elevate-ed.git
cd elevate-ed/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for Eko
cd services/eko_scripts
npm install @eko-ai/eko @eko-ai/eko-nodejs playwright
npx playwright install chromium

# Return to backend root
cd ../..
```

#### **3. Create Systemd Service**
```ini
# /etc/systemd/system/elevate-ed.service
[Unit]
Description=Elevate Ed Enhanced Backend
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/elevate-ed/backend
Environment=PATH=/home/ec2-user/elevate-ed/backend/venv/bin
Environment=PYTHONPATH=/home/ec2-user/elevate-ed/backend
Environment=NODE_PATH=/home/ec2-user/elevate-ed/backend/services/eko_scripts/node_modules
ExecStart=/home/ec2-user/elevate-ed/backend/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **4. Configure Nginx**
```nginx
# /etc/nginx/sites-available/elevate-ed
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for real-time updates
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### **Option 3: Digital Ocean Droplet**

Cost-effective option with good performance.

#### **1. Create Droplet**
```bash
# Ubuntu 22.04 LTS, 4GB RAM minimum for multi-browser
# Add your SSH key during creation

# Connect and setup
ssh root@your-droplet-ip
```

#### **2. Install Dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Python and Node.js
apt install -y python3 python3-pip python3-venv nodejs npm git nginx

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt update
apt install -y google-chrome-stable
```

#### **3. Deploy Application**
```bash
# Clone and setup (similar to EC2 steps above)
git clone https://github.com/yourusername/elevate-ed.git
cd elevate-ed/backend

# Setup virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Eko and Playwright
cd services/eko_scripts
npm install @eko-ai/eko @eko-ai/eko-nodejs playwright
npx playwright install chromium
```

## 🌐 Frontend Deployment

### **Option 1 : Vercel (Recommended)**

Perfect for React applications with excellent performance and easy deployment.

#### **1. Prepare Frontend**
```bash
cd frontend

# Install dependencies
npm install

# Add environment variables to .env.production
echo "REACT_APP_API_URL=https://your-backend-url.com" > .env.production
echo "REACT_APP_SUPABASE_URL=your_supabase_url" >> .env.production
echo "REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key" >> .env.production
```

#### **2. Deploy to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Set root directory to 'frontend'
# - Override build command: npm run build
# - Override output directory: build
```

#### **3. Configure Environment Variables**
```bash
# In Vercel dashboard or via CLI
vercel env add REACT_APP_API_URL production
vercel env add REACT_APP_SUPABASE_URL production
vercel env add REACT_APP_SUPABASE_ANON_KEY production

# Redeploy with new environment variables
vercel --prod
```

### **Option 2: Netlify**

Alternative to Vercel with similar features.

#### **1. Build Configuration**
```toml
# netlify.toml
[build]
  base = "frontend/"
  publish = "frontend/build"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### **2. Deploy**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
cd frontend
npm run build
netlify deploy --prod --dir=build
```

### **Option 3: AWS S3 + CloudFront**

For enterprise-grade hosting with CDN.

#### **1. Build Application**
```bash
cd frontend
npm run build
```

#### **2. Create S3 Bucket**
```bash
# Create bucket
aws s3 mb s3://elevate-ed-frontend

# Upload files
aws s3 sync build/ s3://elevate-ed-frontend --delete

# Configure bucket for static hosting
aws s3 website s3://elevate-ed-frontend --index-document index.html --error-document index.html
```

#### **3. Setup CloudFront**
```bash
# Create CloudFront distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

## 🔧 Environment Configuration

### **Backend Environment Variables**
```bash
# Core API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://user:pass@host:port/db

# Security
JWT_SECRET=your_jwt_secret_key
ENCRYPTION_KEY=your_encryption_key

# Eko Configuration
EKO_MAX_CONCURRENT_SESSIONS=10
EKO_SESSION_TIMEOUT=3600
EKO_BROWSER_HEADLESS=true

# Performance
UVICORN_WORKERS=4
MAX_BROWSER_INSTANCES=10
BROWSER_MEMORY_LIMIT=2048

# Monitoring
SENTRY_DSN=your_sentry_dsn  # Optional
LOG_LEVEL=INFO
```

### **Frontend Environment Variables**
```bash
# API Configuration
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_WS_URL=wss://your-backend-url.com

# Supabase
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key

# Features
REACT_APP_ENABLE_ENHANCED_EKO=true
REACT_APP_MAX_PARALLEL_APPLICATIONS=5

# Analytics (Optional)
REACT_APP_GOOGLE_ANALYTICS_ID=your_ga_id
REACT_APP_SENTRY_DSN=your_sentry_dsn
```

## 📦 Complete Deployment Script

Create this script for automated deployment:

```bash
#!/bin/bash
# deploy.sh - Complete deployment script

set -e

echo "🚀 Deploying Enhanced Elevate Ed Platform..."

# Backend Deployment
echo "📦 Deploying Backend..."
cd backend

# Install dependencies
pip install -r requirements.txt

# Install Node.js dependencies for Eko
cd services/eko_scripts
npm install @eko-ai/eko @eko-ai/eko-nodejs playwright
npx playwright install chromium

# Deploy backend (Railway example)
cd ../..
railway up

# Frontend Deployment
echo "🌐 Deploying Frontend..."
cd ../frontend

# Install dependencies
npm install

# Build application
npm run build

# Deploy to Vercel
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Frontend: https://your-app.vercel.app"
echo "🔗 Backend: https://your-app.railway.app"
```

## 🔍 Post-Deployment Verification

### **1. Health Checks**
```bash
# Backend health
curl https://your-backend-url.com/health
curl https://your-backend-url.com/api/eko-enhanced/health-enhanced

# Frontend access
curl https://your-frontend-url.com
```

### **2. Enhanced Eko Functionality**
```bash
# Test enhanced Eko initialization
curl -X POST https://your-backend-url.com/api/eko-enhanced/initialize-enhanced \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json"

# Test session creation
curl -X POST https://your-backend-url.com/api/eko-enhanced/browser-session/create \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{"session_type": "isolated", "headless": true}'
```

### **3. Performance Monitoring**
```bash
# Monitor resource usage
htop  # or your preferred monitoring tool

# Check browser processes
ps aux | grep chrome

# Monitor logs
tail -f /var/log/your-app.log
```

## 🛡️ Security Considerations

### **1. API Security**
```python
# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/eko-enhanced/applications/parallel")
@limiter.limit("5/minute")  # Limit parallel processing requests
async def process_parallel_applications(...):
    pass
```

### **2. Browser Security**
```python
# Secure browser options
browser_options = {
    "args": [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",  # Optional: for performance
        "--disable-javascript",  # Only if not needed
    ]
}
```

### **3. Network Security**
```nginx
# Nginx security headers
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## 📊 Monitoring & Scaling

### **1. Application Monitoring**
```python
# Add to your backend
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your_sentry_dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

### **2. Resource Monitoring**
```bash
# Setup monitoring alerts
# - CPU usage > 80%
# - Memory usage > 85%
# - Browser session count > 8
# - API response time > 30s
```

### **3. Auto-scaling Configuration**
```yaml
# For Kubernetes/Docker deployment
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: elevate-ed-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: elevate-ed-backend
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## 🎯 Recommended Deployment Strategy

### **Phase 1: Development/Testing**
- **Backend**: Railway (easy setup, Node.js support)
- **Frontend**: Vercel (fast deployment, preview branches)
- **Database**: Supabase (managed PostgreSQL)

### **Phase 2: Production/Scale**
- **Backend**: AWS EC2 with Auto Scaling Group
- **Frontend**: AWS S3 + CloudFront
- **Database**: AWS RDS PostgreSQL
- **Load Balancer**: AWS Application Load Balancer
- **Monitoring**: AWS CloudWatch + Sentry

### **Phase 3: Enterprise**
- **Backend**: Kubernetes on AWS EKS
- **Frontend**: Multi-region deployment
- **Database**: AWS Aurora PostgreSQL
- **Caching**: Redis cluster
- **CDN**: CloudFlare Enterprise

## 🔗 Quick Start Commands

```bash
# 1. Clone repository
git clone https://github.com/yourusername/elevate-ed.git
cd elevate-ed

# 2. Deploy backend to Railway
cd backend
railway init
railway up

# 3. Deploy frontend to Vercel
cd ../frontend
vercel

# 4. Configure environment variables
# Set all required environment variables in Railway and Vercel dashboards

# 5. Test deployment
curl https://your-backend.railway.app/health
curl https://your-frontend.vercel.app
```

## ✅ Deployment Checklist

- [ ] Backend deployed with enhanced Eko services
- [ ] Frontend deployed with EnhancedEkoPanel
- [ ] Environment variables configured
- [ ] Node.js and Playwright installed
- [ ] Browser binaries available
- [ ] API endpoints responding
- [ ] Enhanced Eko initialization working
- [ ] Multi-browser session creation functional
- [ ] SSL certificates configured
- [ ] Monitoring and logging setup
- [ ] Performance testing completed

Your **Enhanced Eko Automation** platform is now ready for production! 🚀 