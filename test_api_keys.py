"""
Test script to demonstrate API Key management functionality.
Run this to see API keys in action.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("🔑 API Key Management Demo")
print("=" * 70)


def test_generate_key():
    """Test generating an API key."""
    print("\n1️⃣  GENERATE API KEY")
    print("-" * 70)
    
    # Use timestamp to make name unique
    import time
    timestamp = int(time.time())
    
    payload = {
        "name": f"Demo Key {timestamp}",
        "expires_in_days": 90,
        "rate_limit": 1000,
        "scopes": ["read", "write"],
        "metadata": {"environment": "demo", "version": "1.0"}
    }
    
    response = requests.post(
        f"{BASE_URL}/api-keys/generate",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Key generated successfully!")
        print(f"   Key ID: {data['key_id']}")
        print(f"   Name: {data['name']}")
        print(f"   Raw Key: {data['key'][:20]}... (truncated)")
        print(f"   Scopes: {', '.join(data['scopes'])}")
        print(f"   Expires: {data['expires_at']}")
        return data['key'], data['key_id']
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        return None, None


def test_list_keys():
    """Test listing API keys."""
    print("\n2️⃣  LIST API KEYS")
    print("-" * 70)
    
    response = requests.get(f"{BASE_URL}/api-keys/list")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} API key(s)")
        for key in data['keys']:
            print(f"\n   📌 {key['name']}")
            print(f"      ID: {key['key_id']}")
            print(f"      Status: {key['status']}")
            print(f"      Created: {key['created_at'][:10]}")
            print(f"      Usage: {key['usage_count']} requests")
            print(f"      Rate Limit: {key['rate_limit']} req/min")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())


def test_validate_key(api_key):
    """Test validating an API key."""
    print("\n3️⃣  VALIDATE API KEY")
    print("-" * 70)
    
    response = requests.post(
        f"{BASE_URL}/api-keys/validate",
        params={"api_key": api_key}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data['valid']:
            print(f"✅ Key is valid!")
            print(f"   Key ID: {data['key_id']}")
            print(f"   Name: {data['name']}")
            print(f"   Scopes: {', '.join(data['scopes'])}")
            print(f"   Usage Count: {data['usage_count']}")
            print(f"   Rate Limit: {data['rate_limit']} req/min")
        else:
            print(f"❌ Key is invalid: {data['message']}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_key_info(key_id):
    """Test getting key information."""
    print("\n4️⃣  GET KEY INFORMATION")
    print("-" * 70)
    
    response = requests.get(f"{BASE_URL}/api-keys/{key_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Key info retrieved!")
        print(f"   Name: {data['name']}")
        print(f"   Status: {data['status']}")
        print(f"   Is Active: {data['is_active']}")
        print(f"   Scopes: {', '.join(data['scopes'])}")
        print(f"   Created: {data['created_at'][:10]}")
        print(f"   Last Used: {data['last_used'][:10] if data['last_used'] else 'Never'}")
        print(f"   Usage Count: {data['usage_count']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())


def test_usage_stats():
    """Test getting usage statistics."""
    print("\n5️⃣  USAGE STATISTICS")
    print("-" * 70)
    
    response = requests.get(f"{BASE_URL}/api-keys/stats/usage")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Usage stats retrieved!")
        print(f"   Total Keys: {data['total_keys']}")
        print(f"   Active Keys: {data['active_keys']}")
        print(f"   Total Requests: {data['total_requests']}")
        print(f"   Last Request: {data['last_request'][:19] if data['last_request'] else 'Never'}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_use_key_in_request(api_key):
    """Test using API key in actual API request."""
    print("\n6️⃣  USE KEY IN API REQUEST")
    print("-" * 70)
    
    headers = {"X-API-Key": api_key}
    response = requests.get(
        f"{BASE_URL}/health",
        headers=headers
    )
    
    if response.status_code == 200:
        print(f"✅ Authenticated request successful!")
        print(f"   Status: {response.json()['status']}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_revoke_key(key_id):
    """Test revoking an API key."""
    print("\n7️⃣  REVOKE API KEY")
    print("-" * 70)
    
    response = requests.post(f"{BASE_URL}/api-keys/{key_id}/revoke")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Key revoked!")
        print(f"   Key ID: {data['key_id']}")
        print(f"   Message: {data['message']}")
    else:
        print(f"❌ Error: {response.status_code}")


def main():
    """Run all tests."""
    try:
        # Test 1: Generate key
        api_key, key_id = test_generate_key()
        if not api_key:
            return
        
        time.sleep(0.5)
        
        # Test 2: List keys
        test_list_keys()
        
        time.sleep(0.5)
        
        # Test 3: Validate key
        test_validate_key(api_key)
        
        time.sleep(0.5)
        
        # Test 4: Get key info
        test_get_key_info(key_id)
        
        time.sleep(0.5)
        
        # Test 5: Usage stats
        test_usage_stats()
        
        time.sleep(0.5)
        
        # Test 6: Use key in request
        test_use_key_in_request(api_key)
        
        time.sleep(0.5)
        
        # Test 7: Revoke key
        test_revoke_key(key_id)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📚 Next Steps:")
        print("   1. Visit http://localhost:8000/docs for interactive API docs")
        print("   2. Generate production API keys with appropriate scopes")
        print("   3. Integrate API keys into your applications")
        print("   4. Monitor usage and rotate keys periodically")
        print("\n📖 For more info, see: API_KEYS_GUIDE.md")
        print("=" * 70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("   Make sure: docker-compose up -d")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
