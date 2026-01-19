# 🏗️ System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
│                                                              │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  REST API  │  │  Scheduler   │  │ Scraper Manager  │   │
│  │ Endpoints  │  │ (APScheduler)│  │                  │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
│         │               │                    │              │
└─────────┼───────────────┼────────────────────┼──────────────┘
          │               │                    │
          │               │                    │
          ▼               ▼                    ▼
    ┌──────────┐    ┌──────────┐      ┌──────────────┐
    │ Database │    │  Cron    │      │   Scrapers   │
    │ (SQLite/ │    │  Jobs    │      │              │
    │  Postgres)│    └──────────┘      │ ┌──────────┐ │
    └──────────┘                       │ │Culture.gov│ │
                                       │ ├──────────┤ │
                                       │ │VisitGreece│ │
                                       │ ├──────────┤ │
                                       │ │Pigolampides│ │
                                       │ ├──────────┤ │
                                       │ │ More.com │ │
                                       │ └──────────┘ │
                                       └──────────────┘
```

## Component Flow

### 1. Application Startup

```
Start API
    │
    ├─> Initialize Database (create tables)
    │
    ├─> Start Scheduler
    │       │
    │       └─> Load schedule from env (SCRAPER_SCHEDULE)
    │       └─> Register scraping jobs
    │       └─> Run initial scrape (if SCRAPER_RUN_ON_STARTUP=True)
    │
    └─> Start FastAPI server
```

### 2. Scheduled Scraping Flow

```
Scheduler Trigger (e.g., every 6 hours)
    │
    ├─> Create Database Session
    │
    ├─> Initialize Scraper Manager
    │
    ├─> Run All Scrapers Sequentially:
    │       │
    │       ├─> Culture.gov Scraper
    │       │       ├─> Navigate to website
    │       │       ├─> Load all events
    │       │       ├─> Extract data
    │       │       └─> Return events list
    │       │
    │       ├─> VisitGreece Scraper
    │       │       └─> (same process)
    │       │
    │       ├─> Pigolampides Scraper
    │       │       └─> (same process)
    │       │
    │       └─> More.com Scraper
    │               └─> (same process)
    │
    ├─> Save Events to Database
    │       ├─> Check for duplicates (by URL)
    │       ├─> Insert new events
    │       └─> Commit transaction
    │
    └─> Log Results
```

### 3. API Request Flow

```
Client Request: GET /events?source=culture_gov&limit=20
    │
    ├─> FastAPI receives request
    │
    ├─> Validate query parameters
    │
    ├─> Create database session
    │
    ├─> Query database:
    │       SELECT * FROM events
    │       WHERE source = 'culture_gov'
    │       ORDER BY created_at DESC
    │       LIMIT 20
    │
    ├─> Serialize to JSON (Pydantic models)
    │
    └─> Return response to client
```

### 4. Manual Scrape Trigger

```
Client Request: POST /scrape?headless=true&max_events=100
    │
    ├─> FastAPI receives request
    │
    ├─> Add scraping task to background queue
    │
    ├─> Return immediate response: "Scraping started"
    │
    └─> Background Task:
            ├─> Create database session
            ├─> Run Scraper Manager
            ├─> Save results to database
            └─> Log completion
```

## Data Flow

### Scraping Process

```
Website → Selenium WebDriver → Scraper Class → Raw Data
                                                    │
                                                    ▼
                                            Data Extraction
                                            (title, date, etc.)
                                                    │
                                                    ▼
                                            Scraper Manager
                                                    │
                                                    ▼
                                            Database Models
                                            (Event/Deal objects)
                                                    │
                                                    ▼
                                            SQLAlchemy ORM
                                                    │
                                                    ▼
                                            Database Storage
```

### API Response Process

```
Database → SQLAlchemy Query → Python Objects → Pydantic Models → JSON → Client
```

## Database Schema

### Events Table

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    date VARCHAR(100),
    location VARCHAR(300),
    category VARCHAR(100),
    price VARCHAR(100),
    url VARCHAR(500) UNIQUE,
    source VARCHAR(100) NOT NULL,
    images JSON,
    contact VARCHAR(300),
    content JSON,
    full_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_source ON events(source);
CREATE INDEX idx_events_category ON events(category);
CREATE INDEX idx_events_url ON events(url);
```

### Deals Table

```sql
CREATE TABLE deals (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    price VARCHAR(100),
    original_price VARCHAR(100),
    discount VARCHAR(50),
    url VARCHAR(500) UNIQUE,
    source VARCHAR(100) NOT NULL,
    images JSON,
    category VARCHAR(100),
    valid_until VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_deals_source ON deals(source);
CREATE INDEX idx_deals_category ON deals(category);
CREATE INDEX idx_deals_url ON deals(url);
```

## Scheduler Configuration

### Schedule Options

| Option | Cron Expression | Description |
|--------|----------------|-------------|
| `hourly` | `0 * * * *` | Every hour at :00 |
| `every_6_hours` | `0 */6 * * *` | Every 6 hours |
| `every_12_hours` | `0 */12 * * *` | Every 12 hours |
| `twice_daily` | `0 6,18 * * *` | 6 AM and 6 PM |
| `daily` | `0 2 * * *` | Daily at 2 AM |

### Scheduler Lifecycle

```
Application Start
    │
    ├─> Create BackgroundScheduler instance
    │
    ├─> Add job with CronTrigger
    │       ├─> Job ID: scraper_6h
    │       ├─> Function: scrape_job()
    │       └─> Schedule: every 6 hours
    │
    ├─> Start scheduler
    │
    └─> Scheduler runs in background thread
            │
            ├─> Wait for trigger time
            │
            ├─> Execute scrape_job()
            │
            ├─> Calculate next run time
            │
            └─> Repeat
```

## Deployment Architecture

### Single Instance (Small Scale)

```
┌─────────────────────────────────────┐
│         Cloud Platform              │
│  (Railway/Render/DigitalOcean)      │
│                                     │
│  ┌───────────────────────────────┐ │
│  │   Docker Container            │ │
│  │                               │ │
│  │  ┌─────────┐  ┌────────────┐ │ │
│  │  │   API   │  │ Scheduler  │ │ │
│  │  └─────────┘  └────────────┘ │ │
│  │                               │ │
│  │  ┌─────────────────────────┐ │ │
│  │  │      Scrapers           │ │ │
│  │  └─────────────────────────┘ │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │   PostgreSQL Database         │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Multi-Instance (Large Scale)

```
┌─────────────────────────────────────────────────────┐
│                  Load Balancer                      │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
       ┌───────▼────────┐    ┌───────▼────────┐
       │  API Instance  │    │  API Instance  │
       │   (Read Only)  │    │   (Read Only)  │
       └────────────────┘    └────────────────┘
                                      
       ┌────────────────────────────────────┐
       │      Worker Instance               │
       │  (Scraping + Scheduler Only)       │
       └────────────────────────────────────┘
                      │
                      ▼
       ┌────────────────────────────────────┐
       │   PostgreSQL (Primary)             │
       │                                    │
       │   ┌──────────────────────────┐    │
       │   │  Read Replicas (Optional)│    │
       │   └──────────────────────────┘    │
       └────────────────────────────────────┘
```

## Security Considerations

### API Security

```
Client Request
    │
    ├─> CORS Middleware (validate origin)
    │
    ├─> Rate Limiting (optional)
    │
    ├─> Authentication (optional)
    │
    ├─> Input Validation (Pydantic)
    │
    └─> Process Request
```

### Scraping Security

- Use headless mode in production
- Rotate user agents
- Respect robots.txt
- Implement rate limiting
- Handle errors gracefully

## Monitoring & Logging

### Key Metrics to Monitor

1. **Scheduler Status**
   - Is scheduler running?
   - Next run time
   - Last run success/failure

2. **Scraping Metrics**
   - Events scraped per source
   - Success/failure rate
   - Scraping duration

3. **API Metrics**
   - Request count
   - Response time
   - Error rate

4. **Database Metrics**
   - Total events/deals
   - Growth rate
   - Query performance

### Logging Flow

```
Application → Python Logger → Console/File
                                    │
                                    ▼
                            Cloud Platform Logs
                            (Railway/Render/etc.)
```

## Performance Optimization

### Database Optimization

- Index on frequently queried columns (source, category, url)
- Use connection pooling
- Implement caching (Redis) for frequent queries
- Use read replicas for scaling

### Scraping Optimization

- Run scrapers in parallel (with caution)
- Implement resume capability
- Cache scraped data temporarily
- Use headless mode to save resources

### API Optimization

- Implement pagination (skip/limit)
- Add response caching
- Use async endpoints for long operations
- Compress responses (gzip)

## Error Handling

### Scraper Errors

```
Scraper Error
    │
    ├─> Log error with traceback
    │
    ├─> Continue with next scraper
    │
    └─> Return partial results
```

### API Errors

```
API Error
    │
    ├─> Catch exception
    │
    ├─> Log error
    │
    ├─> Return appropriate HTTP status
    │       ├─> 400: Bad Request
    │       ├─> 404: Not Found
    │       ├─> 500: Internal Server Error
    │
    └─> Include error message in response
```

## Scaling Strategy

### Vertical Scaling
- Increase instance size
- More CPU/RAM for scrapers
- Faster database

### Horizontal Scaling
- Multiple API instances (read-only)
- Dedicated worker for scraping
- Database read replicas
- Load balancer

### Optimization
- Cache frequently accessed data
- Optimize database queries
- Reduce scraping frequency
- Implement incremental scraping
