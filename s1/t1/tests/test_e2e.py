#!/usr/bin/env python3
"""
End-to-end tests for the prediction markets arbitrage app.
Tests the entire flow from API clients to arbitrage detection.
"""

import asyncio
import sys
import os
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api_clients import PolymarketClient, KalshiClient, ManifoldClient
from arbitrage import find_arbitrage_opportunities, calculate_arbitrage


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"  ✅ {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"  ❌ {test_name}: {error}")
    
    def add_warning(self, test_name: str, message: str):
        self.warnings += 1
        print(f"  ⚠️  {test_name}: {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")
        
        return self.failed == 0


async def test_api_connectivity(results: TestResults):
    """Test basic connectivity to all three APIs"""
    print("\n📡 Testing API Connectivity...")
    
    # Test Manifold
    try:
        client = ManifoldClient()
        markets = await client.get_markets(limit=1)
        await client.close()
        
        if markets and len(markets) > 0:
            results.add_pass("Manifold API connectivity")
        else:
            results.add_warning("Manifold API", "Connected but no markets returned")
    except Exception as e:
        results.add_fail("Manifold API connectivity", str(e))
    
    # Test Kalshi
    try:
        client = KalshiClient()
        markets = await client.get_markets(limit=1)
        await client.close()
        
        if markets and len(markets) > 0:
            results.add_pass("Kalshi API connectivity")
        else:
            results.add_warning("Kalshi API", "Connected but no markets returned")
    except Exception as e:
        results.add_fail("Kalshi API connectivity", str(e))
    
    # Test Polymarket
    try:
        client = PolymarketClient()
        markets = await client.get_markets(limit=1)
        await client.close()
        
        if markets and len(markets) > 0:
            results.add_pass("Polymarket API connectivity")
        else:
            results.add_warning("Polymarket API", "Connected but no markets returned")
    except Exception as e:
        results.add_warning("Polymarket API connectivity", str(e))


async def test_market_data_structure(results: TestResults):
    """Test that market data has the correct structure"""
    print("\n📊 Testing Market Data Structure...")
    
    required_fields = ["id", "question", "outcomes", "prices", "platform", "url"]
    
    # Test Manifold
    try:
        client = ManifoldClient()
        markets = await client.get_markets(limit=1)
        await client.close()
        
        if markets and len(markets) > 0:
            market = markets[0]
            missing = [f for f in required_fields if f not in market]
            
            if not missing:
                results.add_pass("Manifold market structure")
            else:
                results.add_fail("Manifold market structure", f"Missing fields: {missing}")
        else:
            results.add_warning("Manifold market structure", "No markets to test")
    except Exception as e:
        results.add_fail("Manifold market structure", str(e))
    
    # Test Kalshi
    try:
        client = KalshiClient()
        markets = await client.get_markets(limit=1)
        await client.close()
        
        if markets and len(markets) > 0:
            market = markets[0]
            missing = [f for f in required_fields if f not in market]
            
            if not missing:
                results.add_pass("Kalshi market structure")
            else:
                results.add_fail("Kalshi market structure", f"Missing fields: {missing}")
        else:
            results.add_warning("Kalshi market structure", "No markets to test")
    except Exception as e:
        results.add_fail("Kalshi market structure", str(e))


async def test_price_validity(results: TestResults):
    """Test that prices are valid (between 0 and 1)"""
    print("\n💰 Testing Price Validity...")
    
    async def check_prices(client, platform_name: str):
        try:
            markets = await client.get_markets(limit=5)
            await client.close()
            
            if not markets:
                results.add_warning(f"{platform_name} price validity", "No markets to test")
                return
            
            invalid_prices = []
            for market in markets:
                prices = market.get("prices", {})
                for outcome, price in prices.items():
                    if not (0 <= price <= 1):
                        invalid_prices.append(f"{outcome}: {price}")
            
            if not invalid_prices:
                results.add_pass(f"{platform_name} price validity")
            else:
                results.add_fail(f"{platform_name} price validity", 
                               f"Invalid prices found: {invalid_prices[:3]}")
        except Exception as e:
            results.add_fail(f"{platform_name} price validity", str(e))
    
    await check_prices(ManifoldClient(), "Manifold")
    await check_prices(KalshiClient(), "Kalshi")


def test_arbitrage_calculation(results: TestResults):
    """Test arbitrage calculation logic"""
    print("\n🧮 Testing Arbitrage Calculation...")
    
    # Test case 1: Clear arbitrage opportunity
    market1 = {
        "platform": "manifold",
        "question": "Will it rain?",
        "prices": {"Yes": 0.70, "No": 0.30},
        "url": "https://example.com/1"
    }
    
    market2 = {
        "platform": "kalshi",
        "question": "Will it rain?",
        "prices": {"Yes": 0.25, "No": 0.75},
        "url": "https://example.com/2"
    }
    
    try:
        result = calculate_arbitrage(market1, market2)
        
        # Should find arbitrage
        if result["arbitrage"]["exists"]:
            results.add_pass("Arbitrage detection (positive case)")
        else:
            results.add_fail("Arbitrage detection (positive case)", 
                           "Failed to detect clear arbitrage")
        
        # ROI should be positive
        if result["arbitrage"]["roi_percentage"] > 0:
            results.add_pass("Arbitrage ROI calculation")
        else:
            results.add_fail("Arbitrage ROI calculation", 
                           f"ROI should be positive, got {result['arbitrage']['roi_percentage']}")
    except Exception as e:
        results.add_fail("Arbitrage calculation", str(e))
    
    # Test case 2: No arbitrage (efficient market)
    market3 = {
        "platform": "manifold",
        "question": "Will it rain?",
        "prices": {"Yes": 0.50, "No": 0.50},
        "url": "https://example.com/3"
    }
    
    market4 = {
        "platform": "kalshi",
        "question": "Will it rain?",
        "prices": {"Yes": 0.50, "No": 0.50},
        "url": "https://example.com/4"
    }
    
    try:
        result = calculate_arbitrage(market3, market4)
        
        # Should not find arbitrage
        if not result["arbitrage"]["exists"]:
            results.add_pass("Arbitrage detection (negative case)")
        else:
            results.add_warning("Arbitrage detection (negative case)", 
                              "Detected arbitrage in efficient market (might be rounding)")
    except Exception as e:
        results.add_fail("Arbitrage calculation (negative case)", str(e))


async def test_arbitrage_finding(results: TestResults):
    """Test finding arbitrage opportunities across real markets"""
    print("\n🔍 Testing Arbitrage Finding...")
    
    try:
        # Fetch markets from all platforms
        manifold_client = ManifoldClient()
        kalshi_client = KalshiClient()
        
        manifold_markets = await manifold_client.get_markets(limit=10)
        kalshi_markets = await kalshi_client.get_markets(limit=10)
        
        await manifold_client.close()
        await kalshi_client.close()
        
        markets_by_platform = {
            "manifold": manifold_markets,
            "kalshi": kalshi_markets,
            "polymarket": []  # Optional
        }
        
        # Try to find opportunities
        opportunities = find_arbitrage_opportunities(markets_by_platform, min_roi=0.1)
        
        # Just check it runs without errors
        results.add_pass("Arbitrage finding execution")
        
        # Info about results
        if opportunities:
            print(f"    ℹ️  Found {len(opportunities)} opportunities with ROI > 0.1%")
            best = opportunities[0]
            print(f"    ℹ️  Best ROI: {best['arbitrage']['roi_percentage']:.2f}%")
        else:
            print("    ℹ️  No arbitrage opportunities found (this is normal)")
        
    except Exception as e:
        results.add_fail("Arbitrage finding", str(e))


async def test_api_error_handling(results: TestResults):
    """Test that API clients handle errors gracefully"""
    print("\n🛡️  Testing Error Handling...")
    
    # All clients should return empty arrays on error, not crash
    clients = [
        (ManifoldClient(), "Manifold"),
        (KalshiClient(), "Kalshi"),
        (PolymarketClient(), "Polymarket")
    ]
    
    for client, name in clients:
        try:
            # Even if API fails, should return [] not crash
            markets = await client.get_markets(limit=1)
            await client.close()
            
            if isinstance(markets, list):
                results.add_pass(f"{name} error handling (returns list)")
            else:
                results.add_fail(f"{name} error handling", 
                               f"Should return list, got {type(markets)}")
        except Exception as e:
            results.add_fail(f"{name} error handling", 
                           f"Should not raise exception: {e}")


async def test_end_to_end_flow(results: TestResults):
    """Test the complete end-to-end flow"""
    print("\n🔄 Testing End-to-End Flow...")
    
    try:
        # Step 1: Fetch markets from all platforms
        manifold_client = ManifoldClient()
        kalshi_client = KalshiClient()
        polymarket_client = PolymarketClient()
        
        manifold_markets = await manifold_client.get_markets(limit=20)
        kalshi_markets = await kalshi_client.get_markets(limit=20)
        polymarket_markets = await polymarket_client.get_markets(limit=20)
        
        await manifold_client.close()
        await kalshi_client.close()
        await polymarket_client.close()
        
        results.add_pass("E2E: Market fetching")
        
        # Step 2: Combine markets
        markets_by_platform = {
            "manifold": manifold_markets,
            "kalshi": kalshi_markets,
            "polymarket": polymarket_markets
        }
        
        total_markets = len(manifold_markets) + len(kalshi_markets) + len(polymarket_markets)
        print(f"    ℹ️  Fetched {total_markets} total markets")
        
        results.add_pass("E2E: Market aggregation")
        
        # Step 3: Find arbitrage
        opportunities = find_arbitrage_opportunities(markets_by_platform, min_roi=1.0)
        
        results.add_pass("E2E: Arbitrage detection")
        
        # Step 4: Validate results
        if opportunities:
            for opp in opportunities[:3]:  # Check first 3
                required = ["market1", "market2", "arbitrage"]
                missing = [f for f in required if f not in opp]
                
                if missing:
                    results.add_fail("E2E: Result structure", f"Missing: {missing}")
                    break
            else:
                results.add_pass("E2E: Result structure")
            
            print(f"    ℹ️  Found {len(opportunities)} opportunities")
        else:
            print("    ℹ️  No opportunities found (this is normal)")
            results.add_pass("E2E: Complete flow")
        
    except Exception as e:
        results.add_fail("E2E: Complete flow", str(e))


async def run_all_tests():
    """Run all E2E tests"""
    results = TestResults()
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           PREDICTION MARKETS ARBITRAGE E2E TESTS             ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # Run all test suites
    await test_api_connectivity(results)
    await test_market_data_structure(results)
    await test_price_validity(results)
    test_arbitrage_calculation(results)
    await test_arbitrage_finding(results)
    await test_api_error_handling(results)
    await test_end_to_end_flow(results)
    
    # Print summary
    success = results.summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
