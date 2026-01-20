# Railway Deployment Troubleshooting

## Recent Changes
✅ Fixed Chrome installation (modern GPG method)
✅ Simplified health check endpoint
✅ Added detailed logging on startup
✅ Disabled scraper on startup (prevents blocking)
✅ Added `/ping` endpoint for simple testing

## Current Status
- Build: ✅ Successful
- Health Check: ⏳ Testing with improved configuration

## Environment Variables to Set in Railway

### Required
```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
```
Your Neon PostgreSQL connection string

### Recommended
```
SCRAPER_SCHEDULE=every_6_hours
SCRAPER_MAX_EVENTS=100
SCRAPER_RUN_ON_STARTUP=False
HEADLESS_MODE=True
```

### Optional
```
CHROME_DRIVER_PATH=auto
PORT=(Railway sets this automatically)
```

## Testing Endpoints

Once deployed, test these endpoints:

1. **Simple ping** (no dependencies):
   ```bash
   curl https://your-app.railway.app/ping
   ```
   Should return: `{"status":"ok"}`

2. **Health check**:
   ```bash
   curl https://your-app.railway.app/health
   ```
   Should return: `{"status":"healthy","timestamp":"..."}`

3. **Root endpoint**:
   ```bash
   curl https://your-app.railway.app/
   ```
   Should return API info

4. **Stats** (requires database):
   ```bash
   curl https://your-app.railway.app/stats
   ```

## Common Issues

### Issue: Health check fails with "service unavailable"
**Causes:**
- App not binding to correct PORT
- Database connection failing
- Scheduler blocking startup
- Missing environment variables

**Solutions:**
- ✅ Dockerfile now uses `${PORT:-8000}` correctly
- ✅ Startup errors are caught and logged
- ✅ Scheduler won't block startup
- ⚠ Check Railway logs for specific errors

### Issue: App starts but crashes
**Check Railway logs for:**
- Database connection errors → Set DATABASE_URL
- Chrome/ChromeDriver errors → Should work with current Dockerfile
- Import errors → Check requirements.txt

### Issue: Scrapers not running
**Check:**
- Scheduler status: `GET /scheduler/status`
- Environment variable: `SCRAPER_SCHEDULE`
- Logs for scheduler initialization

## Viewing Logs in Railway
1. Go to your project in Railway dashboard
2. Click on the deployment
3. Click "View Logs" or "Deployments" tab
4. Look for:
   - `🚀 Starting API...`
   - `✓ Database initialized`
   - `✓ Background scheduler started`
   - `✓ API started successfully`

## Manual Scraping
If automatic scraping isn't working, trigger manually:
```bash
curl -X POST https://your-app.railway.app/scrape
```

## Next Steps After Successful Deployment
1. Verify health check passes
2. Check `/stats` to see if database is working
3. Trigger manual scrape to populate data
4. Verify scheduler is running: `/scheduler/status`
5. Check events endpoint: `/events`
