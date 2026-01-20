#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles PORT environment variable properly
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🚀 Starting Events & Deals API")
    print("=" * 60)
    
    # Get port from environment or use default
    port = os.environ.get('PORT', '8000')
    
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PORT environment variable: {os.environ.get('PORT', 'Not set')}")
    print(f"Using port: {port}")
    print(f"DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
    print("=" * 60)
    
    # Start uvicorn
    cmd = [
        "uvicorn",
        "api:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--log-level", "info"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    print("=" * 60)
    sys.stdout.flush()
    
    # Execute uvicorn
    os.execvp("uvicorn", cmd)

if __name__ == "__main__":
    main()
