# 🚀 Quick Deployment Guide

## Deployment Order (Important!)

### 1. Deploy Backend First (Railway)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the `railway.toml` configuration

**Add these environment variables in Railway:**
```bash
JWT_SECRET=your-32-char-secret-key
JWT_REFRESH_SECRET=your-32-char-refresh-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
ENVIRONMENT=production
```

**Generate JWT secrets:**
```python
import secrets
print("JWT_SECRET:", secrets.token_urlsafe(32))
print("JWT_REFRESH_SECRET:", secrets.token_urlsafe(32))
```

6. Deploy and get your Railway app URL (e.g., `https://your-app.railway.app`)

### 2. Deploy Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project" → Import your repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

**Add these environment variables in Vercel:**
```bash
REACT_APP_API_URL=https://your-app.railway.app
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key
```

## 🔑 Getting Your Values

### Supabase Values:
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to Settings → API
4. Copy:
   - **Project URL** → `SUPABASE_URL` 
   - **anon public key** → `REACT_APP_SUPABASE_ANON_KEY`
   - **service_role secret key** → `SUPABASE_SERVICE_KEY` (backend only)

### JWT Secrets:
Generate secure random strings (32+ characters):
```bash
# Option 1: Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: OpenSSL
openssl rand -base64 32

# Option 3: Online generator
# Visit: https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx
```

## ✅ Final Checklist

- [ ] Backend deployed to Railway with environment variables
- [ ] Frontend deployed to Vercel with environment variables
- [ ] Supabase database schema applied (setup.sql)
- [ ] JWT secrets generated and configured
- [ ] API URL updated in frontend environment
- [ ] Test login/registration functionality
- [ ] Test application creation workflow

## 🔧 Troubleshooting

**Common Issues:**

1. **CORS Errors**: Update `CORS_ORIGINS` in backend environment
2. **Database Connection**: Verify Supabase keys and URL
3. **Authentication Fails**: Check JWT secrets match between environments
4. **Frontend Can't Reach Backend**: Verify API URL is correct

**Test Your Deployment:**
1. Visit your Vercel URL
2. Try to register a new account
3. Check if you can login
4. Verify the dashboard loads correctly 