#!/bin/bash
set -e

# Get the port from environment variable or default to 8000
PORT=${PORT:-8000}

echo "🚀 Starting server on port $PORT"

# Start the server
uvicorn server:app --host 0.0.0.0 --port $PORT 