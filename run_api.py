"""
Simple script to run the API server
"""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    
    print("="*60)
    print("Starting Events & Deals API")
    print("="*60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"API Docs: http://localhost:{port}/docs")
    print(f"ReDoc: http://localhost:{port}/redoc")
    print("="*60)
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
