"""
Example client script showing how to use the HTTPS-to-HTTP proxy

This script demonstrates how your Vercel frontend should call the proxy.
"""

import requests
import json

# Configuration
PROXY_URL = "https://your-koyeb-app.koyeb.app"  # Replace with your Koyeb URL
# For local testing:
# PROXY_URL = "http://localhost:8000"

def test_health_check():
    """Test if proxy is running"""
    print("🔍 Testing health check...")
    response = requests.get(f"{PROXY_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_backend_status():
    """Check if backend is reachable"""
    print("🔍 Testing backend status...")
    response = requests.get(f"{PROXY_URL}/api/backend-status")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_get_request(endpoint="/get"):
    """Test GET request through proxy"""
    print(f"📤 Testing GET request to {endpoint}...")
    response = requests.get(f"{PROXY_URL}{endpoint}", params={"test": "value"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_post_request(endpoint="/post", data=None):
    """Test POST request through proxy"""
    if data is None:
        data = {"message": "Hello from proxy", "timestamp": "2024-01-01"}
    
    print(f"📤 Testing POST request to {endpoint}...")
    response = requests.post(
        f"{PROXY_URL}{endpoint}",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_custom_api():
    """Test your custom API endpoint"""
    print("📤 Testing custom API endpoint...")
    endpoint = "/api/users"  # Replace with your actual endpoint
    response = requests.get(f"{PROXY_URL}{endpoint}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}\n")


# Frontend JavaScript Examples
FRONTEND_EXAMPLES = """
// Example 1: Simple GET request
fetch('https://your-koyeb-app.koyeb.app/api/users')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// Example 2: POST request with JSON
fetch('https://your-koyeb-app.koyeb.app/api/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John',
    email: 'john@example.com'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));

// Example 3: Using axios (if installed)
axios.get('https://your-koyeb-app.koyeb.app/api/users')
  .then(response => console.log(response.data))
  .catch(error => console.error(error));

// Example 4: POST with axios
axios.post('https://your-koyeb-app.koyeb.app/api/data', {
  name: 'Jane',
  email: 'jane@example.com'
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
"""


if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI HTTPS-to-HTTP Proxy - Client Examples")
    print("=" * 60)
    print()
    
    try:
        # Test proxy connectivity
        test_health_check()
        
        # Check backend
        try:
            test_backend_status()
        except Exception as e:
            print(f"⚠️  Backend check failed: {e}\n")
        
        # Test GET request (using httpbin for demo)
        try:
            test_get_request()
        except Exception as e:
            print(f"❌ GET request failed: {e}")
            print("   (This is expected if your backend doesn't have /get endpoint)\n")
        
        # Test POST request
        try:
            test_post_request()
        except Exception as e:
            print(f"❌ POST request failed: {e}")
            print("   (This is expected if your backend doesn't have /post endpoint)\n")
        
        print("=" * 60)
        print("📝 Frontend JavaScript Examples:")
        print("=" * 60)
        print(FRONTEND_EXAMPLES)
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to proxy at {PROXY_URL}")
        print("   Make sure the proxy is running and accessible")
    except Exception as e:
        print(f"❌ Error: {e}")
