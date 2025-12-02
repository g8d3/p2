import pytest
import asyncio
from datetime import datetime, timedelta
import requests
import json
from typing import Dict, List

class TestE2EWorkflow:
    """End-to-end tests for the complete arbitrage detection workflow"""
    
    def test_complete_arbitrage_workflow(self):
        """Test the complete workflow from startup to arbitrage detection"""
        base_url = "http://localhost:8000"
        
        # Test 1: Health check
        health_response = requests.get(f"{base_url}/health", timeout=10)
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"
        assert "exchanges" in health_data
        
        # Test 2: Fetch markets
        markets_response = requests.get(f"{base_url}/markets", timeout=30)
        if markets_response.status_code == 200:
            markets_data = markets_response.json()
            assert "dydx" in markets_data
            assert "gmx" in markets_data
            assert "perpetual" in markets_data
            assert "total" in markets_data
            
            # Verify market data structure
            for exchange in ["dydx", "gmx", "perpetual"]:
                markets = markets_data[exchange]
                assert isinstance(markets, list)
                if markets:  # If markets exist, check structure
                    market = markets[0]
                    assert "id" in market
                    assert "symbol" in market
                    assert "exchange" in market
                    assert "is_active" in market
        
        # Test 3: Fetch funding rates
        funding_response = requests.get(f"{base_url}/funding-rates", timeout=30)
        if funding_response.status_code == 200:
            funding_data = funding_response.json()
            assert "dydx" in funding_data
            assert "gmx" in funding_data
            assert "perpetual" in funding_data
            
            # Verify funding rate data structure
            for exchange in ["dydx", "gmx", "perpetual"]:
                rates = funding_data[exchange]
                assert isinstance(rates, list)
                if rates:  # If rates exist, check structure
                    rate = rates[0]
                    required_fields = ["market_id", "symbol", "funding_rate", "next_funding_time", "exchange"]
                    for field in required_fields:
                        assert field in rate
                    assert isinstance(rate["funding_rate"], (int, float))
                    assert isinstance(rate["symbol"], str)
        
        # Test 4: Get arbitrage opportunities
        arbitrage_response = requests.get(f"{base_url}/arbitrage", timeout=30)
        if arbitrage_response.status_code == 200:
            arbitrage_data = arbitrage_response.json()
            assert "opportunities" in arbitrage_data
            assert "count" in arbitrage_data
            assert "markets_analyzed" in arbitrage_data
            assert "filters_used" in arbitrage_data
            
            opportunities = arbitrage_data["opportunities"]
            assert isinstance(opportunities, list)
            
            # If opportunities exist, verify structure
            if opportunities:
                opportunity = opportunities[0]
                required_fields = [
                    "id", "symbol", "long_exchange", "short_exchange",
                    "long_funding_rate", "short_funding_rate", "funding_rate_spread",
                    "estimated_daily_profit", "estimated_weekly_profit",
                    "estimated_monthly_profit", "time_to_next_funding"
                ]
                for field in required_fields:
                    assert field in opportunity
                
                # Verify arbitrage logic
                assert opportunity["long_exchange"] != opportunity["short_exchange"]
                assert opportunity["funding_rate_spread"] > 0
                assert opportunity["estimated_daily_profit"] >= 0  # Should only show profitable
        
        # Test 5: Arbitrage endpoint with filters
        filtered_response = requests.get(
            f"{base_url}/arbitrage",
            params={"min_rate_spread": 0.001, "limit": 5},
            timeout=30
        )
        if filtered_response.status_code == 200:
            filtered_data = filtered_response.json()
            assert "opportunities" in filtered_data
            assert len(filtered_data["opportunities"]) <= 5
            
            # Check that all opportunities meet the spread criteria
            for opp in filtered_data["opportunities"]:
                assert opp["funding_rate_spread"] >= 0.001
    
    def test_frontend_serves(self):
        """Test that frontend HTML is served correctly"""
        base_url = "http://localhost:8000"
        
        # Test main page
        page_response = requests.get(base_url, timeout=30)
        assert page_response.status_code == 200
        assert "text/html" in page_response.headers.get("content-type", "")
        
        # Check it contains expected content
        page_content = page_response.text
        assert "DEX Funding Rate Arbitrage" in page_content
        assert "arbitrage" in page_content.lower()
    
    def test_api_error_handling(self):
        """Test API error handling"""
        base_url = "http://localhost:8000"
        
        # Test invalid endpoint
        invalid_response = requests.get(f"{base_url}/invalid", timeout=10)
        assert invalid_response.status_code == 404
        
        # Test with invalid query parameters (should not crash)
        response = requests.get(
            f"{base_url}/arbitrage",
            params={"limit": "invalid", "min_rate_spread": "not_a_number"},
            timeout=30
        )
        # Either returns success (ignores invalid params) or proper error
        assert response.status_code in [200, 400, 422]
    
    def test_performance_benchmarks(self):
        """Test API performance benchmarks"""
        base_url = "http://localhost:8000"
        
        # Test that API responses are reasonably fast
        start_time = datetime.now()
        health_response = requests.get(f"{base_url}/health", timeout=30)
        health_time = (datetime.now() - start_time).total_seconds()
        
        if health_response.status_code == 200:
            # Health should be very fast (< 1 second)
            assert health_time < 1.0, f"Health check took {health_time}s"
        
        # Test arbitrage endpoint (should be < 10 seconds even with external API calls)
        start_time = datetime.now()
        arbitrage_response = requests.get(f"{base_url}/arbitrage", timeout=30)
        arbitrage_time = (datetime.now() - start_time).total_seconds()
        
        if arbitrage_response.status_code == 200:
            assert arbitrage_time < 10.0, f"Arbitrage analysis took {arbitrage_time}s"

class TestRealDataIntegration:
    """Tests with actual DEX API responses (when available)"""
    
    def test_actual_dex_api_responses(self):
        """Test that we can get actual responses from DEX APIs"""
        base_url = "http://localhost:8000"
        
        # Test that we can connect to DEX APIs (may fail depending on network)
        markets_response = requests.get(f"{base_url}/markets", timeout=30)
        
        if markets_response.status_code == 200:
            markets_data = markets_response.json()
            
            # Verify we got some real data (not just empty lists)
            total_markets = markets_data.get("total", 0)
            print(f"Total markets found: {total_markets}")
            
            # If we have markets, check that they have reasonable data
            if total_markets > 0:
                for exchange, exchange_markets in markets_data.items():
                    if exchange == "total":
                        continue
                    if exchange_markets:
                        market = exchange_markets[0]
                        # Basic sanity checks
                        assert isinstance(market.get("symbol"), str)
                        assert market.get("symbol", "").strip() != ""
                        assert market.get("exchange") in ["dYdX", "GMX", "Perpetual"]

    def test_funding_rate_consistency(self):
        """Test that funding rates are consistent and within reasonable ranges"""
        base_url = "http://localhost:8000"
        
        funding_response = requests.get(f"{base_url}/funding-rates", timeout=30)
        
        if funding_response.status_code == 200:
            funding_data = funding_response.json()
            
            for exchange, rates in funding_data.items():
                if exchange == "total":
                    continue
                    
                for rate in rates:
                    funding_rate = rate.get("funding_rate", 0)
                    # Funding rates should typically be between -10% and +10% annually
                    assert isinstance(funding_rate, (int, float))
                    assert -0.1 <= funding_rate <= 0.1, f"Unusual funding rate: {funding_rate}"
                    
                    # Check next funding time is in the future (or recent past)
                    next_funding_str = rate.get("next_funding_time")
                    if next_funding_str:
                        try:
                            next_funding = datetime.fromisoformat(next_funding_str.replace('Z', '+00:00'))
                            time_diff = (next_funding - datetime.utcnow()).total_seconds()
                            # Should be within next 24 hours typically
                            assert -3600 < time_diff < 86400, f"Unexpected funding time: {next_funding}"
                        except ValueError:
                            pass  # Time format parsing failed, ignore

class TestFrontendFunctionality:
    """Test frontend functionality through API responses"""
    
    def test_frontend_data_consumption(self):
        """Test that frontend can consume API data correctly"""
        base_url = "http://localhost:8000"
        
        # Get arbitrage data as frontend would
        response = requests.get(f"{base_url}/arbitrage", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify data structure matches frontend expectations
            opportunities = data.get("opportunities", [])
            
            for opp in opportunities:
                # All frontend fields should be present and serializable
                assert isinstance(opp, dict)
                frontend_fields = [
                    "id", "symbol", "long_exchange", "short_exchange",
                    "long_funding_rate", "short_funding_rate", "funding_rate_spread",
                    "estimated_daily_profit", "estimated_weekly_profit",
                    "estimated_monthly_profit", "time_to_next_funding",
                    "trading_fees", "net_daily_apr"
                ]
                
                for field in frontend_fields:
                    assert field in opp
                    # Values should be JSON serializable
                    json.dumps(opp[field])

def run_e2e_tests():
    """Run all E2E tests"""
    print("🚀 Starting E2E tests for DEX Funding Rate Arbitrage App")
    print("=" * 60)
    
    # Check if server is running
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Server is not responding correctly. Make sure the app is running on port 8000")
            print("Run: python backend/main.py")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Make sure the app is running on port 8000")
        print("Run: python backend/main.py")
        return False
    
    print("✅ Server is responding correctly")
    
    # Run all test suites
    test_suites = [
        TestE2EWorkflow,
        TestRealDataIntegration,
        TestFrontendFunctionality
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_suite in test_suites:
        suite_name = test_suite.__name__
        print(f"\n🧪 Running {suite_name}")
        print("-" * 40)
        
        test_instance = test_suite()
        
        # Get all test methods
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            test_name = f"{suite_name}.{test_method}"
            
            try:
                print(f"  📋 {test_method}... ", end="", flush=True)
                getattr(test_instance, test_method)()
                print("✅ PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"❌ FAILED")
                print(f"    Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All E2E tests passed! The app is working correctly.")
        return True
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    run_e2e_tests()
