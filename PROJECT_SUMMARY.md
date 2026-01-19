# 📦 Events & Deals Scraper API - Project Summary

## What You Have Now

A complete, production-ready web scraping and API system that:

✅ **Scrapes events** from 4 Greek sources:
- Culture.gov.gr (Ministry of Culture events)
- VisitGreece.gr (Tourism events)
- Pigolampides.gr (Blog posts/events)
- More.com (Event tickets)

✅ **Stores data** in database (SQLite/PostgreSQL/MySQL)

✅ **Provides REST API** to access events and deals

✅ **Runs continuously** with automatic scheduled scraping

✅ **Ready to deploy** to cloud platforms

---

## 📁 Key Files

### Core Application
- `api.py` - FastAPI web server with REST endpoints
- `database.py` - Database models (Events & Deals tables)
- `scraper_manager.py` - Manages all scrapers
- `scheduler.py` - Background scheduler for continuous scraping

### Scrapers
- `culture_final_scraper.py` - Culture.gov scraper
- `visitgreece_detailed_scraper.py` - VisitGreece scraper
- `pigolampides_scraper.py` - Pigolampides blog scraper
- `more_events_scraper_optimized.py` - More.com scraper

### Deployment
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Multi-container setup (API + PostgreSQL)
- `render.yaml` - Render.com deployment config
- `railway-config.json` - Railway deployment config

### Documentation
- `README_API.md` - Complete API documentation
- `DEPLOYMENT.md` - Detailed deployment guide
- `QUICKSTART.md` - 5-minute deployment guide

### Utilities
- `run_api.py` - Simple script to start API
- `run_scrapers.py` - Manual scraper execution
- `test_api.py` - API testing script

---

## 🚀 How to Use

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API (with automatic scraping)
python run_api.py

# Or manually run scrapers
python run_scrapers.py --headless --max-events 100
```

### Deploy to Cloud

**Easiest: Railway**
```bash
# Install CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Or: Render, DigitalOcean, AWS** (see DEPLOYMENT.md)

---

## 🔄 Continuous Scraping

The scheduler automatically runs scrapers at intervals you configure:

**Environment Variable**: `SCRAPER_SCHEDULE`

Options:
- `hourly` - Every hour
- `every_6_hours` - Every 6 hours ⭐ Recommended
- `every_12_hours` - Every 12 hours
- `twice_daily` - 6 AM and 6 PM
- `daily` - Once daily at 2 AM

**How it works:**
1. API starts → Scheduler starts
2. Scheduler runs scrapers at configured intervals
3. New events saved to database automatically
4. API serves latest data

---

## 📡 API Endpoints

### Get Events
```bash
GET /events
GET /events?source=culture_gov
GET /events?category=music
GET /events?search=concert
GET /events/{id}
```

### Get Deals
```bash
GET /deals
GET /deals?source=pigolampides
GET /deals/{id}
```

### Trigger Scraping
```bash
POST /scrape              # Background
POST /scrape/sync         # Wait for completion
```

### Monitor
```bash
GET /stats                # Statistics
GET /scheduler/status     # Scheduler info
GET /health              # Health check
```

### Documentation
```
GET /docs                # Swagger UI
GET /redoc               # ReDoc
```

---

## 🗄️ Database Schema

### Events Table
- id, title, description
- date, location, category
- price, url, source
- images (JSON), contact
- content (JSON), full_text
- created_at, updated_at

### Deals Table
- id, title, description
- price, original_price, discount
- url, source, category
- images (JSON), valid_until
- created_at, updated_at

---

## 🎯 Deployment Recommendations

### For Testing
- **Railway Free Tier** or **Render Free Tier**
- SQLite database
- `SCRAPER_SCHEDULE=daily`

### For Production
- **Railway** ($5-10/month) or **DigitalOcean** ($12/month)
- PostgreSQL database
- `SCRAPER_SCHEDULE=every_6_hours`
- `SCRAPER_MAX_EVENTS=200`

### For High Traffic
- Multiple API instances (load balanced)
- Separate worker instance for scraping
- PostgreSQL with read replicas
- Redis for caching

---

## 📊 What Gets Scraped

### Culture.gov.gr
- Greek cultural events
- Museums, exhibitions
- Festivals, performances

### VisitGreece.gr
- Tourism events
- Local festivals
- Cultural activities

### Pigolampides.gr
- Blog posts about events
- Local recommendations
- Event reviews

### More.com
- Event tickets
- Concerts, shows
- Theater, sports

---

## 🔧 Configuration

### For Local Development (.env)
```bash
HEADLESS_MODE=False
SCRAPER_SCHEDULE=daily
SCRAPER_MAX_EVENTS=50
DATABASE_URL=sqlite:///./events_deals.db
```

### For Production (.env)
```bash
HEADLESS_MODE=True
SCRAPER_SCHEDULE=every_6_hours
SCRAPER_MAX_EVENTS=100
DATABASE_URL=postgresql://user:pass@host/db
SCRAPER_RUN_ON_STARTUP=True
```

---

## 📈 Monitoring

### Check Scheduler
```bash
curl https://your-api.com/scheduler/status
```

Response:
```json
{
  "running": true,
  "jobs": [{
    "id": "scraper_6h",
    "name": "6-Hour Scraper",
    "next_run": "2026-01-19T18:00:00"
  }]
}
```

### Check Stats
```bash
curl https://your-api.com/stats
```

Response:
```json
{
  "total_events": 450,
  "total_deals": 23,
  "events_by_source": {
    "culture_gov": 120,
    "visitgreece": 180,
    "pigolampides": 100,
    "more_events": 50
  }
}
```

---

## 🎉 Next Steps

1. ✅ **Test Locally**
   ```bash
   python run_api.py
   # Visit: http://localhost:8000/docs
   ```

2. ✅ **Deploy to Cloud**
   - Follow QUICKSTART.md for Railway/Render
   - Or DEPLOYMENT.md for other platforms

3. ✅ **Configure Scheduler**
   - Set `SCRAPER_SCHEDULE` in environment
   - Monitor with `/scheduler/status`

4. ✅ **Integrate with Frontend**
   - Use API endpoints to fetch events
   - Display in your app/website

5. ✅ **Monitor & Scale**
   - Check logs regularly
   - Adjust scraping frequency
   - Scale as needed

---

## 💡 Tips

- Start with `SCRAPER_SCHEDULE=daily` to avoid rate limiting
- Use `HEADLESS_MODE=True` in production to save resources
- Monitor `/health` endpoint for uptime checks
- Back up database regularly
- Use PostgreSQL for production (not SQLite)

---

## 🆘 Support

- Check logs: `docker-compose logs -f`
- Test endpoints: `python test_api.py`
- View docs: http://localhost:8000/docs
- Read: DEPLOYMENT.md for troubleshooting

---

## 📝 License

MIT - Use freely for your projects!
