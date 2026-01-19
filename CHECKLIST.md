# ✅ Deployment Checklist

Use this checklist to ensure everything is set up correctly.

---

## 📋 Pre-Deployment

### Local Testing

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] Chrome/ChromeDriver available
- [ ] Database initialized
- [ ] API starts successfully (`python run_api.py`)
- [ ] API docs accessible (`http://localhost:8000/docs`)
- [ ] Test API passes (`python test_api.py`)
- [ ] Transformer test passes (`python test_transformer.py`)
- [ ] Manual scraper test works (`python run_scrapers.py --max-events 10`)

### Configuration

- [ ] `HEADLESS_MODE` set correctly (False for local, True for production)
- [ ] `SCRAPER_SCHEDULE` configured (recommend: `every_6_hours`)
- [ ] `SCRAPER_MAX_EVENTS` set (recommend: 100)
- [ ] `DATABASE_URL` configured
- [ ] `API_HOST` and `API_PORT` set

---

## ☁️ Cloud Deployment

### Railway

- [ ] Railway account created
- [ ] Railway CLI installed
- [ ] Project initialized (`railway init`)
- [ ] PostgreSQL database added
- [ ] Environment variables set:
  - [ ] `HEADLESS_MODE=True`
  - [ ] `SCRAPER_SCHEDULE=every_6_hours`
  - [ ] `SCRAPER_MAX_EVENTS=100`
  - [ ] `SCRAPER_RUN_ON_STARTUP=True`
- [ ] Deployed (`railway up`)
- [ ] Domain generated (`railway domain`)
- [ ] Health check passes (`/health`)
- [ ] Scheduler status checked (`/scheduler/status`)

### Render

- [ ] Render account created
- [ ] GitHub repo connected
- [ ] Web service created
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] Deployed successfully
- [ ] Health check passes
- [ ] Scheduler running

### Docker

- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] `.env` file configured
- [ ] `docker-compose up -d` successful
- [ ] Containers running (`docker-compose ps`)
- [ ] Logs clean (`docker-compose logs`)
- [ ] API accessible
- [ ] Database connected

---

## 🧪 Post-Deployment Testing

### API Endpoints

- [ ] Root endpoint works (`GET /`)
- [ ] Health check works (`GET /health`)
- [ ] Scheduler status works (`GET /scheduler/status`)
- [ ] Stats endpoint works (`GET /stats`)
- [ ] Events endpoint works (`GET /events`)
- [ ] Combined events works (`GET /combined-events`)
- [ ] API docs accessible (`GET /docs`)

### Scraping

- [ ] Manual scrape trigger works (`POST /scrape`)
- [ ] Scrapers run successfully
- [ ] Events saved to database
- [ ] Combined JSON file created
- [ ] No errors in logs

### Scheduler

- [ ] Scheduler is running
- [ ] Next run time is set
- [ ] Job is registered
- [ ] Automatic scraping works

---

## 📊 Data Verification

### Database

- [ ] Events table exists
- [ ] Events are being saved
- [ ] No duplicate events (by URL)
- [ ] All fields populated correctly
- [ ] Indexes created

### Combined JSON

- [ ] File exists (`scraped_data/combined_events.json`)
- [ ] Contains events from all sources
- [ ] Data is in standardized format
- [ ] All required fields present
- [ ] Dates formatted correctly (YYYY-MM-DD)
- [ ] Categories mapped correctly
- [ ] Regions detected correctly

### Data Quality

- [ ] Titles are clean
- [ ] Descriptions are readable
- [ ] Dates are valid
- [ ] Images URLs work
- [ ] Prices are correct (0 for free)
- [ ] Sources are labeled correctly

---

## 🔍 Monitoring

### Logs

- [ ] Application logs accessible
- [ ] No critical errors
- [ ] Scraping logs show success
- [ ] Database logs clean

### Performance

- [ ] API response time < 1s
- [ ] Scraping completes in reasonable time
- [ ] Memory usage acceptable
- [ ] CPU usage acceptable

### Alerts (Optional)

- [ ] Uptime monitoring configured
- [ ] Error alerts set up
- [ ] Performance monitoring active

---

## 🔐 Security

### Environment

- [ ] `.env` file not committed to git
- [ ] Sensitive data in environment variables
- [ ] Database credentials secure
- [ ] API keys protected (if any)

### API

- [ ] CORS configured correctly
- [ ] Rate limiting considered (optional)
- [ ] Authentication considered (optional)
- [ ] HTTPS enabled (in production)

---

## 📚 Documentation

### Code

- [ ] README.md updated
- [ ] API documentation complete
- [ ] Code comments added
- [ ] Configuration documented

### Deployment

- [ ] Deployment steps documented
- [ ] Environment variables listed
- [ ] Troubleshooting guide available
- [ ] Architecture documented

---

## 🎯 Integration

### Frontend

- [ ] API URL configured
- [ ] Endpoints tested
- [ ] Data format understood
- [ ] Error handling implemented

### Third-party

- [ ] Webhooks configured (if needed)
- [ ] External services connected (if needed)
- [ ] API keys set (if needed)

---

## 🔄 Maintenance

### Regular Tasks

- [ ] Monitor logs weekly
- [ ] Check scraper success rate
- [ ] Review database size
- [ ] Update dependencies monthly
- [ ] Backup database regularly

### Optimization

- [ ] Review scraping frequency
- [ ] Optimize database queries
- [ ] Clean old data (optional)
- [ ] Monitor costs

---

## 📈 Scaling (When Needed)

### Performance

- [ ] Database optimization
- [ ] Caching implemented
- [ ] Load balancing configured
- [ ] CDN for static files

### Infrastructure

- [ ] Separate worker instance
- [ ] Database read replicas
- [ ] Horizontal scaling
- [ ] Auto-scaling configured

---

## ✅ Final Checks

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Team trained (if applicable)
- [ ] Monitoring active
- [ ] Backup strategy in place
- [ ] Rollback plan ready
- [ ] Support contacts documented

---

## 🎉 Launch

- [ ] Production deployment complete
- [ ] All checks passed
- [ ] Monitoring confirmed
- [ ] Team notified
- [ ] Users can access API
- [ ] Data is flowing correctly

---

## 📞 Support Contacts

**Technical Issues:**
- Check logs first
- Review documentation
- Test endpoints manually

**Deployment Issues:**
- Check environment variables
- Verify database connection
- Review platform-specific docs

---

**Congratulations! You're ready to go live! 🚀**

---

## Quick Reference

### Essential Commands

```bash
# Local
python run_api.py
python test_api.py
python test_transformer.py

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down

# Railway
railway logs
railway status
railway variables

# Testing
curl http://localhost:8000/health
curl http://localhost:8000/scheduler/status
curl http://localhost:8000/stats
```

### Essential URLs

- API Docs: `/docs`
- Health: `/health`
- Scheduler: `/scheduler/status`
- Stats: `/stats`
- Events: `/events`
- Combined: `/combined-events`
