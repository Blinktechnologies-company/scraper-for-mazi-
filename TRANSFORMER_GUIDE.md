# Data Transformer Guide

## Overview

The Data Transformer standardizes all scraped data into a unified format before saving to the database. This ensures consistency across all data sources.

## Standardized Format

Every event is transformed into this format:

```json
{
  "id": 1342,
  "title": "Event Title",
  "description": "Event description...",
  "date": "2026-02-09",
  "schedule": null,
  "region": "Αττική",
  "category": "Cultural",
  "categoryColor": "#F39C12",
  "subCategories": null,
  "location": "Venue address",
  "venue": "Venue name",
  "venueUrl": null,
  "url": "https://example.com/event",
  "eventUrl": "https://example.com/event",
  "image": "https://example.com/image.jpg",
  "imageUrl": "https://example.com/image.jpg",
  "price": 0,
  "maxCapacity": 100,
  "targetAges": null,
  "specialFeatures": null,
  "source": "More.com"
}
```

## Field Mapping

### From Different Sources

The transformer intelligently extracts data from various field names:

| Standard Field | Possible Source Fields |
|---------------|------------------------|
| `title` | title |
| `description` | description, excerpt, summary, content, full_text |
| `date` | date (auto-formatted to YYYY-MM-DD) |
| `location` | location, venue |
| `venue` | venue, location |
| `category` | category, categories (auto-mapped) |
| `image` | images[0], image |
| `price` | price (converted to integer, 0 for free) |
| `region` | Inferred from location/venue |

## Categories

Standard categories with colors:

| Category | Color | Greek Terms |
|----------|-------|-------------|
| Cultural | #F39C12 | πολιτιστικό |
| Theater | #9B59B6 | θέατρο |
| Music | #E74C3C | μουσική |
| Concert | #E74C3C | συναυλία |
| Sports | #3498DB | αθλητισμός |
| Cinema | #1ABC9C | κινηματογράφος |
| Festival | #E67E22 | φεστιβάλ |
| Exhibition | #95A5A6 | έκθεση |
| Conference | #34495E | συνέδριο |
| Dance | #9B59B6 | χορός |
| Other | #7F8C8D | - |

## Regions

Automatically detected from location text:

- **Αττική** (Attica) - Athens, Attiki
- **Κεντρική Μακεδονία** - Thessaloniki, Macedonia
- **Κρήτη** (Crete) - Heraklion, Crete
- **Δυτική Ελλάδα** - Patras
- **Ήπειρος** - Ioannina
- **Θεσσαλία** - Larissa, Volos
- **Νότιο Αιγαίο** - Rhodes, Mykonos, Santorini
- **Ιόνια Νησιά** - Corfu

Default: Αττική

## Date Formatting

Automatically converts various date formats to `YYYY-MM-DD`:

**Input formats supported:**
- `2026-02-09` (already standard)
- `09/02/2026` (DD/MM/YYYY)
- `09.02.2026` (DD.MM.YYYY)
- `09-02-2026` (DD-MM-YYYY)
- `9 February 2026` (text format)

**Output:** Always `2026-02-09`

## Price Extraction

Converts price strings to integers:

- `"Free"` → `0`
- `"Δωρεάν"` → `0`
- `"30€"` → `30`
- `"From 10"` → `10`
- `""` (empty) → `0`

## How It Works

### 1. Scraping Phase

```
Scrapers run → Raw data collected → Stored by source
```

### 2. Transformation Phase

```
Raw data → DataTransformer → Standardized format
```

### 3. Storage Phase

```
Standardized data → Combined JSON file → Database
```

## Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Scraper Manager                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │  Run All Scrapers (4 sources)   │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   Collect Raw Events by Source  │
        │   {                             │
        │     'culture_gov': [...],       │
        │     'visitgreece': [...],       │
        │     'pigolampides': [...],      │
        │     'more_events': [...]        │
        │   }                             │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │      Data Transformer           │
        │  - Extract fields               │
        │  - Clean text                   │
        │  - Format dates                 │
        │  - Map categories               │
        │  - Detect regions               │
        │  - Extract images               │
        │  - Convert prices               │
        └─────────────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   Standardized Events Array     │
        │   [                             │
        │     {id: 1, title: "...", ...}, │
        │     {id: 2, title: "...", ...}, │
        │     ...                         │
        │   ]                             │
        └─────────────────────────────────┘
                          │
                          ├──────────────────────┐
                          ▼                      ▼
        ┌─────────────────────────┐  ┌──────────────────┐
        │  Save Combined JSON     │  │  Save to Database│
        │  combined_events.json   │  │  (PostgreSQL)    │
        └─────────────────────────┘  └──────────────────┘
```

## Usage

### Automatic (via Scraper Manager)

The transformer runs automatically when you use the scraper manager:

```python
from scraper_manager import ScraperManager
from database import SessionLocal

db = SessionLocal()
manager = ScraperManager(db)
results = manager.run_all_scrapers(headless=True, max_events_per_source=100)

# Results include:
# - results['total_events']: Number saved to DB
# - results['combined_json_path']: Path to combined JSON file
```

### Manual (standalone)

You can also use the transformer directly:

```python
from data_transformer import DataTransformer

transformer = DataTransformer()

# Your raw events from scrapers
events_by_source = {
    'culture_gov': [...],
    'visitgreece': [...],
    'pigolampides': [...],
    'more_events': [...]
}

# Transform
standardized = transformer.transform_all_events(events_by_source)

# Save to JSON
transformer.save_combined_json(standardized, 'my_events.json')
```

## Testing

Test the transformer with sample data:

```bash
python test_transformer.py
```

This will:
1. Create sample events from each source
2. Transform them to standardized format
3. Save to `test_combined_events.json`
4. Display sample output

## API Endpoints

### Get Combined JSON

```bash
GET /combined-events
```

Returns the latest combined events JSON file.

**Example:**
```bash
curl http://localhost:8000/combined-events
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Event Title",
    "description": "...",
    "date": "2026-02-09",
    ...
  },
  ...
]
```

## File Locations

- **Combined JSON**: `scraped_data/combined_events.json`
- **Test Output**: `scraped_data/test_combined_events.json`
- **Individual Source JSONs**: `scraped_data/<source>_events.json`

## Customization

### Add New Category

Edit `data_transformer.py`:

```python
self.category_colors = {
    'Cultural': '#F39C12',
    'YourNewCategory': '#HEXCOLOR',
    ...
}

category_mapping = {
    'your_keyword': 'YourNewCategory',
    ...
}
```

### Add New Region

Edit `data_transformer.py`:

```python
regions = {
    'your_city': 'Your Region Name',
    ...
}
```

### Customize Field Extraction

Override methods in `DataTransformer` class:

```python
def _extract_description(self, event: Dict) -> str:
    # Your custom logic
    pass
```

## Benefits

1. **Consistency** - All events have the same structure
2. **Clean Data** - Automatic text cleaning and formatting
3. **Easy Integration** - Standard format works with any frontend
4. **Flexibility** - Easy to add new sources
5. **Debugging** - Combined JSON file for inspection
6. **Database Ready** - Format matches database schema

## Troubleshooting

### Missing Fields

If some fields are empty:
- Check source data has the information
- Add field mapping in transformer
- Check field name variations

### Wrong Category

If category is incorrect:
- Add keyword to `category_mapping`
- Check title/description for category hints

### Date Format Issues

If dates aren't parsing:
- Add date pattern to `_extract_date()`
- Check source date format

### Region Detection

If region is wrong:
- Add location keywords to `regions` dict
- Check location/venue text

## Example Output

See `scraped_data/combined_events.json` after running scrapers for real examples.
