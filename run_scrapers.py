"""
Script to manually run all scrapers and save to database
"""
from scraper_manager import ScraperManager
from database import SessionLocal, init_db
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run all scrapers')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--max-events', type=int, default=50, help='Max events per source')
    args = parser.parse_args()
    
    print("="*60)
    print("Events & Deals Scraper")
    print("="*60)
    print(f"Headless mode: {args.headless}")
    print(f"Max events per source: {args.max_events}")
    print("="*60)
    
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Run scrapers
        manager = ScraperManager(db)
        results = manager.run_all_scrapers(
            headless=args.headless,
            max_events_per_source=args.max_events
        )
        
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        print(f"Total events saved: {results['total_events']}")
        print(f"Total deals saved: {results['total_deals']}")
        print("\nBy source:")
        for source, count in results['by_source'].items():
            print(f"  {source}: {count}")
        print("="*60)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
