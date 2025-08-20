#!/usr/bin/env python3
"""
Test script for host endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:3002/api"

def test_locations():
    """Test location endpoints"""
    print("=== Testing Locations ===\n")
    
    # Test countries
    print("Testing GET /locations/countries...")
    response = requests.get(f"{BASE_URL}/locations/countries")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test cities by country
    print("\nTesting GET /locations/cities/country/IL...")
    response = requests.get(f"{BASE_URL}/locations/cities/country/IL")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test search
    print("\nTesting GET /locations/search?query=jerusalem...")
    response = requests.get(f"{BASE_URL}/locations/search?query=jerusalem")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_hosts_public():
    """Test public host endpoints"""
    print("\n=== Testing Public Host Endpoints ===\n")
    
    # Test get all hosts
    print("Testing GET /hosts...")
    response = requests.get(f"{BASE_URL}/hosts")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test get hosts by country
    print("\nTesting GET /hosts/country/IL...")
    response = requests.get(f"{BASE_URL}/hosts/country/IL")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_auth_and_hosts():
    """Test authentication and protected host endpoints"""
    print("\n=== Testing Authentication and Protected Host Endpoints ===\n")
    
    # First, register a user
    print("1. Registering a new user...")
    register_data = {
        "first_name": "משה",
        "last_name": "לוי",
        "email": "moshe@example.com",
        "password": "secret123",
        "phone": "050-1111111",
        "country": "ישראל",
        "city": "ירושלים"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Register Status: {response.status_code}")
    if response.status_code == 201:
        auth_data = response.json()
        access_token = auth_data['access_token']
        print("✅ Registration successful")
    else:
        print(f"❌ Registration failed: {response.json()}")
        return
    
    # Test get my host profile (should return 404 initially)
    print("\n2. Testing GET /hosts/me (should return 404)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/hosts/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test create host profile
    print("\n3. Testing POST /hosts (create host profile)...")
    host_data = {
        "country_place_id": "IL",
        "city_place_id": "IL-JM",
        "area": "העיר העתיקה",
        "address": "רחוב יפו 123",
        "description": "בית חם ומזמין בשבת",
        "bio": "אני אוהב לארח אנשים בשבת",
        "max_guests": 8,
        "hosting_type": ["shabbos_meal", "sleepover"],
        "kashrut_level": "mehadrin",
        "languages": ["he", "en"],
        "is_always_available": False,
        "available": True
    }
    
    response = requests.post(f"{BASE_URL}/hosts", json=host_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        host_response = response.json()
        host_id = host_response['id']
        print("✅ Host profile created successfully")
        
        # Test get my host profile (should work now)
        print("\n4. Testing GET /hosts/me (should work now)...")
        response = requests.get(f"{BASE_URL}/hosts/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Test update host profile
        print("\n5. Testing PUT /hosts/{host_id} (update host profile)...")
        update_data = {
            "max_guests": 10,
            "bio": "בית חם ומזמין בשבת - עודכן!",
            "available": False
        }
        
        response = requests.put(f"{BASE_URL}/hosts/{host_id}", json=update_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Test upload photo
        print("\n6. Testing POST /hosts/upload-photo...")
        # Create a mock file
        files = {'photo': ('test.jpg', b'fake_image_data', 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/hosts/upload-photo", files=files, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Test get host by ID
        print("\n7. Testing GET /hosts/{host_id}...")
        response = requests.get(f"{BASE_URL}/hosts/{host_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Test delete host profile
        print("\n8. Testing DELETE /hosts/{host_id}...")
        response = requests.delete(f"{BASE_URL}/hosts/{host_id}", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # Verify deletion
        print("\n9. Testing GET /hosts/me (should return 404 after deletion)...")
        response = requests.get(f"{BASE_URL}/hosts/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print("❌ Failed to create host profile")

def test_error_cases():
    """Test error cases"""
    print("\n=== Testing Error Cases ===\n")
    
    # Test unauthorized access
    print("1. Testing GET /hosts/me without token...")
    response = requests.get(f"{BASE_URL}/hosts/me")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test invalid host ID
    print("\n2. Testing GET /hosts/invalid-id...")
    response = requests.get(f"{BASE_URL}/hosts/invalid-id")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("=== ShabbesGuests Host System Test ===\n")
    
    # Test locations first
    test_locations()
    
    # Test public host endpoints
    test_hosts_public()
    
    # Test authentication and protected endpoints
    test_auth_and_hosts()
    
    # Test error cases
    test_error_cases()
    
    print("\n=== Test Complete ===")
