# 🚀 AI Automation Backend - GCP Deployment Guide

This guide will help you deploy your AI automation backend to Google Cloud Platform with **real browser automation** using Playwright.

## 🎯 Why GCP?

- ✅ **Linux Environment**: Playwright works perfectly on Linux
- ✅ **Serverless**: Cloud Run scales automatically 
- ✅ **Real Browser Automation**: Full Chromium, Firefox, WebKit support
- ✅ **Production Ready**: Enterprise-grade infrastructure

## 📋 Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed locally (optional)
4. **Supabase** project configured

## 🔧 Step 1: Setup GCP Project

```bash
# Install gcloud CLI (if not installed)
# https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create your-ai-automation-project
gcloud config set project your-ai-automation-project

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

## ⚙️ Step 2: Configure Environment

1. **Update Project Configuration**:
   ```bash
   # Edit deploy-to-gcp.sh
   PROJECT_ID="your-ai-automation-project"  # Your actual project ID
   REGION="us-central1"                     # Or your preferred region
   ```

2. **Set up Environment Variables** (in GCP Console or via CLI):
   ```bash
   # Required environment variables for production
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-service-role-key
   SECRET_KEY=your-super-secret-key
   MASTER_KEY=your-master-encryption-key
   ENVIRONMENT=production
   ```

## 🚢 Step 3: Deploy to Cloud Run

### Option A: Automated Deployment (Recommended)

```bash
# Make the script executable
chmod +x deploy-to-gcp.sh

# Run the deployment script
./deploy-to-gcp.sh
```

### Option B: Manual Deployment

```bash
# 1. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 2. Build with Cloud Build
gcloud builds submit --config cloudbuild.yaml

# 3. Deploy to Cloud Run
gcloud run deploy ai-automation-backend \
    --image gcr.io/your-project-id/ai-automation-backend:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8001 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 900 \
    --max-instances 10
```

## 🔗 Step 4: Update Frontend Configuration

Update your frontend to use the new GCP backend:

```javascript
// In your frontend/.env
REACT_APP_BACKEND_URL=https://your-service-url.run.app
```

## 🧪 Step 5: Test Your Deployment

1. **Health Check**:
   ```bash
   curl https://your-service-url.run.app/health
   ```

2. **Test Automation Endpoints**:
   ```bash
   # Create automation session
   curl -X POST "https://your-service-url.run.app/api/admin/automation/sessions/create" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"client_id": "test", "university_name": "Oxford"}'

   # Get sessions
   curl "https://your-service-url.run.app/api/admin/automation/sessions" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Test WebSocket**:
   ```javascript
   const ws = new WebSocket('wss://your-service-url.run.app/ws/automation/session-id');
   ```

## 🎛 Step 6: Monitor and Scale

### Viewing Logs
```bash
# View real-time logs
gcloud logs tail --service=ai-automation-backend

# View specific logs
gcloud logs read --service=ai-automation-backend --limit=50
```

### Scaling Configuration
```bash
# Update scaling settings
gcloud run services update ai-automation-backend \
    --min-instances=1 \
    --max-instances=20 \
    --concurrency=10
```

### Resource Monitoring
- Visit: https://console.cloud.google.com/run
- Monitor CPU, Memory, and Request metrics
- Set up alerts for errors or high usage

## 🔒 Step 7: Security Best Practices

1. **Environment Variables**: Store sensitive data in Secret Manager
   ```bash
   # Create secrets
   echo "your-supabase-key" | gcloud secrets create supabase-key --data-file=-
   
   # Reference in Cloud Run
   gcloud run services update ai-automation-backend \
     --set-env-vars="SUPABASE_KEY=[supabase-key]"
   ```

2. **Authentication**: Configure IAM for API access
3. **CORS**: Update CORS origins for production domains
4. **Rate Limiting**: Implement rate limiting for automation endpoints

## 💰 Cost Optimization

- **Cloud Run Pricing**: Pay per request, scales to zero
- **Estimated Costs**:
  - Small usage: $5-20/month
  - Medium usage: $20-100/month
  - High usage: $100+/month

## 🚨 Troubleshooting

### Common Issues:

1. **Playwright Browser Launch Fails**:
   ```bash
   # Check logs for browser errors
   gcloud logs read --service=ai-automation-backend --filter="playwright"
   ```

2. **Memory Issues**:
   ```bash
   # Increase memory allocation
   gcloud run services update ai-automation-backend --memory=4Gi
   ```

3. **Timeout Issues**:
   ```bash
   # Increase timeout
   gcloud run services update ai-automation-backend --timeout=1800
   ```

4. **WebSocket Connection Issues**:
   - Ensure Cloud Run supports WebSockets (it does!)
   - Check CORS configuration
   - Verify WebSocket URL format

## 🎉 Success Indicators

After successful deployment, you should see:

- ✅ Health endpoint returns `{"status": "healthy"}`
- ✅ Browser automation initializes without errors
- ✅ Screenshots capture real browser content
- ✅ WebSocket connections work from admin panel
- ✅ No "Mock Mode" messages in logs

## 🔄 Continuous Deployment

For automated deployments, set up GitHub Actions or Cloud Build triggers:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GCP
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Cloud Run
        run: gcloud builds submit --config cloudbuild.yaml
```

## 📞 Support

If you encounter issues:
1. Check the logs: `gcloud logs read --service=ai-automation-backend`
2. Verify environment variables are set correctly
3. Test locally with Docker first
4. Check GCP quotas and billing

---

**🎯 Result**: Your AI automation backend will be running on GCP with **real browser automation**, supporting multiple concurrent sessions with live WebSocket updates and screenshot streaming! 