# Deployment Guide - Continuous Scraping

This guide covers deploying your Events & Deals API with continuous background scraping.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

Railway supports Docker, PostgreSQL, and background workers out of the box.

**Steps:**

1. Create account at [railway.app](https://railway.app)

2. Install Railway CLI:
```bash
npm install -g @railway/cli
railway login
```

3. Initialize project:
```bash
railway init
```

4. Add PostgreSQL database:
```bash
railway add --database postgresql
```

5. Set environment variables:
```bash
railway variables set HEADLESS_MODE=True
railway variables set SCRAPER_SCHEDULE=every_6_hours
railway variables set SCRAPER_MAX_EVENTS=100
railway variables set SCRAPER_RUN_ON_STARTUP=True
```

6. Deploy:
```bash
railway up
```

7. Get your URL:
```bash
railway domain
```

**Cost:** Free tier includes 500 hours/month + $5 credit

---

### Option 2: Render

Render offers free tier with background workers.

**Steps:**

1. Create account at [render.com](https://render.com)

2. Create `render.yaml`:
```yaml
services:
  - type: web
    name: events-api
    env: docker
    plan: free
    envVars:
      - key: HEADLESS_MODE
        value: "True"
      - key: SCRAPER_SCHEDULE
        value: every_6_hours
      - key: SCRAPER_MAX_EVENTS
        value: "100"
      - key: DATABASE_URL
        fromDatabase:
          name: events-db
          property: connectionString

databases:
  - name: events-db
    plan: free
```

3. Connect your GitHub repo

4. Deploy automatically on push

**Cost:** Free tier available (with limitations)

---

### Option 3: DigitalOcean App Platform

**Steps:**

1. Create account at [digitalocean.com](https://digitalocean.com)

2. Create new App from Docker Hub or GitHub

3. Add PostgreSQL database

4. Set environment variables in dashboard

5. Deploy

**Cost:** $5/month for basic app + $7/month for database

---

### Option 4: AWS (EC2 + RDS)

Most flexible but requires more setup.

**Steps:**

1. Launch EC2 instance (t2.micro for free tier)

2. Install Docker:
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

3. Create RDS PostgreSQL database

4. Clone your repo and create `.env`:
```bash
git clone your-repo
cd your-repo
nano .env
```

5. Run with Docker Compose:
```bash
docker-compose up -d
```

6. Set up CloudWatch for monitoring

**Cost:** Free tier available for 12 months

---

### Option 5: VPS (DigitalOcean Droplet, Linode, etc.)

**Steps:**

1. Create a VPS ($5-10/month)

2. SSH into server:
```bash
ssh root@your-server-ip
```

3. Install Docker and Docker Compose:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Clone repo and configure:
```bash
git clone your-repo
cd your-repo
cp .env.example .env
nano .env
```

5. Run:
```bash
docker-compose up -d
```

6. Set up nginx reverse proxy (optional):
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/events-api
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/events-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📋 Environment Variables for Production

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/dbname
HEADLESS_MODE=True
CHROME_DRIVER_PATH=auto

# Scheduler (choose one)
SCRAPER_SCHEDULE=hourly              # Every hour
SCRAPER_SCHEDULE=every_6_hours       # Every 6 hours
SCRAPER_SCHEDULE=every_12_hours      # Every 12 hours
SCRAPER_SCHEDULE=twice_daily         # 6 AM and 6 PM
SCRAPER_SCHEDULE=daily               # Once daily at 2 AM

# Optional
SCRAPER_MAX_EVENTS=100               # Max events per source
SCRAPER_RUN_ON_STARTUP=True          # Run immediately on startup
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart
```

### Using Docker only

```bash
# Build image
docker build -t events-api .

# Run with SQLite
docker run -d -p 8000:8000 \
  -e HEADLESS_MODE=True \
  -e SCRAPER_SCHEDULE=every_6_hours \
  -v $(pwd)/events_deals.db:/app/events_deals.db \
  events-api

# Run with PostgreSQL
docker run -d -p 8000:8000 \
  -e HEADLESS_MODE=True \
  -e SCRAPER_SCHEDULE=every_6_hours \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  events-api
```

---

## 📊 Monitoring

### Check Scheduler Status

```bash
curl http://your-domain.com/scheduler/status
```

Response:
```json
{
  "running": true,
  "jobs": [
    {
      "id": "scraper_6h",
      "name": "6-Hour Scraper",
      "next_run": "2026-01-19T12:00:00"
    }
  ]
}
```

### Check Health

```bash
curl http://your-domain.com/health
```

### View Logs

**Docker:**
```bash
docker logs -f container-name
```

**Docker Compose:**
```bash
docker-compose logs -f api
```

**Railway:**
```bash
railway logs
```

---

## 🔧 Troubleshooting

### Scrapers Not Running

1. Check scheduler status:
```bash
curl http://your-domain.com/scheduler/status
```

2. Check logs for errors

3. Verify environment variables:
```bash
echo $SCRAPER_SCHEDULE
echo $HEADLESS_MODE
```

### ChromeDriver Issues

Make sure Dockerfile includes Chrome installation:
```dockerfile
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable
```

### Database Connection Issues

1. Check DATABASE_URL format
2. Ensure database is accessible from container
3. For Railway/Render, use internal connection string

### Memory Issues

1. Reduce `SCRAPER_MAX_EVENTS`
2. Use `SCRAPER_SCHEDULE=daily` instead of hourly
3. Upgrade to larger instance

---

## 🎯 Recommended Configurations

### Light Usage (Small Sites)
```bash
SCRAPER_SCHEDULE=daily
SCRAPER_MAX_EVENTS=50
```

### Medium Usage (Regular Updates)
```bash
SCRAPER_SCHEDULE=every_12_hours
SCRAPER_MAX_EVENTS=100
```

### Heavy Usage (Frequent Updates)
```bash
SCRAPER_SCHEDULE=every_6_hours
SCRAPER_MAX_EVENTS=200
```

---

## 📈 Scaling

### Horizontal Scaling

Run multiple instances with load balancer:

1. Deploy API instances (read-only)
2. Deploy separate worker instance (scraping only)
3. Use shared PostgreSQL database

### Separate Worker

Create `worker.py`:
```python
from scheduler import start_scheduler
import time

if __name__ == "__main__":
    start_scheduler()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
```

Deploy worker separately from API.

---

## 🔐 Security

1. Use environment variables for secrets
2. Enable HTTPS (use Cloudflare or Let's Encrypt)
3. Add API authentication if needed
4. Restrict database access
5. Use read-only database replicas for API

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid | Database |
|----------|-----------|------|----------|
| Railway | 500h/month + $5 credit | $5-20/month | Included |
| Render | 750h/month | $7-25/month | Free tier |
| DigitalOcean | No | $5-12/month | $7-15/month |
| AWS | 12 months | $5-50/month | $15-50/month |
| VPS | No | $5-10/month | Self-hosted |

**Recommendation:** Start with Railway or Render free tier, upgrade as needed.
