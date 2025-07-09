#!/bin/bash
set -e

echo "🚀 Starting Enhanced Eko Deployment..."

# Check if Node.js and npm are available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

# Install Eko framework if not already installed
if ! command -v eko &> /dev/null; then
    echo "📦 Installing Eko framework..."
    npm install -g @eko-ai/core
fi

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install --with-deps chromium

# Create necessary directories
mkdir -p logs
mkdir -p temp

# Set permissions
chmod +x start.sh

echo "✅ Setup complete. Starting server..."

# Start the FastAPI server
python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} 