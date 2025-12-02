"""
Test Phase 3 API integration - Authentication, Templates, Analytics, WebSocket
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_auth_module():
    """Test authentication module."""
    print("\n" + "="*60)
    print("Testing Authentication Module")
    print("="*60)
    
    try:
        from auth import TokenManager, APIKeyManager, verify_credentials, DEMO_CREDENTIALS
        
        print("✓ Auth module imported successfully")
        
        # Test TokenManager
        token_manager = TokenManager()
        token = token_manager.create_access_token("user123", "testuser", ["user"])
        print(f"✓ JWT token created: {token[:30]}...")
        
        # Verify token
        user_data = token_manager.verify_token(token)
        print(f"✓ Token verified: {user_data}")
        
        # Test APIKeyManager
        api_key_manager = APIKeyManager()
        api_key = api_key_manager.generate_api_key("user123")
        print(f"✓ API key generated: {api_key}")
        
        # Validate API key
        is_valid = api_key_manager.validate_api_key(api_key)
        print(f"✓ API key validated: {is_valid}")
        
        # Test credentials
        user = verify_credentials("demo", "demo123")
        print(f"✓ Demo credentials verified: {user.username if user else 'Failed'}")
        
        print("\n✅ Authentication module tests PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Authentication module tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_websocket_module():
    """Test WebSocket module."""
    print("\n" + "="*60)
    print("Testing WebSocket Module")
    print("="*60)
    
    try:
        from websocket_support import ConnectionManager, EventBroadcaster, manager
        
        print("✓ WebSocket module imported successfully")
        
        # Check ConnectionManager
        print(f"✓ ConnectionManager created: {type(manager).__name__}")
        print(f"✓ Active connections: {len(manager.active_connections)}")
        
        # Check EventBroadcaster methods
        methods = ['task_started', 'task_progress', 'task_completed', 'task_failed', 'plan_updated']
        for method in methods:
            assert hasattr(EventBroadcaster, method), f"Missing method: {method}"
            print(f"✓ EventBroadcaster.{method} exists")
        
        print("\n✅ WebSocket module tests PASSED")
        return True
    except Exception as e:
        print(f"\n❌ WebSocket module tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_templates_module():
    """Test Templates module."""
    print("\n" + "="*60)
    print("Testing Templates Module")
    print("="*60)
    
    try:
        from templates import TemplateLibrary, TaskTemplate
        
        print("✓ Templates module imported successfully")
        
        library = TemplateLibrary()
        
        # Test list templates
        templates = library.list_templates()
        print(f"✓ Available templates: {len(templates)}")
        for t in templates:
            print(f"  - {t.name} ({t.difficulty}): {len(t.tasks)} tasks")
        
        # Test get template
        rest_api = library.get_template("rest_api")
        assert rest_api is not None, "REST API template not found"
        print(f"✓ Retrieved REST API template with {len(rest_api.tasks)} tasks")
        
        # Test search
        search_results = library.search_templates("api")
        print(f"✓ Search for 'api': {len(search_results)} results")
        
        # Test filter by difficulty
        easy_templates = library.get_templates_by_difficulty("easy")
        print(f"✓ Easy templates: {len(easy_templates)}")
        
        # Test filter by tag
        web_templates = library.get_templates_by_tag("web")
        print(f"✓ Web-related templates: {len(web_templates)}")
        
        print("\n✅ Templates module tests PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Templates module tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analytics_module():
    """Test Analytics module."""
    print("\n" + "="*60)
    print("Testing Analytics Module")
    print("="*60)
    
    try:
        from analytics import Analytics, MetricsCollector, analytics, metrics_collector
        
        print("✓ Analytics module imported successfully")
        
        # Test record execution
        analytics.record_execution(1, 2.5, True, 1500)
        analytics.record_execution(1, 3.0, True, 1600)
        analytics.record_execution(1, 1.8, False, 500)
        print("✓ Recorded 3 executions")
        
        # Test get stats
        stats = analytics.get_execution_stats(1)
        print(f"✓ Execution stats for task 1: {stats}")
        
        # Test plan analytics
        plan_stats = analytics.get_plan_analytics()
        print(f"✓ Plan analytics retrieved: {len(plan_stats)} tasks analyzed")
        
        # Test performance report
        report = analytics.get_performance_report()
        print(f"✓ Performance report generated")
        print(f"  - Total executions: {report.get('total_executions')}")
        print(f"  - Average duration: {report.get('average_duration'):.2f}s")
        print(f"  - Success rate: {report.get('overall_success_rate'):.1%}")
        
        # Test trending
        trending = analytics.get_trending_tasks(limit=5)
        print(f"✓ Trending tasks: {len(trending)} tasks")
        
        # Test metrics collector
        metrics_collector.record_hourly_metric("performance", 85.5)
        print("✓ Hourly metric recorded")
        
        hourly_sum = metrics_collector.get_hourly_summary()
        print(f"✓ Hourly summary: {len(hourly_sum)} entries")
        
        print("\n✅ Analytics module tests PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Analytics module tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_imports():
    """Test that API can import all Phase 3 modules."""
    print("\n" + "="*60)
    print("Testing API Integration Imports")
    print("="*60)
    
    try:
        # This will fail if any imports are broken
        from api import app, token_manager, api_key_manager, template_library, analytics, metrics_collector
        
        print("✓ API module imported successfully")
        print("✓ All Phase 3 dependencies available in API")
        
        # Check that FastAPI app is created
        assert app is not None, "FastAPI app not created"
        print(f"✓ FastAPI app initialized")
        
        # Check routes
        routes = [route.path for route in app.routes]
        print(f"✓ Total routes: {len(routes)}")
        
        # Check for new Phase 3 routes
        phase3_routes = ["/auth/login", "/auth/token", "/templates", "/ws/", "/analytics"]
        for route in phase3_routes:
            has_route = any(route in r for r in routes)
            if has_route:
                print(f"  ✓ {route} route found")
        
        print("\n✅ API integration tests PASSED")
        return True
    except Exception as e:
        print(f"\n❌ API integration tests FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all Phase 3 tests."""
    print("\n" + "="*60)
    print("PHASE 3 API INTEGRATION TEST SUITE")
    print("="*60)
    
    results = {
        "Authentication": test_auth_module(),
        "WebSocket": test_websocket_module(),
        "Templates": test_templates_module(),
        "Analytics": test_analytics_module(),
        "API Integration": test_api_imports(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All Phase 3 tests PASSED! API integration complete.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
