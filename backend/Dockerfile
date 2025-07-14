FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium  # Installs browser + deps

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Start command - Cloud Run sets PORT=8080
# Start command - run as a module to ensure correct pathing
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8080"] 