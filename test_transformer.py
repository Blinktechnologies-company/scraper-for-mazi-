"""
Test the data transformer with sample data
"""
from data_transformer import DataTransformer
import json

def test_transformer():
    """Test transformer with sample data from different sources"""
    
    transformer = DataTransformer()
    
    # Sample data from different sources
    sample_data = {
        'culture_gov': [
            {
                'title': 'Ancient Greek Theater Performance',
                'content': ['A magnificent performance of ancient Greek tragedy', 'Featuring renowned actors'],
                'date': '15/02/2026',
                'location': 'Odeon of Herodes Atticus, Athens',
                'url': 'https://culture.gov.gr/event1',
                'images': ['https://culture.gov.gr/image1.jpg', 'https://culture.gov.gr/image2.jpg']
            }
        ],
        'visitgreece': [
            {
                'title': 'Santorini Wine Festival',
                'description': 'Experience the finest wines of Santorini',
                'date': '2026-03-20',
                'location': 'Santorini, Greece',
                'category': 'Festival',
                'price': 'Free',
                'url': 'https://visitgreece.gr/event2',
                'images': ['https://visitgreece.gr/wine.jpg']
            }
        ],
        'pigolampides': [
            {
                'title': 'Athens Street Food Tour',
                'excerpt': 'Discover the best street food in Athens',
                'date': '10 March 2026',
                'categories': ['Food', 'Cultural'],
                'url': 'https://pigolampides.gr/post1',
                'images': [{'src': 'https://pigolampides.gr/food.jpg', 'alt': 'Street food'}]
            }
        ],
        'more_events': [
            {
                'title': 'Τα μυστικά της ανωτερότητας των Ιταλικών ζυμαρικών',
                'description': 'Masterclass για ζυμαρικά',
                'date': '2026-02-09',
                'location': 'Technopolis - City of Athens, Peiraios 100 & Persefonis, Gazi',
                'category': 'Conference',
                'price': '30',
                'url': 'https://www.more.com/gr-en/tickets/conference/masterclass-zymarikon/',
                'images': ['https://www.more.com/image.png']
            }
        ]
    }
    
    print("="*60)
    print("Testing Data Transformer")
    print("="*60)
    
    # Transform data
    transformed = transformer.transform_all_events(sample_data)
    
    print(f"\n✓ Transformed {len(transformed)} events")
    
    # Save to file
    filepath = transformer.save_combined_json(transformed, 'test_combined_events.json')
    
    # Display sample
    print("\n" + "="*60)
    print("Sample Transformed Events:")
    print("="*60)
    
    for i, event in enumerate(transformed[:3], 1):
        print(f"\n[{i}] {event['title']}")
        print(f"    Category: {event['category']} ({event['categoryColor']})")
        print(f"    Date: {event['date']}")
        print(f"    Region: {event['region']}")
        print(f"    Source: {event['source']}")
        print(f"    Price: {event['price']}")
        print(f"    Image: {event['image'][:50] if event['image'] else 'None'}...")
    
    # Show full JSON for first event
    print("\n" + "="*60)
    print("Full JSON Format (First Event):")
    print("="*60)
    print(json.dumps(transformed[0], indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("✓ Test complete!")
    print(f"✓ Output saved to: {filepath}")
    print("="*60)

if __name__ == "__main__":
    test_transformer()
