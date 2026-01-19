# Events & Deals API

A complete web scraping and API solution for Greek events and deals from multiple sources.

## Features

- **Multiple Scrapers**: Scrapes events from Culture.gov, VisitGreece, Pigolampides, More.com
- **Database Storage**: SQLite (default) or PostgreSQL/MySQL support
- **REST API**: FastAPI-powered endpoints for accessing events and deals
- **Background Scraping**: Run scrapers in background without blocking API
- **Filtering & Search**: Filter by source, category, search by keywords
- **Resume Capability**: Scrapers can resume from where they left off

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=sqlite:///./events_deals.db
HEADLESS_MODE=True
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Run the API

```bash
python api.py
```

Or with uvicorn:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### 4. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Events

- `GET /events` - Get all events
  - Query params: `skip`, `limit`, `source`, `category`, `search`
  - Example: `/events?source=culture_gov&limit=20`

- `GET /events/{event_id}` - Get specific event

### Deals

- `GET /deals` - Get all deals
  - Query params: `skip`, `limit`, `source`, `category`, `search`

- `GET /deals/{deal_id}` - Get specific deal

### Scraping

- `POST /scrape` - Run scrapers in background
  - Query params: `headless` (bool), `max_events` (int)
  - Returns immediately, scraping runs in background

- `POST /scrape/sync` - Run scrapers synchronously
  - Query params: `headless` (bool), `max_events` (int)
  - Waits for completion (may take several minutes)

### Statistics

- `GET /stats` - Get statistics about events and deals
  - Returns counts by source and category

### Health

- `GET /health` - Health check endpoint

## Usage Examples

### Get Events

```bash
# Get first 50 events
curl http://localhost:8000/events

# Get events from specific source
curl http://localhost:8000/events?source=culture_gov

# Search events
curl http://localhost:8000/events?search=concert

# Get events by category
curl http://localhost:8000/events?category=music
```

### Trigger Scraping

```bash
# Run scrapers in background
curl -X POST "http://localhost:8000/scrape?headless=true&max_events=100"

# Run scrapers synchronously (wait for completion)
curl -X POST "http://localhost:8000/scrape/sync?headless=true&max_events=50"
```

### Get Statistics

```bash
curl http://localhost:8000/stats
```

## Database

### SQLite (Default)

The default configuration uses SQLite, which creates a file `events_deals.db` in your project directory.

### PostgreSQL

To use PostgreSQL, update your `.env`:

```
DATABASE_URL=postgresql://username:password@localhost/events_db
```

Then install the PostgreSQL driver:

```bash
pip install psycopg2-binary
```

### MySQL

To use MySQL, update your `.env`:

```
DATABASE_URL=mysql://username:password@localhost/events_db
```

Then install the MySQL driver:

```bash
pip install pymysql
```

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t events-api .
docker run -p 8000:8000 -v $(pwd)/events_deals.db:/app/events_deals.db events-api
```

### Cloud Deployment (Heroku, Railway, etc.)

1. Add a `Procfile`:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

2. Add buildpacks for Chrome (if using Heroku):
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
```

3. Set environment variables:
```bash
heroku config:set HEADLESS_MODE=True
heroku config:set DATABASE_URL=your_database_url
```

## Manual Scraping

You can also run scrapers manually:

```bash
# Run all scrapers
python -c "from scraper_manager import ScraperManager; from database import SessionLocal; db = SessionLocal(); manager = ScraperManager(db); manager.run_all_scrapers(headless=True, max_events_per_source=100)"

# Run individual scrapers
python culture_final_scraper.py
python visitgreece_detailed_scraper.py
python pigolampides_scraper.py
python more_events_scraper_optimized.py
```

## Scheduled Scraping

### Using Cron (Linux/Mac)

Add to crontab:

```bash
# Run scrapers daily at 2 AM
0 2 * * * cd /path/to/project && python -c "from scraper_manager import ScraperManager; from database import SessionLocal; db = SessionLocal(); manager = ScraperManager(db); manager.run_all_scrapers(headless=True)"
```

### Using Windows Task Scheduler

Create a batch file `run_scrapers.bat`:

```batch
@echo off
cd C:\path\to\project
python -c "from scraper_manager import ScraperManager; from database import SessionLocal; db = SessionLocal(); manager = ScraperManager(db); manager.run_all_scrapers(headless=True)"
```

Schedule it in Task Scheduler.

### Using APScheduler (Python)

Add to your `api.py`:

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def scheduled_scrape():
    db = SessionLocal()
    manager = ScraperManager(db)
    manager.run_all_scrapers(headless=True, max_events_per_source=100)
    db.close()

scheduler.add_job(scheduled_scrape, 'cron', hour=2)  # Daily at 2 AM
scheduler.start()
```

## Troubleshooting

### ChromeDriver Issues

If you get ChromeDriver errors:

1. Make sure Chrome is installed
2. Set `CHROME_DRIVER_PATH=auto` in `.env`
3. Or download ChromeDriver manually and set the path

### Database Locked (SQLite)

If you get "database is locked" errors with SQLite:

1. Use PostgreSQL for production
2. Or ensure only one process writes at a time

### Memory Issues

If scrapers use too much memory:

1. Reduce `max_events_per_source`
2. Run scrapers one at a time
3. Use `headless=True` mode

## Project Structure

```
.
├── api.py                          # FastAPI application
├── database.py                     # Database models and connection
├── scraper_manager.py              # Unified scraper manager
├── scraper_base.py                 # Base scraper class
├── config.py                       # Configuration
├── culture_final_scraper.py        # Culture.gov scraper
├── visitgreece_detailed_scraper.py # VisitGreece scraper
├── pigolampides_scraper.py         # Pigolampides blog scraper
├── more_events_scraper_optimized.py # More.com scraper
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── scraped_data/                   # JSON backups
```

## License

MIT
