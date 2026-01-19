# 🚀 Get Started in 3 Steps

## Step 1: Setup (2 minutes)

### Local Development

```bash
# Clone repository
git clone your-repo
cd your-repo

# Run setup script
python setup.py

# Edit .env file
# Set: SCRAPER_SCHEDULE=every_6_hours
```

### Or with Docker

```bash
# Clone and configure
git clone your-repo
cd your-repo
cp .env.example .env

# Start services
docker-compose up -d
```

---

## Step 2: Test (1 minute)

```bash
# Start API
python run_api.py

# In another terminal, test
python test_api.py

# Or visit in browser
http://localhost:8000/docs
```

---

## Step 3: Deploy (2 minutes)

### Railway (Recommended)

```bash
# Install CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Add database
railway add --database postgresql

# Set environment
railway variables set HEADLESS_MODE=True
railway variables set SCRAPER_SCHEDULE=every_6_hours

# Get URL
railway domain
```

**Done!** Your API is live at `https://your-app.railway.app`

---

## What You Get

✅ **4 Scrapers** running continuously
✅ **Standardized data** in unified format
✅ **Combined JSON** file with all events
✅ **Database storage** (PostgreSQL/SQLite)
✅ **REST API** with full documentation
✅ **Automatic scheduling** (every 6 hours)

---

## Quick Test

```bash
# Check health
curl https://your-app.railway.app/health

# Get events
curl https://your-app.railway.app/combined-events

# View docs
https://your-app.railway.app/docs
```

---

## Next Steps

1. ✅ Read [FINAL_SUMMARY.md](FINAL_SUMMARY.md) for complete overview
2. ✅ Check [TRANSFORMER_GUIDE.md](TRANSFORMER_GUIDE.md) for data format
3. ✅ See [WORKFLOW.md](WORKFLOW.md) for how it works
4. ✅ Integrate with your frontend

---

## Need Help?

- **Quick Deploy**: [QUICKSTART.md](QUICKSTART.md)
- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **API Docs**: [README_API.md](README_API.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**That's it! You're ready to go! 🎉**
