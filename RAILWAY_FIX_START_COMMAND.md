# Railway Start Command Fix

## Problem
Railway has a "Start command" override in the settings that's using:
```
uvicorn api:app --host 0.0.0.0 --port $PORT
```

This doesn't work because `$PORT` isn't being expanded properly.

## Solution

### Option 1: Remove Start Command Override (RECOMMENDED)
1. Go to Railway dashboard
2. Click on your deployment
3. Go to **Settings** tab
4. Find **"Deploy"** section
5. Look for **"Start Command"** field
6. **DELETE** the start command (leave it empty)
7. Click **"Save"**
8. Redeploy

This will let the Dockerfile CMD take over, which uses `python3 start.py` that properly handles the PORT variable.

### Option 2: Update Start Command
If you want to keep a start command, change it to:
```
python3 start.py
```

## Why This Fixes It
- The Dockerfile CMD is: `CMD ["python3", "start.py"]`
- The `start.py` script properly reads `os.environ.get('PORT')` 
- Python handles environment variables correctly
- No shell expansion issues

## Verification
After removing the start command override, you should see in the logs:
```
🚀 Starting Events & Deals API
Python version: Python 3.11.x
PORT environment variable: 8000
Using port: 8000
Executing: uvicorn api:app --host 0.0.0.0 --port 8000 --log-level info
```

Then the app will start successfully and health checks will pass.

## Current Files
- ✅ `Dockerfile` - Uses `CMD ["python3", "start.py"]`
- ✅ `start.py` - Properly handles PORT environment variable
- ✅ `railway.toml` - Start command commented out
- ✅ `api.py` - Has robust error handling and logging

## Next Step
**Go to Railway Settings → Deploy → Delete the "Start Command" field → Save → Redeploy**
