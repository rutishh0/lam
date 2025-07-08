# 🚀 Railway.com Deployment Guide for AI LAM

This guide covers deploying your AI University Application SaaS platform to Railway.com.

## 🎯 Why Railway.com?

Railway.com is an excellent choice for this project because it supports:
- ✅ **Python/Flask Applications**: Native support for Python web frameworks
- ✅ **WebSocket Connections**: Real-time communication for automation updates
- ✅ **Browser Automation**: Can run Playwright and headless browsers
- ✅ **Environment Variables**: Secure configuration management
- ✅ **Database Connections**: Works seamlessly with Supabase
- ✅ **Cost-Effective**: Starting at $5/month for hobby projects
- ✅ **Easy Deployment**: Git-based deployment with automatic builds
- ✅ **Scaling**: Automatic scaling based on demand

## 📋 Prerequisites

- GitHub account with your project repository
- Railway.com account (free tier available)
- Supabase account (database already configured)

## 🚢 Backend Deployment to Railway

### 1. **Create Railway Account and Project**

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your AI LAM repository
4. Railway will automatically detect the `railway.toml` configuration

### 2. **Configure Environment Variables**

In your Railway dashboard, add these environment variables:

```env
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-min-32-chars-production
JWT_REFRESH_SECRET=your-super-secret-refresh-key-min-32-chars-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Supabase Configuration
SUPABASE_URL=https://nwtzhzagqfuedsljngkl.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# Application Settings
ENVIRONMENT=production
PORT=8001
HOST=0.0.0.0

# CORS Configuration
CORS_ORIGINS=["https://your-frontend-domain.com"]

# Security
SECRET_KEY=your-super-secret-key-here
MASTER_KEY=your-master-encryption-key

# Browser Automation
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000

# Optional Services
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
SENDGRID_API_KEY=SG.your-sendgrid-api-key
SENTRY_DSN=https://your-sentry-dsn
```

### 3. **Custom Start Command**

The `railway.toml` file already contains the proper start command:
```toml
startCommand = "cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT"
```

### 4. **Deploy and Generate Domain**

1. Click **"Deploy"** in your Railway dashboard
2. Wait for the build to complete (usually 2-5 minutes)
3. Go to **Settings** → **Networking**
4. Click **"Generate Domain"** to get a public URL like `https://your-app.railway.app`

## 🌐 Frontend Deployment (Vercel)

### 1. **Deploy Frontend to Vercel**

1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click **"New Project"** → Import your repository
3. Configure build settings:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 2. **Set Frontend Environment Variables**

```env
REACT_APP_API_URL=https://your-app.railway.app
REACT_APP_SUPABASE_URL=https://nwtzhzagqfuedsljngkl.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🔧 Railway-Specific Optimizations

### **Browser Automation Support**

Railway supports Playwright, but you may need to:

1. **Install Browser Dependencies** (handled in requirements.txt):
```txt
playwright==1.40.0
playwright-python==1.40.0
```

2. **Use Nixpacks Builder** (configured in railway.toml):
```toml
[build]
builder = "nixpacks"
```

3. **Set Browser Path** (in environment variables):
```env
PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright
PLAYWRIGHT_HEADLESS=true
```

### **Memory and CPU Configuration**

Railway automatically allocates resources, but you can monitor usage:
- **Memory**: 512MB on hobby plan, up to 8GB on pro
- **CPU**: Shared on hobby, dedicated on pro
- **Disk**: 1GB persistent storage included

### **WebSocket Support**

Railway fully supports WebSocket connections:
- No additional configuration needed
- Works with your existing `/ws/automation/{session_id}` endpoints
- Supports real-time browser automation updates

## 📊 Cost Estimation

### **Hobby Plan (~$5-10/month)**
- 512MB RAM, shared CPU
- 1GB persistent storage
- Custom domain support
- Perfect for development and testing

### **Pro Plan (~$20-50/month)**
- Up to 8GB RAM, dedicated CPU
- 100GB persistent storage
- Priority support
- Better for production workloads

### **Team Plan (~$20+ per seat/month)**
- Collaboration features
- Multiple environments
- Advanced monitoring

## 🔐 Security Configuration

### **Generate JWT Secrets**
```python
import secrets
print("JWT_SECRET:", secrets.token_urlsafe(32))
print("JWT_REFRESH_SECRET:", secrets.token_urlsafe(32))
```

### **CORS Configuration**
Update your backend environment variables:
```env
CORS_ORIGINS=["https://your-vercel-app.vercel.app", "https://yourdomain.com"]
```

## 🚨 Troubleshooting

### **Common Issues and Solutions**

1. **Build Failures**
   - Check that `railway.toml` is in the root directory
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Playwright Browser Issues**
   - Ensure `PLAYWRIGHT_HEADLESS=true` is set
   - Check browser installation in logs
   - Verify memory allocation is sufficient

3. **Environment Variable Issues**
   - Double-check all required variables are set
   - Ensure no trailing spaces in values
   - Use Railway's environment variable validation

4. **WebSocket Connection Issues**
   - Verify WebSocket endpoint URLs
   - Check CORS configuration
   - Monitor connection logs in Railway dashboard

5. **Database Connection Issues**
   - Verify Supabase URLs and keys
   - Check network connectivity
   - Test connection with health endpoint

### **Debugging Steps**

1. **Check Railway Logs**:
   - Go to Railway dashboard → Deployments → View Logs
   - Look for startup errors or runtime issues

2. **Test Health Endpoint**:
   ```bash
   curl https://your-app.railway.app/health
   ```

3. **Monitor Resource Usage**:
   - Railway dashboard shows CPU/Memory usage
   - Upgrade plan if consistently hitting limits

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your main branch. To optimize:

1. **Use Branch Deployments**:
   - Create separate Railway services for staging/production
   - Connect different branches to different services

2. **Environment Management**:
   - Use Railway's environment variables for different stages
   - Consider using Railway's template system for team deployments

## 📈 Monitoring and Analytics

### **Railway Built-in Monitoring**
- CPU and memory usage graphs
- Request/response monitoring
- Error rate tracking
- Deployment history

### **External Monitoring** (Optional)
- **Sentry**: For error tracking
- **LogRocket**: For session replay
- **DataDog**: For advanced metrics

## 🎯 Production Readiness

### **Pre-Launch Checklist**
- [ ] All environment variables configured
- [ ] Custom domain connected (optional)
- [ ] SSL certificate verified
- [ ] Health checks passing
- [ ] Browser automation tested
- [ ] WebSocket connections working
- [ ] Database connections verified
- [ ] Error monitoring configured
- [ ] Backup strategy implemented

### **Performance Optimization**
- [ ] Enable Railway's built-in caching
- [ ] Optimize Playwright browser settings
- [ ] Monitor memory usage during automation
- [ ] Set up appropriate rate limiting

## 🌟 Railway vs Other Platforms

| Feature | Railway | Heroku | GCP Cloud Run | Render |
|---------|---------|---------|---------------|---------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Python Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **WebSocket Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Browser Automation** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cost** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Scaling** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 📞 Support and Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Active community support
- **Railway Status**: [status.railway.app](https://status.railway.app)
- **Railway Blog**: Latest updates and tutorials

---

**🎉 Result**: Your AI automation backend will be running on Railway with full browser automation support, real-time WebSocket updates, and seamless Supabase integration! 