"""
Unified scraper manager that runs all scrapers and saves to database
"""
from sqlalchemy.orm import Session
from database import Event, Deal
from datetime import datetime
import json
import os

# Import all scrapers
from culture_final_scraper import CultureFinalScraper
from visitgreece_detailed_scraper import VisitGreeceDetailedScraper
from pigolampides_scraper import PigolampidesScraper
from more_events_scraper_optimized import MoreEventsScraperOptimized

# Import data transformer
from data_transformer import DataTransformer

class ScraperManager:
    """Manages all scrapers and database operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.scrapers = {
            'culture_gov': CultureFinalScraper,
            'visitgreece': VisitGreeceDetailedScraper,
            'pigolampides': PigolampidesScraper,
            'more_events': MoreEventsScraperOptimized
        }
    
    def run_all_scrapers(self, headless=True, max_events_per_source=50):
        """Run all scrapers, transform data, and save to database"""
        results = {
            'total_events': 0,
            'total_deals': 0,
            'by_source': {},
            'combined_json_path': None
        }
        
        print("="*60)
        print("Starting all scrapers...")
        print("="*60)
        
        # Dictionary to store raw events from each source
        events_by_source = {}
        
        # Run Culture.gov scraper
        try:
            print("\n[1/4] Running Culture.gov scraper...")
            scraper = CultureFinalScraper(headless=headless)
            events = scraper.scrape_all_events(max_events=max_events_per_source)
            events_by_source['culture_gov'] = events
            print(f"✓ Scraped {len(events)} events from Culture.gov")
        except Exception as e:
            print(f"✗ Error with Culture.gov scraper: {e}")
            events_by_source['culture_gov'] = []
        
        # Run VisitGreece scraper
        try:
            print("\n[2/4] Running VisitGreece scraper...")
            scraper = VisitGreeceDetailedScraper(headless=headless)
            events = scraper.scrape_events_with_details(max_events=max_events_per_source)
            events_by_source['visitgreece'] = events
            print(f"✓ Scraped {len(events)} events from VisitGreece")
        except Exception as e:
            print(f"✗ Error with VisitGreece scraper: {e}")
            events_by_source['visitgreece'] = []
        
        # Run Pigolampides scraper
        try:
            print("\n[3/4] Running Pigolampides scraper...")
            scraper = PigolampidesScraper(headless=headless)
            posts = scraper.scrape_all_posts(max_posts=max_events_per_source)
            events_by_source['pigolampides'] = posts
            print(f"✓ Scraped {len(posts)} posts from Pigolampides")
        except Exception as e:
            print(f"✗ Error with Pigolampides scraper: {e}")
            events_by_source['pigolampides'] = []
        
        # Run More Events scraper
        try:
            print("\n[4/4] Running More Events scraper...")
            scraper = MoreEventsScraperOptimized(headless=headless)
            events = scraper.scrape_all_events(max_events=max_events_per_source, resume=False)
            events_by_source['more_events'] = events
            print(f"✓ Scraped {len(events)} events from More Events")
        except Exception as e:
            print(f"✗ Error with More Events scraper: {e}")
            events_by_source['more_events'] = []
        
        # Transform all events to standardized format
        print("\n" + "="*60)
        print("Transforming data to standardized format...")
        print("="*60)
        
        transformer = DataTransformer()
        standardized_events = transformer.transform_all_events(events_by_source)
        
        # Save combined JSON file
        combined_json_path = transformer.save_combined_json(standardized_events)
        results['combined_json_path'] = combined_json_path
        
        # Save to database
        print("\n" + "="*60)
        print("Saving to database...")
        print("="*60)
        
        saved_count = self.save_standardized_events(standardized_events)
        results['total_events'] = saved_count
        
        # Count by source
        for source in events_by_source.keys():
            source_count = sum(1 for e in standardized_events if e.get('source', '').lower().replace('.', '').replace('gr', '').strip() in source)
            results['by_source'][source] = source_count
        
        print("\n" + "="*60)
        print(f"✓ Scraping complete!")
        print(f"  Total events: {results['total_events']}")
        print(f"  Combined JSON: {results['combined_json_path']}")
        print(f"  By source: {results['by_source']}")
        print("="*60)
        
        return results
    
    def save_standardized_events(self, events):
        """Save standardized events to database"""
        saved_count = 0
        
        for event_data in events:
            try:
                # Check if event already exists by URL
                url = event_data.get('url') or event_data.get('eventUrl')
                if url:
                    existing = self.db.query(Event).filter(Event.url == url).first()
                    if existing:
                        continue
                
                # Create new event from standardized format
                event = Event(
                    title=event_data.get('title', 'Untitled'),
                    description=event_data.get('description'),
                    date=event_data.get('date'),
                    location=event_data.get('location') or event_data.get('venue'),
                    category=event_data.get('category'),
                    price=str(event_data.get('price', 0)),
                    url=url,
                    source=event_data.get('source', 'Unknown'),
                    images=[event_data.get('image')] if event_data.get('image') else [],
                    contact=None,
                    content={'region': event_data.get('region'), 'venue': event_data.get('venue')},
                    full_text=None
                )
                
                self.db.add(event)
                self.db.commit()
                saved_count += 1
                
            except Exception as e:
                print(f"  Error saving event: {e}")
                self.db.rollback()
                continue
        
        return saved_count
    
    def save_events(self, events, source):
        """Legacy method - kept for backward compatibility"""
        saved_count = 0
        
        for event_data in events:
            try:
                # Check if event already exists by URL
                url = event_data.get('url')
                if url:
                    existing = self.db.query(Event).filter(Event.url == url).first()
                    if existing:
                        continue
                
                # Create new event
                event = Event(
                    title=event_data.get('title', 'Untitled'),
                    description=self._get_description(event_data),
                    date=event_data.get('date'),
                    location=event_data.get('location'),
                    category=event_data.get('category') or self._extract_category(event_data),
                    price=event_data.get('price'),
                    url=url,
                    source=source,
                    images=event_data.get('images', []),
                    contact=event_data.get('contact'),
                    content=event_data.get('content'),
                    full_text=event_data.get('full_text')
                )
                
                self.db.add(event)
                self.db.commit()
                saved_count += 1
                
            except Exception as e:
                print(f"  Error saving event: {e}")
                self.db.rollback()
                continue
        
        return saved_count
    
    def save_deals(self, deals, source):
        """Save deals to database"""
        saved_count = 0
        
        for deal_data in deals:
            try:
                # Check if deal already exists by URL
                url = deal_data.get('url')
                if url:
                    existing = self.db.query(Deal).filter(Deal.url == url).first()
                    if existing:
                        continue
                
                # Create new deal
                deal = Deal(
                    title=deal_data.get('title', 'Untitled'),
                    description=deal_data.get('description'),
                    price=deal_data.get('price'),
                    original_price=deal_data.get('original_price'),
                    discount=deal_data.get('discount'),
                    url=url,
                    source=source,
                    images=deal_data.get('images', []),
                    category=deal_data.get('category'),
                    valid_until=deal_data.get('valid_until')
                )
                
                self.db.add(deal)
                self.db.commit()
                saved_count += 1
                
            except Exception as e:
                print(f"  Error saving deal: {e}")
                self.db.rollback()
                continue
        
        return saved_count
    
    def _get_description(self, event_data):
        """Extract description from various fields"""
        if event_data.get('description'):
            return event_data['description']
        
        if event_data.get('excerpt'):
            return event_data['excerpt']
        
        if event_data.get('content'):
            content = event_data['content']
            if isinstance(content, list) and content:
                return ' '.join(content[:3])  # First 3 paragraphs
            elif isinstance(content, str):
                return content[:500]
        
        return None
    
    def _extract_category(self, event_data):
        """Try to extract category from various fields"""
        if event_data.get('categories'):
            cats = event_data['categories']
            if isinstance(cats, list) and cats:
                return cats[0]
            elif isinstance(cats, str):
                return cats
        
        return None
