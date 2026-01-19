"""
FastAPI application for events and deals
Provides REST endpoints to access scraped data
"""
from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from database import get_db, Event, Deal, init_db
from scraper_manager import ScraperManager
from scheduler import start_scheduler, stop_scheduler, get_scheduler_status

# Initialize FastAPI app
app = FastAPI(
    title="Events & Deals API",
    description="API for Greek events and deals scraped from multiple sources",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API responses
class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: Optional[str]
    location: Optional[str]
    category: Optional[str]
    price: Optional[str]
    url: Optional[str]
    source: str
    images: Optional[List[str]]
    contact: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DealResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Optional[str]
    original_price: Optional[str]
    discount: Optional[str]
    url: Optional[str]
    source: str
    images: Optional[List[str]]
    category: Optional[str]
    valid_until: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScraperStatus(BaseModel):
    status: str
    message: str
    results: Optional[dict] = None

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    start_scheduler()
    print("✓ API started successfully")
    print("✓ Background scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()
    print("✓ Scheduler stopped")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Events & Deals API",
        "version": "1.0.0",
        "endpoints": {
            "events": "/events",
            "deals": "/deals",
            "combined_events": "/combined-events",
            "scrape": "/scrape",
            "stats": "/stats",
            "scheduler": "/scheduler/status"
        }
    }

# Events endpoints
@app.get("/events", response_model=List[EventResponse])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    source: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all events with optional filtering"""
    query = db.query(Event)
    
    if source:
        query = query.filter(Event.source == source)
    
    if category:
        query = query.filter(Event.category == category)
    
    if search:
        query = query.filter(
            Event.title.contains(search) | 
            Event.description.contains(search)
        )
    
    events = query.order_by(Event.created_at.desc()).offset(skip).limit(limit).all()
    return events

@app.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Deals endpoints
@app.get("/deals", response_model=List[DealResponse])
async def get_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    source: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all deals with optional filtering"""
    query = db.query(Deal)
    
    if source:
        query = query.filter(Deal.source == source)
    
    if category:
        query = query.filter(Deal.category == category)
    
    if search:
        query = query.filter(
            Deal.title.contains(search) | 
            Deal.description.contains(search)
        )
    
    deals = query.order_by(Deal.created_at.desc()).offset(skip).limit(limit).all()
    return deals

@app.get("/deals/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: int, db: Session = Depends(get_db)):
    """Get a specific deal by ID"""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

# Statistics endpoint
@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about events and deals"""
    total_events = db.query(Event).count()
    total_deals = db.query(Deal).count()
    
    # Events by source
    events_by_source = {}
    sources = db.query(Event.source).distinct().all()
    for (source,) in sources:
        count = db.query(Event).filter(Event.source == source).count()
        events_by_source[source] = count
    
    # Events by category
    events_by_category = {}
    categories = db.query(Event.category).distinct().all()
    for (category,) in categories:
        if category:
            count = db.query(Event).filter(Event.category == category).count()
            events_by_category[category] = count
    
    return {
        "total_events": total_events,
        "total_deals": total_deals,
        "events_by_source": events_by_source,
        "events_by_category": events_by_category
    }

# Scraper endpoints
@app.post("/scrape", response_model=ScraperStatus)
async def run_scrapers(
    background_tasks: BackgroundTasks,
    headless: bool = True,
    max_events: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Trigger scrapers to run (runs in background)
    """
    def scrape_task():
        manager = ScraperManager(db)
        results = manager.run_all_scrapers(headless=headless, max_events_per_source=max_events)
        print(f"Background scraping completed: {results}")
    
    background_tasks.add_task(scrape_task)
    
    return ScraperStatus(
        status="started",
        message="Scraping started in background. Check /stats for updates."
    )

@app.post("/scrape/sync", response_model=ScraperStatus)
async def run_scrapers_sync(
    headless: bool = True,
    max_events: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Trigger scrapers to run synchronously (waits for completion)
    Warning: This may take several minutes
    """
    try:
        manager = ScraperManager(db)
        results = manager.run_all_scrapers(headless=headless, max_events_per_source=max_events)
        
        return ScraperStatus(
            status="completed",
            message="Scraping completed successfully",
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

# Scheduler status endpoint
@app.get("/scheduler/status")
async def scheduler_status():
    """Get scheduler status and next run times"""
    return get_scheduler_status()

# Combined JSON endpoint
@app.get("/combined-events")
async def get_combined_events():
    """Get the latest combined events JSON file"""
    import os
    filepath = os.path.join('scraped_data', 'combined_events.json')
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Combined events file not found. Run scrapers first.")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            events = json.load(f)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading combined events: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    scheduler_info = get_scheduler_status()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "scheduler": scheduler_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
