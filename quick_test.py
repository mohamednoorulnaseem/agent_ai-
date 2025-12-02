"""
Quick test of Phase 3 modules directly
"""

import sys
import os

# Add the parent directory to the path so we can import modules directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\nTesting Phase 3 modules...")
print("="*60)

try:
    print("\n1. Testing auth module...")
    from auth import TokenManager, APIKeyManager, verify_credentials
    token_mgr = TokenManager()
    token = token_mgr.create_access_token({"sub": "user1", "username": "testuser", "roles": ["user"]})
    print(f"   ✓ JWT token created: {token[:20]}...")
    verified = token_mgr.verify_token(token)
    print(f"   ✓ Token verified: {verified}")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n2. Testing websocket_support module...")
    from websocket_support import ConnectionManager, EventBroadcaster
    print(f"   ✓ ConnectionManager imported")
    print(f"   ✓ EventBroadcaster imported")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n3. Testing templates module...")
    from templates import TemplateLibrary
    lib = TemplateLibrary()
    templates = lib.list_templates()
    print(f"   ✓ TemplateLibrary loaded {len(templates)} templates")
    rest_api = lib.get_template("rest_api")
    print(f"   ✓ REST API template has {len(rest_api.tasks)} tasks")
    search = lib.search_templates("web")
    print(f"   ✓ Search for 'web' found {len(search)} templates")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n4. Testing analytics module...")
    from analytics import analytics
    analytics.record_execution(1, 2.5, True, 1500)
    analytics.record_execution(1, 3.0, True, 1600)
    stats = analytics.get_execution_stats(1)
    print(f"   ✓ Recorded executions: {stats}")
    report = analytics.get_performance_report()
    print(f"   ✓ Performance report: {report['total_executions']} total executions")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n5. Testing API imports...")
    from api import app, token_manager, api_key_manager, template_library, analytics as api_analytics
    print(f"   ✓ API imports successful")
    routes = [route.path for route in app.routes]
    print(f"   ✓ FastAPI has {len(routes)} routes")
    
    # Check for new endpoints
    new_endpoints = ["/auth/login", "/templates", "/analytics"]
    for endpoint in new_endpoints:
        if any(endpoint in route for route in routes):
            print(f"   ✓ Found endpoint: {endpoint}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Phase 3 module testing complete!")
print("="*60)
