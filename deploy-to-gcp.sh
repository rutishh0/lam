#!/bin/bash

# GCP Deployment Script for AI Automation Backend
set -e

# Configuration - Update these values
PROJECT_ID="clear-shadow-450810-r1"
REGION="us-central1"
SERVICE_NAME="ai-automation-backend"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Starting deployment to Google Cloud Platform..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if logged in to gcloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: Not logged in to gcloud"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo "📋 Setting GCP project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the image using Cloud Build
echo "🔨 Building Docker image with Cloud Build..."
gcloud builds submit --config cloudbuild.yaml --substitutions=_PROJECT_ID=$PROJECT_ID

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8001 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 900 \
    --max-instances 10 \
    --set-env-vars "ENVIRONMENT=production,PLAYWRIGHT_BROWSERS_PATH=/usr/lib/playwright,PLAYWRIGHT_HEADLESS=true"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🔗 Health check: $SERVICE_URL/health"
echo "📊 Admin API: $SERVICE_URL/api/admin"

# Test the deployment
echo "🧪 Testing deployment..."
if curl -s "$SERVICE_URL/health" | grep -q "healthy"; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed - check logs with:"
    echo "gcloud logs read --service=$SERVICE_NAME --region=$REGION"
fi

echo ""
echo "🎉 Your AI automation backend is now live!"
echo "Next steps:"
echo "1. Update your frontend to use: $SERVICE_URL"
echo "2. Set up your Supabase environment variables"
echo "3. Test the automation endpoints" 