# 🔧 Troubleshooting Guide

Common issues and solutions for the Events & Deals API.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [ChromeDriver Issues](#chromedriver-issues)
3. [Database Issues](#database-issues)
4. [Scheduler Issues](#scheduler-issues)
5. [Scraping Issues](#scraping-issues)
6. [API Issues](#api-issues)
7. [Deployment Issues](#deployment-issues)
8. [Performance Issues](#performance-issues)

---

## Installation Issues

### Problem: pip install fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with specific Python version
python3.11 -m pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Python version too old

**Error:**
```
Python 3.7 or lower detected
```

**Solution:**
- Install Python 3.8 or higher
- Download from [python.org](https://python.org)
- Or use pyenv: `pyenv install 3.11`

---

## ChromeDriver Issues

### Problem: ChromeDriver not found

**Error:**
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Solution 1: Auto-detect (Recommended)**
```bash
# In .env file
CHROME_DRIVER_PATH=auto
```

**Solution 2: Manual installation**
```bash
# Download ChromeDriver
# Visit: https://chromedriver.chromium.org/downloads

# Windows
set CHROME_DRIVER_PATH=C:\path\to\chromedriver.exe

# Linux/Mac
export CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
```

**Solution 3: Use webdriver-manager**
```python
# Already included in requirements.txt
pip install webdriver-manager
```

### Problem: Chrome version mismatch

**Error:**
```
This version of ChromeDriver only supports Chrome version XX
```

**Solution:**
```bash
# Update Chrome browser to latest version
# Then update ChromeDriver

# Or use auto mode
CHROME_DRIVER_PATH=auto
```

### Problem: Chrome not found in Docker

**Error:**
```
chrome not reachable
```

**Solution:**
Ensure Dockerfile includes Chrome installation:
```dockerfile
RUN apt-get update && apt-get install -y \
    wget gnupg unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable
```

---

## Database Issues

### Problem: Database is locked (SQLite)

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution 1: Use PostgreSQL (Recommended for production)