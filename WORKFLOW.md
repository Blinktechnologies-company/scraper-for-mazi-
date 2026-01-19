# Complete Workflow Guide

## Overview

This document explains the complete workflow from scraping to API delivery.

---

## 🔄 Automatic Workflow (Scheduled)

### When Scheduler Triggers

```
1. Scheduler Trigger (e.g., every 6 hours)
        ↓
2. Scraper Manager Starts
        ↓
3. Run All Scrapers Sequentially
        ├─→ Culture.gov Scraper
        │       ├─ Navigate to website
        │       ├─ Load all events
        │       ├─ Extract data
        │       └─ Return raw events
        │
        ├─→ VisitGreece Scraper
        │       └─ (same process)
        │
        ├─→ Pigolampides Scraper
        │       └─ (same process)
        │
        └─→ More.com Scraper
                └─ (same process)
        ↓
4. Collect Raw Events by Source
   {
     'culture_gov': [event1, event2, ...],
     'visitgreece': [event1, event2, ...],
     'pigolampides': [event1, event2, ...],
     'more_events': [event1, event2, ...]
   }
        ↓
5. Data Transformer
        ├─ Clean text
        ├─ Format dates → YYYY-MM-DD
        ├─ Map categories → Standard names
        ├─ Detect regions → Greek regions
        ├─ Extract images → First image URL
        ├─ Convert prices → Integer (0 for free)
        └─ Assign IDs → Sequential
        ↓
6. Standardized Events Array
   [
     {id: 1, title: "...", date: "2026-02-09", ...},
     {id: 2, title: "...", date: "2026-02-10", ...},
     ...
   ]
        ↓
7. Save to Two Locations
        ├─→ Combined JSON File
        │   scraped_data/combined_events.json
        │
        └─→ Database (PostgreSQL/SQLite)
            ├─ Check for duplicates (by URL)
            ├─ Insert new events
            └─ Commit transaction
        ↓
8. Log Results
   ✓ Total events: 450
   ✓ By source: {culture_gov: 120, visitgreece: 180, ...}
   ✓ Combined JSON: scraped_data/combined_events.json
        ↓
9. Wait for Next Trigger
```

---

## 🎯 Manual Workflow (API Trigger)

### When User Calls POST /scrape

```
1. API Receives Request
   POST /scrape?headless=true&max_events=100
        ↓
2. Add to Background Queue
        ↓
3. Return Immediate Response
   {"status": "started", "message": "Scraping started in background"}
        ↓
4. Background Task Runs
   (Same as automatic workflow steps 2-8)
        ↓
5. User Can Check Progress
   GET /scheduler/status
   GET /stats
```

---

## 📊 Data Transformation Details

### Example: Culture.gov Event

**Raw Data (from scraper):**
```json
{
  "title": "Ancient Greek Theater",
  "content": [
    "A magnificent performance",
    "Featuring renowned actors"
  ],
  "date": "15/02/2026",
  "location": "Odeon of Herodes Atticus, Athens",
  "url": "https://culture.gov.gr/event1",
  "images": [
    "https://culture.gov.gr/image1.jpg",
    "https://culture.gov.gr/image2.jpg"
  ],
  "full_text": "Long text content..."
}
```

**Transformed Data:**
```json
{
  "id": 1,
  "title": "Ancient Greek Theater",
  "description": "A magnificent performance Featuring renowned actors",
  "date": "2026-02-15",
  "schedule": null,
  "region": "Αττική",
  "category": "Theater",
  "categoryColor": "#9B59B6",
  "subCategories": null,
  "location": "Odeon of Herodes Atticus, Athens",
  "venue": "Odeon of Herodes Atticus, Athens",
  "venueUrl": null,
  "url": "https://culture.gov.gr/event1",
  "eventUrl": "https://culture.gov.gr/event1",
  "image": "https://culture.gov.gr/image1.jpg",
  "imageUrl": "https://culture.gov.gr/image1.jpg",
  "price": 0,
  "maxCapacity": 100,
  "targetAges": null,
  "specialFeatures": null,
  "source": "Culture.gov.gr"
}
```

**Transformations Applied:**
1. ✅ Description: Joined content array
2. ✅ Date: `15/02/2026` → `2026-02-15`
3. ✅ Region: Detected "Athens" → "Αττική"
4. ✅ Category: Detected "Theater" from title
5. ✅ Category Color: Mapped to `#9B59B6`
6. ✅ Image: Extracted first image
7. ✅ Price: No price found → `0`
8. ✅ Source: Formatted to "Culture.gov.gr"

---

## 🌐 API Access Workflow

### Client Requests Events

```
1. Client Makes Request
   GET /events?category=Theater&limit=20
        ↓
2. API Receives Request
        ↓
3. Validate Parameters
   ✓ category: valid
   ✓ limit: within range (1-200)
        ↓
4. Query Database
   SELECT * FROM events
   WHERE category = 'Theater'
   ORDER BY created_at DESC
   LIMIT 20
        ↓
5. Serialize Results (Pydantic)
   Convert DB objects → JSON
        ↓
6. Return Response
   [
     {id: 1, title: "...", ...},
     {id: 2, title: "...", ...},
     ...
   ]
```

### Client Requests Combined JSON

```
1. Client Makes Request
   GET /combined-events
        ↓
2. API Receives Request
        ↓
3. Read JSON File
   scraped_data/combined_events.json
        ↓
4. Return File Contents
   [all events in standardized format]
```

---

## 🔍 Search & Filter Workflow

### Example: Search for "concert" in Athens

```
1. Request
   GET /events?search=concert&region=Αττική
        ↓
2. Build Query
   SELECT * FROM events
   WHERE (title LIKE '%concert%' OR description LIKE '%concert%')
   AND content->>'region' = 'Αττική'
   ORDER BY created_at DESC
        ↓
3. Execute Query
        ↓
4. Return Matching Events
```

---

## 📅 Scheduler Workflow

### Initialization

```
1. API Starts
        ↓
2. Initialize Database
   Create tables if not exist
        ↓
3. Start Scheduler
        ├─ Load schedule from env (SCRAPER_SCHEDULE)
        ├─ Create cron trigger
        └─ Register scraping job
        ↓
4. Scheduler Running
   ✓ Next run: 2026-01-19 18:00:00
```

### Job Execution

```
1. Cron Trigger Fires
   (e.g., every 6 hours at :00)
        ↓
2. Execute Scraping Job
   (See Automatic Workflow above)
        ↓
3. Calculate Next Run Time
   Current: 12:00
   Next: 18:00 (6 hours later)
        ↓
4. Wait for Next Trigger
```

---

## 🐳 Docker Workflow

### Startup

```
1. docker-compose up
        ↓
2. Start PostgreSQL Container
   ✓ Database ready
        ↓
3. Start API Container
        ├─ Install dependencies
        ├─ Initialize database
        ├─ Start scheduler
        └─ Start FastAPI server
        ↓
4. Services Running
   ✓ API: http://localhost:8000
   ✓ Database: localhost:5432
   ✓ Scheduler: Active
```

---

## ☁️ Cloud Deployment Workflow

### Railway Example

```
1. Push Code to GitHub
        ↓
2. Railway Detects Changes
        ↓
3. Build Docker Image
   ├─ Install Chrome
   ├─ Install Python dependencies
   └─ Copy application code
        ↓
4. Deploy Container
   ├─ Set environment variables
   ├─ Connect to PostgreSQL
   └─ Start application
        ↓
5. Application Running
   ✓ API: https://your-app.railway.app
   ✓ Scheduler: Active
   ✓ Database: Connected
        ↓
6. Continuous Operation
   ├─ Scheduler runs on schedule
   ├─ API serves requests
   └─ Auto-restart on failure
```

---

## 🔄 Complete Lifecycle

### Day 1: Initial Setup

```
1. Deploy to Railway
2. Scheduler starts
3. Initial scrape runs (if SCRAPER_RUN_ON_STARTUP=True)
4. ~400 events collected
5. Combined JSON created
6. Database populated
7. API ready for requests
```

### Day 2-∞: Continuous Operation

```
Every 6 hours:
  ├─ Scheduler triggers
  ├─ Scrapers run
  ├─ New events collected
  ├─ Data transformed
  ├─ Combined JSON updated
  ├─ Database updated (new events only)
  └─ API serves latest data

Anytime:
  ├─ Clients query API
  ├─ Get latest events
  └─ Display in frontend
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTINUOUS OPERATION                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  Scheduler   │ ← Every 6 hours
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                    Scraper Manager                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────┐│
│  │Culture.gov │  │VisitGreece │  │Pigolampides│  │More.com││
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └────┬───┘│
└────────┼───────────────┼───────────────┼──────────────┼─────┘
         │               │               │              │
         └───────────────┴───────────────┴──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Raw Events Dict  │
                    │  by Source       │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Data Transformer │
                    │  - Clean         │
                    │  - Format        │
                    │  - Standardize   │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Standardized     │
                    │ Events Array     │
                    └─────────┬────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
          ┌──────────────────┐  ┌──────────────┐
          │  Combined JSON   │  │  Database    │
          │  File            │  │  (Postgres)  │
          └──────────────────┘  └──────────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   FastAPI        │
                    │   Endpoints      │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Your Frontend  │
                    │   / Clients      │
                    └──────────────────┘
```

---

## 🎯 Key Points

1. **Automatic**: Runs on schedule without intervention
2. **Standardized**: All data in consistent format
3. **Dual Storage**: JSON file + Database
4. **API Access**: Multiple endpoints for different needs
5. **Monitoring**: Built-in status and statistics
6. **Scalable**: Easy to add more scrapers or sources
7. **Reliable**: Error handling and retry logic
8. **Cloud Ready**: Deploy anywhere with Docker

---

## 📝 Summary

The system operates in a continuous loop:

1. ⏰ **Scheduler triggers** at configured intervals
2. 🕷️ **Scrapers collect** data from 4 sources
3. 🔀 **Transformer standardizes** all data
4. 💾 **Storage saves** to JSON + Database
5. 🚀 **API serves** data to clients
6. 🔁 **Repeat** on next trigger

All while providing:
- Real-time monitoring
- Manual trigger capability
- Flexible querying
- Clean, consistent data

**Your events are always fresh and ready to use!**
