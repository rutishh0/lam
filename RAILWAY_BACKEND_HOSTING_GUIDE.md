# 🚀 Complete Guide: Hosting AI LAM Backend on Railway.com

This is a comprehensive, step-by-step guide to deploy your AI LAM backend automation system to Railway.com. Follow this guide exactly and you'll have your backend running in production within 30 minutes.

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] ✅ GitHub account with your AI LAM project pushed
- [ ] ✅ Railway.com account (free tier available)
- [ ] ✅ Supabase project set up with database configured
- [ ] ✅ Environment variables ready (JWT secrets, Supabase keys, etc.)

## 🔑 Step 1: Prepare Your Environment Variables

### **Generate Required Secrets**

First, generate your JWT secrets:

```python
# Run this Python script to generate secure secrets
import secrets

print("JWT_SECRET:", secrets.token_urlsafe(32))
print("JWT_REFRESH_SECRET:", secrets.token_urlsafe(32))
print("SECRET_KEY:", secrets.token_urlsafe(32))
print("MASTER_KEY:", secrets.token_urlsafe(32))
```

### **Gather Supabase Credentials**

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** → **API**
4. Copy these values:
   - Project URL
   - `anon` public key
   - `service_role` secret key

### **Complete Environment Variables List**

Prepare these environment variables (you'll add them to Railway):

```env
# === REQUIRED VARIABLES ===

# JWT Configuration
JWT_SECRET=<your-generated-jwt-secret>
JWT_REFRESH_SECRET=<your-generated-refresh-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Supabase Configuration  
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_KEY=<your-supabase-service-role-key>

# Application Settings
ENVIRONMENT=production
PORT=8001
HOST=0.0.0.0

# Security
SECRET_KEY=<your-generated-secret-key>
MASTER_KEY=<your-generated-master-key>

# Browser Automation
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000

# CORS Configuration (update after frontend deployment)
CORS_ORIGINS=["https://your-frontend-domain.com", "http://localhost:3000"]

# === OPTIONAL VARIABLES ===

# Stripe (for payments)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email Service (SendGrid)
SENDGRID_API_KEY=SG.your-sendgrid-api-key

# SMS Service (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Monitoring (Sentry)
SENTRY_DSN=https://your-sentry-dsn

# Caching (Redis)
REDIS_URL=redis://your-redis-instance-url

# Feature Flags
ENABLE_EMAIL_VERIFICATION=false
ENABLE_SMS_NOTIFICATIONS=false
ENABLE_RATE_LIMITING=true
ENABLE_CACHING=false

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=structured
```

## 🚢 Step 2: Deploy to Railway

### **2.1 Create Railway Account**

1. Go to [railway.app](https://railway.app)
2. Click **"Sign up"**
3. Choose **"Continue with GitHub"** (recommended)
4. Authorize Railway to access your GitHub account

### **2.2 Create New Project**

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select your **AI LAM repository**
4. Railway will automatically start analyzing your project

### **2.3 Configure Project Settings**

Railway should automatically detect your Python project and the `railway.toml` configuration file. If not:

1. Go to **Settings** tab in your Railway project
2. Under **Build**, ensure:
   - **Builder**: Nixpacks (auto-detected)
   - **Root Directory**: `/` (leave empty for root)
3. Under **Deploy**, verify:
   - **Start Command**: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`

## 🔧 Step 3: Configure Environment Variables

### **3.1 Add Environment Variables**

1. In your Railway project, go to the **Variables** tab
2. Click **"New Variable"** for each environment variable
3. Add **all the required variables** from Step 1

**Pro Tip**: Use the **Raw Editor** for faster bulk entry:
1. Click **"Raw Editor"** in the Variables tab
2. Paste all your environment variables at once:

```
JWT_SECRET=your-jwt-secret-here
JWT_REFRESH_SECRET=your-refresh-secret-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here
ENVIRONMENT=production
PORT=8001
HOST=0.0.0.0
SECRET_KEY=your-secret-key
MASTER_KEY=your-master-key
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000
CORS_ORIGINS=["http://localhost:3000"]
```

3. Click **"Update Variables"**

### **3.2 Verify Configuration**

Double-check these critical variables are set correctly:
- ✅ `SUPABASE_URL` - Must match your Supabase project URL exactly
- ✅ `SUPABASE_SERVICE_KEY` - Must be the service role key (not anon key)
- ✅ `JWT_SECRET` - Must be at least 32 characters
- ✅ `PLAYWRIGHT_HEADLESS=true` - Required for production
- ✅ `PORT=8001` - Must match your FastAPI configuration

## 🚀 Step 4: Deploy and Monitor

### **4.1 Trigger Deployment**

1. Go to the **Deployments** tab
2. Click **"Deploy"** (if not already deploying)
3. Watch the build logs in real-time

**Expected Build Process:**
```
⠹ Building with Nixpacks
⠸ Installing Python dependencies
⠼ Installing Playwright browsers
⠦ Setting up environment
⠧ Starting application
✅ Build completed successfully
✅ Deployment ready
```

### **4.2 Monitor Build Logs**

Watch for these key indicators:

**✅ Good Signs:**
- `Successfully installed packages from requirements.txt`
- `Playwright browsers installed successfully`
- `FastAPI application startup complete`
- `Uvicorn running on 0.0.0.0:8001`

**❌ Warning Signs:**
- `ModuleNotFoundError` - Missing dependencies
- `Connection refused` - Database connection issues
- `Permission denied` - Environment variable issues
- `Memory allocation failed` - Insufficient resources

### **4.3 Verify Deployment**

1. Once deployment shows "✅ Success", go to **Settings** → **Networking**
2. Click **"Generate Domain"** to get a public URL
3. Your backend will be available at: `https://your-app-name.railway.app`

## ✅ Step 5: Test Your Deployment

### **5.1 Health Check Test**

Test your backend health endpoint:

```bash
curl https://your-app-name.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "database": "connected",
    "api": "running"
  },
  "version": "2.0.0"
}
```

### **5.2 API Documentation Test**

Visit your interactive API documentation:
```
https://your-app-name.railway.app/docs
```

You should see the FastAPI Swagger UI with all your endpoints.

### **5.3 Database Connection Test**

Test a simple API endpoint that requires database access:

```bash
curl https://your-app-name.railway.app/api/universities
```

Should return a list of universities without authentication errors.

### **5.4 WebSocket Test**

Test WebSocket connectivity (from browser console):

```javascript
const ws = new WebSocket('wss://your-app-name.railway.app/ws/automation/test-session');
ws.onopen = () => console.log('WebSocket connected!');
ws.onmessage = (event) => console.log('Message:', event.data);
ws.onerror = (error) => console.error('WebSocket error:', error);
```

## 🔧 Step 6: Optimization and Configuration

### **6.1 Performance Tuning**

#### **Memory Settings:**
Your app should work fine on Railway's default 512MB, but for heavy browser automation:

1. Go to **Settings** → **Resources**
2. If using Pro plan, consider upgrading to 1GB+ RAM for better performance

#### **Timeout Configuration:**
```env
# Add these to your environment variables if needed
UVICORN_TIMEOUT_KEEP_ALIVE=5
UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN=30
```

### **6.2 Browser Automation Optimization**

For optimal Playwright performance on Railway:

```env
# Already configured in your environment
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true

# Additional optimizations you can add:
PLAYWRIGHT_BROWSER_EXECUTABLE_PATH=/usr/lib/playwright/chromium-*/chrome-linux/chrome
PLAYWRIGHT_SKIP_DOWNLOAD=true
PLAYWRIGHT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage,--disable-gpu
```

### **6.3 Security Hardening**

1. **Update CORS Origins:**
   ```env
   CORS_ORIGINS=["https://your-frontend-domain.com", "https://your-app-name.railway.app"]
   ```

2. **Enable Rate Limiting:**
   ```env
   ENABLE_RATE_LIMITING=true
   ```

3. **Configure Secure Headers:**
   Your FastAPI app already includes security middleware.

## 🔄 Step 7: Custom Domain (Optional)

### **7.1 Add Custom Domain**

1. In Railway project, go to **Settings** → **Networking**
2. Click **"Custom Domain"**
3. Enter your domain: `api.yourdomain.com`
4. Railway provides DNS instructions

### **7.2 DNS Configuration**

Add this CNAME record to your domain DNS:
```
Type: CNAME
Name: api
Value: your-app-name.railway.app
TTL: 300
```

SSL certificates are automatically handled by Railway.

## 🚨 Troubleshooting Guide

### **Common Issues and Solutions**

#### **Issue 1: Build Fails - Dependencies Error**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
1. Check `backend/requirements.txt` exists
2. Verify Python version compatibility
3. Update requirements:
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

#### **Issue 2: Database Connection Failed**
```
Connection to database failed
```

**Solutions:**
1. Verify `SUPABASE_URL` format: `https://project-id.supabase.co`
2. Check `SUPABASE_SERVICE_KEY` is the service role key (not anon key)
3. Test connection from your local machine first
4. Verify Supabase project is active

#### **Issue 3: Playwright Browser Launch Failed**
```
browserType.launch: Executable doesn't exist
```

**Solutions:**
1. Ensure `PLAYWRIGHT_HEADLESS=true`
2. Add environment variable: `PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright`
3. Check Railway build logs for browser installation errors

#### **Issue 4: Port Binding Error**
```
Address already in use
```

**Solution:**
1. Ensure `PORT=8001` in environment variables
2. Verify start command uses `$PORT`: `uvicorn server:app --host 0.0.0.0 --port $PORT`

#### **Issue 5: Memory Issues**
```
Process killed (OOM - Out of Memory)
```

**Solutions:**
1. Upgrade to Railway Pro plan for more memory
2. Optimize browser automation to use less memory
3. Implement browser instance pooling

### **Advanced Debugging**

#### **Access Railway Logs:**
1. Go to your Railway project
2. Click **Deployments** → Select latest deployment
3. Click **View Logs** to see real-time logs

#### **Test Locally First:**
Before deploying to Railway, always test locally:
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001
```

#### **Check Resource Usage:**
Monitor your app's resource usage in Railway dashboard:
- CPU usage should be < 80%
- Memory usage should be < 85%
- Response times should be < 2 seconds

## 📊 Monitoring and Maintenance

### **Railway Built-in Monitoring**

Railway provides excellent monitoring out of the box:

1. **Deployment History**: Track all deployments and rollbacks
2. **Resource Usage**: Monitor CPU, Memory, and Network usage
3. **Logs**: Real-time application logs with search and filtering
4. **Metrics**: Request/response times, error rates
5. **Alerts**: Get notified of deployment failures or resource issues

### **Custom Monitoring Setup**

Your backend includes built-in monitoring endpoints:

```bash
# System health
curl https://your-app-name.railway.app/health

# Admin system stats (requires authentication)
curl https://your-app-name.railway.app/api/admin/stats \
  -H "Authorization: Bearer your-jwt-token"

# Performance metrics
curl https://your-app-name.railway.app/api/admin/performance \
  -H "Authorization: Bearer your-jwt-token"
```

### **External Monitoring (Optional)**

For production, consider adding:

1. **Sentry** (Error Tracking):
   ```env
   SENTRY_DSN=https://your-sentry-dsn
   ```

2. **Uptime Monitoring**:
   - UptimeRobot: Monitor your `/health` endpoint
   - Better Uptime: More advanced monitoring

## 🎯 Production Checklist

Before going live, ensure:

### **Security Checklist:**
- [ ] ✅ All JWT secrets are strong (32+ characters)
- [ ] ✅ Database credentials are secure
- [ ] ✅ CORS origins are properly configured
- [ ] ✅ Rate limiting is enabled
- [ ] ✅ HTTPS is working (automatic with Railway)
- [ ] ✅ Environment variables don't contain test data

### **Performance Checklist:**
- [ ] ✅ Health endpoint responds quickly (< 1 second)
- [ ] ✅ Database queries are optimized
- [ ] ✅ Browser automation works without errors
- [ ] ✅ WebSocket connections are stable
- [ ] ✅ Memory usage is under 80%

### **Functionality Checklist:**
- [ ] ✅ User registration works
- [ ] ✅ User authentication works
- [ ] ✅ Admin panel is accessible
- [ ] ✅ Browser automation sessions can be created
- [ ] ✅ Real-time updates work via WebSockets
- [ ] ✅ File uploads work properly
- [ ] ✅ Email notifications work (if configured)

## 🔄 Continuous Deployment

### **Automatic Deployments**

Railway automatically deploys when you push to your main branch:

1. **Make changes** to your code locally
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update backend features"
   git push origin main
   ```
3. **Railway automatically deploys** your changes
4. **Monitor deployment** in Railway dashboard

### **Deployment Best Practices**

1. **Use Branch Protection:**
   - Set up branch protection rules on GitHub
   - Require pull requests for main branch

2. **Test Before Deploying:**
   - Always test changes locally first
   - Consider setting up a staging environment

3. **Environment-Specific Configs:**
   - Use different environment variables for staging/production
   - Consider using Railway's template system for team deployments

## 💰 Cost Management

### **Railway Pricing Tiers**

**Hobby Plan ($5/month):**
- 512MB RAM, Shared CPU
- 1GB Disk Storage  
- 100GB Bandwidth
- Perfect for development and light production

**Pro Plan ($20+/month):**
- Up to 8GB RAM, Dedicated CPU
- 100GB Disk Storage
- 100GB+ Bandwidth
- Priority support

### **Cost Optimization Tips**

1. **Monitor Resource Usage:**
   - Keep an eye on CPU and memory usage
   - Optimize code to use fewer resources

2. **Efficient Browser Automation:**
   - Close browsers when not needed
   - Implement browser instance pooling
   - Use headless mode always in production

3. **Database Optimization:**
   - Index frequently queried fields
   - Implement caching where appropriate
   - Clean up old data regularly

## 🎉 Success! Your Backend is Live

Congratulations! Your AI LAM backend is now running on Railway.com with:

✅ **Full browser automation capabilities**  
✅ **Real-time WebSocket communication**  
✅ **Secure authentication and authorization**  
✅ **Supabase database integration**  
✅ **Production-ready monitoring**  
✅ **Automatic scaling and high availability**  

### **What's Next?**

1. **Deploy your frontend** to Vercel (see `DEPLOYMENT.md`)
2. **Set up custom domain** (optional)
3. **Configure additional services** (email, SMS, payments)
4. **Monitor performance** and optimize as needed
5. **Scale up resources** as your user base grows

### **Important URLs to Save:**

- **Backend API**: `https://your-app-name.railway.app`
- **API Documentation**: `https://your-app-name.railway.app/docs`
- **Health Check**: `https://your-app-name.railway.app/health`
- **Railway Dashboard**: `https://railway.app/project/your-project-id`

### **Support Resources:**

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Railway Status**: [status.railway.app](https://status.railway.app)

---

**🚀 Your AI LAM backend is now powering university applications from the cloud!**

Need help with any specific step? Just ask! 