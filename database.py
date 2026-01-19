"""
Database models and connection for events and deals
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./events_deals.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Event(Base):
    """Event model"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    date = Column(String(100), nullable=True)
    location = Column(String(300), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    price = Column(String(100), nullable=True)
    url = Column(String(500), unique=True, index=True)
    source = Column(String(100), nullable=False, index=True)  # Which scraper
    images = Column(JSON, nullable=True)
    contact = Column(String(300), nullable=True)
    content = Column(JSON, nullable=True)
    full_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Deal(Base):
    """Deal model"""
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(String(100), nullable=True)
    original_price = Column(String(100), nullable=True)
    discount = Column(String(50), nullable=True)
    url = Column(String(500), unique=True, index=True)
    source = Column(String(100), nullable=False, index=True)
    images = Column(JSON, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    valid_until = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
