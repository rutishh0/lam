FROM node:20-slim AS frontend
WORKDIR /app/frontend
# Copy frontend from repository root context
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund || npm install
COPY frontend .
RUN npm run build

FROM python:3.12-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements from repository root context
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium  # Installs browser + deps

# Copy backend application code from repository root context
COPY backend .

# Copy built frontend into backend for static serving
COPY --from=frontend /app/frontend/build /app/frontend/build

# Expose port
EXPOSE 8080

# Start command honoring PORT env (Koyeb sets PORT=8000). Defaults to 8080 if unset.
CMD ["sh", "-c", "uvicorn server_enhanced:app --host 0.0.0.0 --port ${PORT:-8080}"]