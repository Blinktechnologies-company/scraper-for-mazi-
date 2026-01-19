# 🚀 Quick Start - Deploy in 5 Minutes

## Option 1: Railway (Easiest)

1. **Sign up**: Go to [railway.app](https://railway.app) and create account

2. **Click "New Project"** → **"Deploy from GitHub repo"**

3. **Connect your repo** and select it

4. **Add PostgreSQL**: 
   - Click "New" → "Database" → "Add PostgreSQL"

5. **Set Variables** (in your service settings):
   ```
   HEADLESS_MODE=True
   SCRAPER_SCHEDULE=every_6_hours
   SCRAPER_MAX_EVENTS=100
   SCRAPER_RUN_ON_STARTUP=True
   ```

6. **Deploy** - Railway will automatically build and deploy

7. **Get URL**: Click "Settings" → "Generate Domain"

✅ Done! Your API is live with continuous scraping every 6 hours.

---

## Option 2: Render

1. **Sign up**: Go to [render.com](https://render.com)

2. **New Web Service** → Connect GitHub repo

3. **Settings**:
   - Environment: Docker
   - Plan: Free

4. **Add PostgreSQL**:
   - Dashboard → "New" → "PostgreSQL"
   - Copy connection string

5. **Environment Variables**:
   ```
   DATABASE_URL=<paste connection string>
   HEADLESS_MODE=True
   SCRAPER_SCHEDULE=every_6_hours
   SCRAPER_MAX_EVENTS=100
   ```

6. **Deploy**

✅ Done!

---

## Option 3: Local with Docker

1. **Install Docker**: [docker.com](https://docker.com)

2. **Clone and configure**:
```bash
git clone your-repo
cd your-repo
cp .env.example .env
```

3. **Edit .env**:
```bash
SCRAPER_SCHEDULE=every_6_hours
SCRAPER_MAX_EVENTS=100
HEADLESS_MODE=True
```

4. **Run**:
```bash
docker-compose up -d
```

5. **Access**: http://localhost:8000

✅ Done!

---

## Test Your Deployment

```bash
# Check health
curl https://your-domain.com/health

# Check scheduler
curl https://your-domain.com/scheduler/status

# Get events
curl https://your-domain.com/events?limit=10

# View API docs
# Open: https://your-domain.com/docs
```

---

## Scheduler Options

Change `SCRAPER_SCHEDULE` to:

- `hourly` - Every hour
- `every_6_hours` - Every 6 hours (recommended)
- `every_12_hours` - Every 12 hours
- `twice_daily` - 6 AM and 6 PM
- `daily` - Once daily at 2 AM

---

## Next Steps

1. ✅ Deploy using one of the options above
2. ✅ Test endpoints
3. ✅ Monitor scheduler status
4. ✅ Check logs for scraping activity
5. ✅ Integrate with your frontend

Need help? Check `DEPLOYMENT.md` for detailed guides.
