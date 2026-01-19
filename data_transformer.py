"""
Data transformer to standardize all scraped data into unified format
Combines data from all scrapers and formats before database storage
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import re

class DataTransformer:
    """Transform scraped data into standardized format"""
    
    def __init__(self):
        self.next_id = 1
        self.category_colors = {
            'Cultural': '#F39C12',
            'Theater': '#9B59B6',
            'Music': '#E74C3C',
            'Sports': '#3498DB',
            'Cinema': '#1ABC9C',
            'Festival': '#E67E22',
            'Exhibition': '#95A5A6',
            'Conference': '#34495E',
            'Dance': '#9B59B6',
            'Concert': '#E74C3C',
            'Other': '#7F8C8D'
        }
    
    def transform_all_events(self, events_by_source: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Transform events from all sources into unified format
        
        Args:
            events_by_source: Dict with source name as key and list of events as value
                Example: {
                    'culture_gov': [...],
                    'visitgreece': [...],
                    'pigolampides': [...],
                    'more_events': [...]
                }
        
        Returns:
            List of standardized event dictionaries
        """
        all_transformed = []
        
        for source, events in events_by_source.items():
            print(f"Transforming {len(events)} events from {source}...")
            
            for event in events:
                try:
                    transformed = self.transform_event(event, source)
                    if transformed:
                        all_transformed.append(transformed)
                except Exception as e:
                    print(f"  Error transforming event: {e}")
                    continue
        
        print(f"Total transformed events: {len(all_transformed)}")
        return all_transformed
    
    def transform_event(self, event: Dict, source: str) -> Optional[Dict]:
        """Transform a single event to standardized format"""
        
        # Extract and clean data
        title = self._clean_text(event.get('title', ''))
        if not title:
            return None
        
        description = self._extract_description(event)
        date = self._extract_date(event)
        region = self._extract_region(event)
        category = self._extract_category(event)
        location = self._extract_location(event)
        venue = self._extract_venue(event)
        url = event.get('url', '')
        image = self._extract_image(event)
        price = self._extract_price(event)
        
        # Build standardized event
        standardized = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'date': date,
            'schedule': None,  # Can be enhanced later
            'region': region,
            'category': category,
            'categoryColor': self.category_colors.get(category, '#7F8C8D'),
            'subCategories': None,  # Can be enhanced later
            'location': location,
            'venue': venue,
            'venueUrl': None,  # Can be enhanced later
            'url': url,
            'eventUrl': url,
            'image': image,
            'imageUrl': image,
            'price': price,
            'maxCapacity': 100,  # Default value
            'targetAges': None,  # Can be enhanced later
            'specialFeatures': None,  # Can be enhanced later
            'source': self._format_source_name(source)
        }
        
        self.next_id += 1
        return standardized
    
    def _clean_text(self, text: Any) -> str:
        """Clean and normalize text"""
        if not text:
            return ''
        
        if isinstance(text, list):
            text = ' '.join(str(t) for t in text if t)
        
        text = str(text).strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _extract_description(self, event: Dict) -> str:
        """Extract description from various fields"""
        # Try multiple fields
        desc = (
            event.get('description') or
            event.get('excerpt') or
            event.get('summary') or
            ''
        )
        
        # If description is a list, join it
        if isinstance(desc, list):
            desc = ' '.join(str(d) for d in desc if d)
        
        # If still no description, try content field
        if not desc and event.get('content'):
            content = event['content']
            if isinstance(content, list):
                desc = ' '.join(str(c) for c in content[:3] if c)  # First 3 paragraphs
            elif isinstance(content, str):
                desc = content[:500]  # First 500 chars
        
        # If still no description, use full_text
        if not desc and event.get('full_text'):
            desc = str(event['full_text'])[:500]
        
        return self._clean_text(desc)
    
    def _extract_date(self, event: Dict) -> Optional[str]:
        """Extract and format date"""
        date = event.get('date')
        
        if not date:
            return None
        
        date = str(date).strip()
        
        # Try to parse and standardize date format to YYYY-MM-DD
        try:
            # Handle various date formats
            date_patterns = [
                r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
                r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
                r'(\d{1,2})\.(\d{1,2})\.(\d{4})',  # DD.MM.YYYY
                r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, date)
                if match:
                    groups = match.groups()
                    if len(groups[0]) == 4:  # YYYY-MM-DD format
                        year, month, day = groups
                    else:  # DD/MM/YYYY format
                        day, month, year = groups
                    
                    # Ensure proper formatting
                    return f"{year}-{int(month):02d}-{int(day):02d}"
        except:
            pass
        
        # Return as-is if can't parse
        return date
    
    def _extract_region(self, event: Dict) -> str:
        """Extract region from location or venue"""
        location = event.get('location', '')
        venue = event.get('venue', '')
        
        # Common Greek regions
        regions = {
            'athens': 'Αττική',
            'attiki': 'Αττική',
            'attica': 'Αττική',
            'thessaloniki': 'Κεντρική Μακεδονία',
            'macedonia': 'Κεντρική Μακεδονία',
            'crete': 'Κρήτη',
            'patras': 'Δυτική Ελλάδα',
            'ioannina': 'Ήπειρος',
            'iwannina': 'Ήπειρος',
            'larissa': 'Θεσσαλία',
            'volos': 'Θεσσαλία',
            'heraklion': 'Κρήτη',
            'rhodes': 'Νότιο Αιγαίο',
            'corfu': 'Ιόνια Νησιά',
            'mykonos': 'Νότιο Αιγαίο',
            'santorini': 'Νότιο Αιγαίο'
        }
        
        text = f"{location} {venue}".lower()
        
        for key, region in regions.items():
            if key in text:
                return region
        
        return 'Αττική'  # Default to Athens
    
    def _extract_category(self, event: Dict) -> str:
        """Extract and standardize category"""
        category = event.get('category', '')
        
        if isinstance(category, list):
            category = category[0] if category else ''
        
        category = str(category).strip().lower()
        
        # Map to standard categories
        category_mapping = {
            'theater': 'Theater',
            'theatre': 'Theater',
            'θέατρο': 'Theater',
            'music': 'Music',
            'μουσική': 'Music',
            'concert': 'Concert',
            'συναυλία': 'Concert',
            'cinema': 'Cinema',
            'κινηματογράφος': 'Cinema',
            'movie': 'Cinema',
            'sports': 'Sports',
            'αθλητισμός': 'Sports',
            'dance': 'Dance',
            'χορός': 'Dance',
            'exhibition': 'Exhibition',
            'έκθεση': 'Exhibition',
            'festival': 'Festival',
            'φεστιβάλ': 'Festival',
            'conference': 'Conference',
            'συνέδριο': 'Conference',
            'cultural': 'Cultural',
            'πολιτιστικό': 'Cultural'
        }
        
        for key, value in category_mapping.items():
            if key in category:
                return value
        
        # Try to infer from title or description
        title = str(event.get('title', '')).lower()
        desc = str(event.get('description', '')).lower()
        text = f"{title} {desc}"
        
        for key, value in category_mapping.items():
            if key in text:
                return value
        
        return 'Cultural'  # Default category
    
    def _extract_location(self, event: Dict) -> str:
        """Extract location"""
        location = event.get('location', '')
        
        if not location:
            location = event.get('venue', '')
        
        return self._clean_text(location)
    
    def _extract_venue(self, event: Dict) -> str:
        """Extract venue"""
        venue = event.get('venue', '')
        
        if not venue:
            venue = event.get('location', '')
        
        return self._clean_text(venue)
    
    def _extract_image(self, event: Dict) -> Optional[str]:
        """Extract primary image URL"""
        images = event.get('images', [])
        
        if isinstance(images, list) and images:
            # Return first image
            return str(images[0]) if images[0] else None
        elif isinstance(images, str):
            return images
        
        # Try image field
        image = event.get('image')
        if image:
            return str(image)
        
        return None
    
    def _extract_price(self, event: Dict) -> int:
        """Extract price as integer (0 for free)"""
        price = event.get('price', '')
        
        if not price:
            return 0
        
        price_str = str(price).lower()
        
        # Check if free
        if any(word in price_str for word in ['free', 'δωρεάν', 'ελεύθερη']):
            return 0
        
        # Try to extract number
        try:
            # Remove currency symbols and text
            numbers = re.findall(r'\d+', price_str)
            if numbers:
                return int(numbers[0])
        except:
            pass
        
        return 0
    
    def _format_source_name(self, source: str) -> str:
        """Format source name for display"""
        source_names = {
            'culture_gov': 'Culture.gov.gr',
            'visitgreece': 'VisitGreece.gr',
            'pigolampides': 'Pigolampides.gr',
            'more_events': 'More.com'
        }
        
        return source_names.get(source, source.title())
    
    def save_combined_json(self, events: List[Dict], filename: str = 'combined_events.json'):
        """Save combined events to JSON file"""
        os.makedirs('scraped_data', exist_ok=True)
        filepath = os.path.join('scraped_data', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Combined events saved to: {filepath}")
        return filepath

# Example usage
if __name__ == "__main__":
    # Test with sample data
    transformer = DataTransformer()
    
    sample_events = {
        'culture_gov': [
            {
                'title': 'Test Event',
                'description': 'Test description',
                'date': '2026-02-15',
                'location': 'Athens',
                'url': 'https://example.com/event1',
                'images': ['https://example.com/image1.jpg']
            }
        ]
    }
    
    transformed = transformer.transform_all_events(sample_events)
    print(json.dumps(transformed, indent=2, ensure_ascii=False))
