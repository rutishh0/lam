#!/bin/bash
# Install Node.js dependencies for Eko
cd services/eko_scripts
npm install @eko-ai/eko @eko-ai/eko-nodejs playwright
npx playwright install chromium
cd ../..

# Start the Python server
python server.py