#!/usr/bin/env python3
"""
API integration tests - test FastAPI endpoints
"""

import asyncio
import sys
import os
import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from fastapi.testclient import TestClient


def test_health_endpoint():
    """Test the health check endpoint"""
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", f"Expected healthy, got {data}"
    print("✅ Health endpoint working")


def test_root_endpoint():
    """Test the root endpoint"""
    client = TestClient(app)
    response = client.get("/")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "message" in data, "Missing message in response"
    assert "endpoints" in data, "Missing endpoints in response"
    print("✅ Root endpoint working")


async def test_markets_endpoint():
    """Test the markets endpoint"""
    client = TestClient(app)
    
    # Use smaller limit for faster testing
    response = client.get("/markets?limit=5")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    # Should have all platform keys
    assert "polymarket" in data, "Missing polymarket"
    assert "kalshi" in data, "Missing kalshi"
    assert "manifold" in data, "Missing manifold"
    assert "total" in data, "Missing total"
    
    # Each should be a list
    assert isinstance(data["polymarket"], list), "polymarket should be list"
    assert isinstance(data["kalshi"], list), "kalshi should be list"
    assert isinstance(data["manifold"], list), "manifold should be list"
    
    print(f"✅ Markets endpoint working (total: {data['total']} markets)")


async def test_arbitrage_endpoint():
    """Test the arbitrage endpoint"""
    client = TestClient(app)
    
    # Use smaller limit for faster testing
    response = client.get("/arbitrage?limit=10&min_roi=1.0")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    # Should have required keys
    assert "opportunities" in data, "Missing opportunities"
    assert "count" in data, "Missing count"
    assert "markets_analyzed" in data, "Missing markets_analyzed"
    
    # Types check
    assert isinstance(data["opportunities"], list), "opportunities should be list"
    assert isinstance(data["count"], int), "count should be int"
    
    print(f"✅ Arbitrage endpoint working ({data['count']} opportunities found)")
    
    # If opportunities found, validate structure
    if data["opportunities"]:
        opp = data["opportunities"][0]
        assert "market1" in opp, "Missing market1"
        assert "market2" in opp, "Missing market2"
        assert "arbitrage" in opp, "Missing arbitrage"
        assert "roi_percentage" in opp["arbitrage"], "Missing roi_percentage"
        print(f"   Best ROI: {opp['arbitrage']['roi_percentage']}%")


def run_api_tests():
    """Run all API integration tests"""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║              API INTEGRATION TESTS                           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    try:
        print("Testing API endpoints...\n")
        
        test_health_endpoint()
        test_root_endpoint()
        asyncio.run(test_markets_endpoint())
        asyncio.run(test_arbitrage_endpoint())
        
        print("\n✅ All API integration tests passed!\n")
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False


if __name__ == "__main__":
    success = run_api_tests()
    sys.exit(0 if success else 1)
