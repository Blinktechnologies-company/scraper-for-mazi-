#!/bin/bash

echo "=========================================="
echo "Starting Events & Deals API"
echo "=========================================="
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "PORT environment variable: ${PORT}"
echo "Using port: ${PORT:-8000}"
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "=========================================="

# Set default port if not provided
PORT=${PORT:-8000}

# Start uvicorn with the port
exec uvicorn api:app --host 0.0.0.0 --port $PORT --log-level info
