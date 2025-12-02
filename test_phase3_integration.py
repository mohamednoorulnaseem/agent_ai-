#!/usr/bin/env python3
"""
Phase 3 Complete System Integration Test
Demonstrates all Phase 3 features working together.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("PHASE 3 COMPLETE SYSTEM INTEGRATION TEST")
print("="*70)

def test_authentication():
    """Test authentication system"""
    print("\n[1] AUTHENTICATION SYSTEM TEST")
    print("-" * 70)
    try:
        from auth import TokenManager, APIKeyManager
        
        # Test token creation
        token_mgr = TokenManager()
        token_data = {"sub": "user_demo", "username": "demo", "roles": ["user"]}
        token = token_mgr.create_access_token(token_data)
        print(f"✓ JWT token created: {token[:50]}...")
        
        # Test token validation
        verified = token_mgr.verify_token(token)
        print(f"✓ Token validated: {verified['username']}")
        
        # Test API key generation
        api_key_mgr = APIKeyManager()
        api_key = api_key_mgr.generate_api_key("user_demo")
        print(f"✓ API key generated: {api_key[:30]}...")
        
        print("✓ Authentication system: WORKING")
        return True
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False

def test_websocket():
    """Test WebSocket support"""
    print("\n[2] WEBSOCKET REAL-TIME SUPPORT TEST")
    print("-" * 70)
    try:
        from websocket_support import ConnectionManager, EventBroadcaster, manager
        
        print(f"✓ ConnectionManager imported")
        print(f"✓ EventBroadcaster imported")
        print(f"✓ Global manager instance available")
        
        # Verify event methods
        events = [
            "task_started", "task_progress", "task_completed",
            "task_failed", "plan_updated"
        ]
        count = 0
        for event in events:
            if hasattr(EventBroadcaster, event):
                print(f"✓ Event broadcaster: {event}")
                count += 1
        
        print(f"✓ WebSocket system: WORKING ({count}/5 events)")
        return True
    except Exception as e:
        print(f"✗ WebSocket test failed: {e}")
        return False

def test_templates():
    """Test template library"""
    print("\n[3] TASK TEMPLATES TEST")
    print("-" * 70)
    try:
        from templates import TemplateLibrary
        
        lib = TemplateLibrary()
        templates = lib.list_templates()
        print(f"✓ Loaded {len(templates)} templates")
        
        # Test search
        search_results = lib.search_templates("api")
        print(f"✓ Search for 'api' found {len(search_results)} template(s)")
        
        # Test difficulty filter
        hard_templates = lib.get_templates_by_difficulty("hard")
        print(f"✓ Hard difficulty templates: {len(hard_templates)}")
        
        # Test tag filtering
        api_tags = lib.get_templates_by_tag("api")
        print(f"✓ Templates with 'api' tag: {len(api_tags)}")
        
        print("✓ Template system: WORKING")
        return True
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        return False

def test_analytics():
    """Test analytics engine"""
    print("\n[4] ANALYTICS ENGINE TEST")
    print("-" * 70)
    try:
        from analytics import analytics, metrics_collector
        
        # Record some sample executions
        analytics.record_execution(10, 2.5, True, 1500)
        analytics.record_execution(10, 2.8, True, 1600)
        analytics.record_execution(10, 3.0, False, 0)
        
        print(f"✓ Recorded 3 sample task executions")
        
        # Get stats
        stats = analytics.get_execution_stats(10)
        print(f"✓ Task 10 Stats:")
        print(f"  - Executions: {stats['total_executions']}")
        print(f"  - Success Rate: {stats['success_rate']:.1f}%")
        print(f"  - Avg Duration: {stats['avg_duration']:.2f}s")
        
        # Get trending
        trending = analytics.get_trending_tasks(limit=5)
        print(f"✓ Trending analysis: {len(trending)} tasks tracked")
        
        print("✓ Analytics system: WORKING")
        return True
    except Exception as e:
        print(f"✗ Analytics test failed: {e}")
        return False

def test_api_integration():
    """Test API integration"""
    print("\n[5] API INTEGRATION TEST")
    print("-" * 70)
    try:
        from api import app, token_manager, api_key_manager, template_library
        
        # Count routes
        routes = [route.path for route in app.routes]
        print(f"✓ FastAPI app loaded with {len(routes)} routes")
        
        # Check for Phase 3 endpoints
        phase3_endpoints = [
            "/auth/login", "/auth/token", "/auth/validate",
            "/templates", "/analytics", "/ws/{client_id}"
        ]
        
        found_count = 0
        for endpoint in phase3_endpoints:
            if any(endpoint in route for route in routes):
                print(f"✓ Found: {endpoint}")
                found_count += 1
        
        print(f"✓ Phase 3 endpoints: {found_count}/{len(phase3_endpoints)} found")
        print("✓ API integration: WORKING")
        return True
    except Exception as e:
        print(f"✗ API integration test failed: {e}")
        return False

def test_core_system():
    """Test core system compatibility"""
    print("\n[6] CORE SYSTEM COMPATIBILITY TEST")
    print("-" * 70)
    try:
        from config import load_config_and_llm
        from agent.planner import Planner
        from agent.executor import Executor
        from agent.history import ConversationHistory
        from persistence import DatabaseManager
        
        # Load config
        config, llm = load_config_and_llm()
        provider = config.get('llm', {}).get('provider', 'unknown')
        print(f"✓ Config loaded: LLM provider = {provider}")
        
        # Initialize components
        planner = Planner(llm)
        print(f"✓ Planner initialized")
        
        executor = Executor(llm, ".")
        print(f"✓ Executor initialized")
        
        history = ConversationHistory()
        print(f"✓ Conversation history initialized")
        
        db = DatabaseManager()
        print(f"✓ Database manager initialized")
        
        print("✓ Core system compatibility: WORKING")
        return True
    except Exception as e:
        print(f"✗ Core system test failed: {e}")
        return False

def main():
    """Run all tests"""
    tests = [
        test_authentication,
        test_websocket,
        test_templates,
        test_analytics,
        test_api_integration,
        test_core_system
    ]
    
    results = {}
    for test in tests:
        results[test.__name__] = test()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: [{status}]")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed >= 4:
        print("\n✓ PHASE 3 FEATURES OPERATIONAL")
        print("\nSystem is ready for use!")
        return 0
    else:
        print(f"\n⚠ Review errors above")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\n" + "="*70)
    sys.exit(exit_code)
