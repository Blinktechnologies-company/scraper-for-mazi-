"""
Simple test script for the API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n[1] Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_stats():
    """Test stats endpoint"""
    print("\n[2] Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_events():
    """Test get events endpoint"""
    print("\n[3] Testing get events endpoint...")
    response = requests.get(f"{BASE_URL}/events?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} events")
    if data:
        print(f"Sample event: {data[0]['title']}")
    return response.status_code == 200

def test_get_deals():
    """Test get deals endpoint"""
    print("\n[4] Testing get deals endpoint...")
    response = requests.get(f"{BASE_URL}/deals?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} deals")
    return response.status_code == 200

def test_search():
    """Test search functionality"""
    print("\n[5] Testing search...")
    response = requests.get(f"{BASE_URL}/events?search=concert&limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} events matching 'concert'")
    return response.status_code == 200

def test_filter_by_source():
    """Test filtering by source"""
    print("\n[6] Testing filter by source...")
    response = requests.get(f"{BASE_URL}/events?source=culture_gov&limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} events from culture_gov")
    return response.status_code == 200

def main():
    print("="*60)
    print("API Test Suite")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API is running: python run_api.py")
    print("="*60)
    
    tests = [
        test_health,
        test_stats,
        test_get_events,
        test_get_deals,
        test_search,
        test_filter_by_source
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*60)

if __name__ == "__main__":
    main()
