# 🚀 AI LAM Deployment Guide

This guide covers deploying your AI University Application SaaS platform to production.

## 📋 Prerequisites

- GitHub account (for code hosting)
- Supabase account (database already configured)
- Domain name (optional, can use provided subdomains)

## 🎯 Recommended Deployment: Vercel + Railway

### **Frontend Deployment (Vercel)**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add deployment configurations"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign up with GitHub
   - Click "New Project" → Import your repository
   - Configure build settings:
     - **Framework Preset**: Create React App
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `build`

3. **Set Environment Variables** in Vercel:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   REACT_APP_SUPABASE_URL=your_supabase_url
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

### **Backend Deployment (Railway)**

1. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app) and sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Railway**:
   - Railway will auto-detect the `railway.toml` configuration
   - Add environment variables in Railway dashboard:
     ```
     JWT_SECRET=your_jwt_secret_here
     JWT_REFRESH_SECRET=your_jwt_refresh_secret_here
     SUPABASE_URL=your_supabase_url
     SUPABASE_SERVICE_KEY=your_supabase_service_key
     ENVIRONMENT=production
     ```

3. **Generate Custom Domain** (optional):
   - In Railway dashboard → Settings → Domain
   - Add custom domain or use provided railway.app subdomain

## 🔄 Alternative Deployment Options

### **Option 2: Netlify + Render**

**Frontend (Netlify)**:
1. Connect GitHub repo to Netlify
2. Build settings: `cd frontend && npm run build`
3. Publish directory: `frontend/build`

**Backend (Render)**:
1. Connect GitHub repo to Render
2. Use provided `render.yaml` configuration
3. Set environment variables in Render dashboard

### **Option 3: Full Cloud Platform (AWS/GCP/Azure)**

**AWS Example**:
- Frontend: S3 + CloudFront
- Backend: ECS Fargate or Lambda
- Database: Keep Supabase or migrate to RDS

## 🔐 Environment Variables Setup

### **Backend Variables**:
```env
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
JWT_REFRESH_SECRET=your-super-secret-refresh-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key

# Optional Services
STRIPE_SECRET_KEY=sk_test_... (for payments)
REDIS_URL=redis://... (for caching)
SENTRY_DSN=https://... (for error tracking)

# Application Settings
ENVIRONMENT=production
CORS_ORIGINS=["https://yourdomain.com"]
```

### **Frontend Variables**:
```env
REACT_APP_API_URL=https://your-backend-url
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-public-key
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_... (for payments)
```

## 🔒 Security Setup

### **Generate JWT Secrets**:
```python
import secrets
print("JWT_SECRET:", secrets.token_urlsafe(32))
print("JWT_REFRESH_SECRET:", secrets.token_urlsafe(32))
```

### **Supabase Configuration**:
1. Go to Supabase Dashboard → Settings → API
2. Copy your project URL and anon key
3. For backend, use the `service_role` key (keep secret!)

## 🌐 Domain & SSL Setup

### **Custom Domain**:
1. **Buy domain** from any registrar (Namecheap, GoDaddy, etc.)
2. **Configure DNS**:
   - Frontend: Point to Vercel/Netlify servers
   - Backend: Point to Railway/Render servers
3. **SSL certificates** are automatically provided by deployment platforms

### **Example DNS Configuration**:
```
Type    Name    Value
A       @       76.76.19.61 (Vercel IP)
CNAME   api     your-app.railway.app
CNAME   www     your-app.vercel.app
```

## 📊 Monitoring & Analytics

### **Application Monitoring**:
- **Sentry**: Error tracking and performance monitoring
- **LogRocket**: Session replay and debugging
- **DataDog**: Infrastructure monitoring

### **Business Analytics**:
- **Google Analytics**: Website traffic
- **Mixpanel**: User behavior tracking
- **Stripe Dashboard**: Payment analytics

## 🚀 CI/CD Pipeline

The included GitHub Actions workflow automatically:
- Runs tests on every push
- Deploys frontend to Vercel on main branch
- Deploys backend to Railway on main branch

### **Setup GitHub Secrets**:
```
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
RAILWAY_TOKEN=your_railway_token
```

## 💰 Cost Estimation

### **Starter Setup (~$5-15/month)**:
- Vercel: Free tier (can handle significant traffic)
- Railway: $5/month (512MB RAM, 1GB storage)
- Supabase: Free tier (500MB database, 50,000 monthly active users)

### **Growing Business (~$50-100/month)**:
- Vercel Pro: $20/month (advanced features)
- Railway: $20-50/month (more resources)
- Supabase Pro: $25/month (8GB database, 100,000 MAU)

### **Enterprise (~$200+/month)**:
- Custom infrastructure based on scale
- Dedicated database instances
- Advanced monitoring and support

## 🛠 Production Checklist

- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] Custom domain configured
- [ ] SSL certificates active
- [ ] Error monitoring setup (Sentry)
- [ ] Analytics configured
- [ ] Backup strategy implemented
- [ ] Performance monitoring active
- [ ] Security headers configured
- [ ] Rate limiting configured

## 🚨 Troubleshooting

### **Common Issues**:

1. **CORS Errors**:
   - Ensure `CORS_ORIGINS` includes your frontend domain
   - Check Supabase CORS settings

2. **Authentication Issues**:
   - Verify JWT secrets are consistent
   - Check Supabase RLS policies

3. **Build Failures**:
   - Ensure all dependencies are in `package.json`
   - Check Node.js version compatibility

4. **Database Connection**:
   - Verify Supabase URL and keys
   - Check network connectivity

## 📞 Support

- **Vercel**: [vercel.com/support](https://vercel.com/support)
- **Railway**: [help.railway.app](https://help.railway.app)
- **Supabase**: [supabase.com/docs](https://supabase.com/docs)

## 🔄 Next Steps

1. Deploy using recommended setup
2. Configure custom domain
3. Set up monitoring
4. Implement payment processing (Stripe)
5. Add email verification
6. Scale infrastructure as needed

---

**Ready to deploy?** Start with the Vercel + Railway setup for the fastest time to production! 🚀 