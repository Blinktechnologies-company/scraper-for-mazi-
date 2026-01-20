#!/bin/bash

echo "=========================================="
echo "Starting Events & Deals API"
echo "=========================================="
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "PORT: ${PORT:-8000}"
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "=========================================="

# Start uvicorn
exec uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info
