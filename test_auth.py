#!/usr/bin/env python3
"""
Simple test script for authentication endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:3002/api"

def test_register():
    """Test user registration"""
    print("Testing registration...")
    
    data = {
        "first_name": "שרה",
        "last_name": "לוי",
        "email": "sarah@example.com",
        "password": "secret123",
        "phone": "050-9876543",
        "country": "ישראל",
        "city": "ירושלים"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        return response.json()
    return None

def test_login():
    """Test user login"""
    print("\nTesting login...")
    
    data = {
        "email": "sarah@example.com",
        "password": "secret123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return response.json()
    return None

def test_get_profile(auth_response):
    """Test getting user profile"""
    print("\nTesting get profile...")
    
    headers = {
        "Authorization": f"Bearer {auth_response['access_token']}"
    }
    
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_refresh_token(auth_response):
    """Test token refresh"""
    print("\nTesting token refresh...")
    
    data = {
        "refresh_token": auth_response['refresh_token']
    }
    
    response = requests.post(f"{BASE_URL}/auth/refresh", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("=== ShabbesGuests Backend Test ===\n")
    
    # Test registration
    auth_response = test_register()
    
    if auth_response:
        # Test login
        login_response = test_login()
        
        if login_response:
            # Test get profile
            test_get_profile(login_response)
            
            # Test refresh token
            test_refresh_token(login_response)
    
    print("\n=== Test Complete ===")
