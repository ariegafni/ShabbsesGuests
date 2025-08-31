import unittest
from datetime import date
from app import create_app
from storage.postgres_db import get_connection


class AccommodationRequestsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user and get auth token
        self.test_user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        # Register test user
        response = self.client.post('/api/auth/register', 
                                  json=self.test_user_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Login to get token
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        response = self.client.post('/api/auth/login',
                                  json=login_data,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.auth_token = response.json['token']
        
        # Create test host
        self.test_host_data = {
            "country_place_id": "ChIJLQMo04-0AhURqHqZLcJ8V8M",  # Israel
            "city_place_id": "ChIJ0V94rPlMHRURWnD9HpBqHmM",  # Tel Aviv
            "area": "Test Area",
            "address": "Test Address",
            "description": "Test Description",
            "bio": "Test Bio",
            "max_guests": 2,
            "hosting_type": ["shabbat_meal"],
            "kashrut_level": "kosher",
            "languages": ["Hebrew", "English"]
        }
        
        response = self.client.post('/api/hosts',
                                  json=self.test_host_data,
                                  headers={'Authorization': f'Bearer {self.auth_token}'},
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.test_host_id = response.json['id']

    def tearDown(self):
        # Clean up test data
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM accommodation_requests WHERE guest_id IN (SELECT id FROM users WHERE email = %s)", (self.test_user_data["email"],))
        cur.execute("DELETE FROM hosts WHERE user_id IN (SELECT id FROM users WHERE email = %s)", (self.test_user_data["email"],))
        cur.execute("DELETE FROM users WHERE email = %s", (self.test_user_data["email"],))
        conn.commit()
        cur.close()
        conn.close()

    def test_create_accommodation_request(self):
        """Test creating a new accommodation request"""
        request_data = {
            "host": self.test_host_id,
            "requested_date": date.today().isoformat(),
            "message": "Test request message"
        }
        
        response = self.client.post('/api/hosting-requests',
                                  json=request_data,
                                  headers={'Authorization': f'Bearer {self.auth_token}'},
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertIn('id', data)
        self.assertEqual(data['guest_id'], self.get_user_id())
        self.assertEqual(data['host_id'], self.test_host_id)
        self.assertEqual(data['status'], 'pending')

    def test_get_my_accommodation_requests(self):
        """Test getting user's accommodation requests"""
        # First create a request
        request_data = {
            "host": self.test_host_id,
            "requested_date": date.today().isoformat(),
            "message": "Test request message"
        }
        
        self.client.post('/api/hosting-requests',
                        json=request_data,
                        headers={'Authorization': f'Bearer {self.auth_token}'},
                        content_type='application/json')
        
        # Then get all requests
        response = self.client.get('/api/hosting-requests/my-guest-requests',
                                 headers={'Authorization': f'Bearer {self.auth_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_host_accommodation_requests(self):
        """Test getting accommodation requests for a host"""
        # First create a request
        request_data = {
            "host": self.test_host_id,
            "requested_date": date.today().isoformat(),
            "message": "Test request message"
        }
        
        self.client.post('/api/hosting-requests',
                        json=request_data,
                        headers={'Authorization': f'Bearer {self.auth_token}'},
                        content_type='application/json')
        
        # Then get host requests
        response = self.client.get('/api/hosting-requests/my-host-requests',
                                 headers={'Authorization': f'Bearer {self.auth_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_update_request_status(self):
        """Test updating accommodation request status"""
        # First create a request
        request_data = {
            "host": self.test_host_id,
            "requested_date": date.today().isoformat(),
            "message": "Test request message"
        }
        
        response = self.client.post('/api/hosting-requests',
                                  json=request_data,
                                  headers={'Authorization': f'Bearer {self.auth_token}'},
                                  content_type='application/json')
        request_id = response.json['id']
        
        # Update status to accepted
        status_data = {"status": "accepted"}
        response = self.client.put(f'/api/hosting-requests/{request_id}/respond',
                                 json=status_data,
                                 headers={'Authorization': f'Bearer {self.auth_token}'},
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['status'], 'accepted')

    def test_delete_accommodation_request(self):
        """Test deleting an accommodation request"""
        # First create a request
        request_data = {
            "host": self.test_host_id,
            "requested_date": date.today().isoformat(),
            "message": "Test request message"
        }
        
        response = self.client.post('/api/hosting-requests',
                                  json=request_data,
                                  headers={'Authorization': f'Bearer {self.auth_token}'},
                                  content_type='application/json')
        request_id = response.json['id']
        
        # Delete the request
        response = self.client.delete(f'/api/hosting-requests/{request_id}',
                                    headers={'Authorization': f'Bearer {self.auth_token}'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def get_user_id(self):
        """Helper method to get current user ID"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (self.test_user_data["email"],))
        user_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return str(user_id)


if __name__ == '__main__':
    unittest.main()
