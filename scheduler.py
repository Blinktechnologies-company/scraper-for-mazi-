"""
Background scheduler for continuous scraping
Runs scrapers at scheduled intervals
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from scraper_manager import ScraperManager
from database import SessionLocal, init_db
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScraperScheduler:
    """Manages scheduled scraping tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        
    def scrape_job(self):
        """Job that runs the scrapers"""
        logger.info("="*60)
        logger.info("Starting scheduled scraping job")
        logger.info("="*60)
        
        db = SessionLocal()
        
        try:
            manager = ScraperManager(db)
            
            # Get max events from environment or default
            max_events = int(os.getenv('SCRAPER_MAX_EVENTS', 100))
            headless = os.getenv('HEADLESS_MODE', 'True').lower() == 'true'
            
            results = manager.run_all_scrapers(
                headless=headless,
                max_events_per_source=max_events
            )
            
            logger.info("Scraping job completed successfully")
            logger.info(f"Total events: {results['total_events']}")
            logger.info(f"By source: {results['by_source']}")
            
        except Exception as e:
            logger.error(f"Error in scraping job: {e}", exc_info=True)
        
        finally:
            db.close()
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        # Initialize database
        init_db()
        
        # Get schedule from environment or use defaults
        schedule_type = os.getenv('SCRAPER_SCHEDULE', 'daily')
        
        if schedule_type == 'hourly':
            # Run every hour
            self.scheduler.add_job(
                self.scrape_job,
                CronTrigger(minute=0),
                id='scraper_hourly',
                name='Hourly Scraper',
                replace_existing=True
            )
            logger.info("Scheduled: Hourly scraping (every hour at :00)")
            
        elif schedule_type == 'every_6_hours':
            # Run every 6 hours
            self.scheduler.add_job(
                self.scrape_job,
                CronTrigger(hour='*/6', minute=0),
                id='scraper_6h',
                name='6-Hour Scraper',
                replace_existing=True
            )
            logger.info("Scheduled: Every 6 hours scraping")
            
        elif schedule_type == 'every_12_hours':
            # Run every 12 hours
            self.scheduler.add_job(
                self.scrape_job,
                CronTrigger(hour='*/12', minute=0),
                id='scraper_12h',
                name='12-Hour Scraper',
                replace_existing=True
            )
            logger.info("Scheduled: Every 12 hours scraping")
            
        elif schedule_type == 'twice_daily':
            # Run twice a day (6 AM and 6 PM)
            self.scheduler.add_job(
                self.scrape_job,
                CronTrigger(hour='6,18', minute=0),
                id='scraper_twice',
                name='Twice Daily Scraper',
                replace_existing=True
            )
            logger.info("Scheduled: Twice daily scraping (6 AM and 6 PM)")
            
        else:  # daily (default)
            # Run once a day at 2 AM
            self.scheduler.add_job(
                self.scrape_job,
                CronTrigger(hour=2, minute=0),
                id='scraper_daily',
                name='Daily Scraper',
                replace_existing=True
            )
            logger.info("Scheduled: Daily scraping (2 AM)")
        
        # Run immediately on startup if configured
        run_on_startup = os.getenv('SCRAPER_RUN_ON_STARTUP', 'False').lower() == 'true'
        if run_on_startup:
            logger.info("Running initial scrape on startup...")
            self.scrape_job()
        
        self.scheduler.start()
        self.is_running = True
        logger.info("Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
    
    def get_jobs(self):
        """Get list of scheduled jobs"""
        return self.scheduler.get_jobs()

# Global scheduler instance
scheduler_instance = ScraperScheduler()

def start_scheduler():
    """Start the global scheduler"""
    scheduler_instance.start()

def stop_scheduler():
    """Stop the global scheduler"""
    scheduler_instance.stop()

def get_scheduler_status():
    """Get scheduler status"""
    return {
        'running': scheduler_instance.is_running,
        'jobs': [
            {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in scheduler_instance.get_jobs()
        ]
    }
