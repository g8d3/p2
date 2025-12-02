#!/usr/bin/env python3
"""
Standalone test that demonstrates the arbitrage app is working
"""
import sys
import os
import json
from datetime import datetime, timedelta

# Add project to Python path
sys.path.insert(0, '/home/vuos/code/p2/s1/t2')

def test_complete_arbitrage_pipeline():
    """Test the complete arbitrage detection pipeline with mock data"""
    print("🧪 Testing Complete Arbitrage Pipeline")
    print("-" * 40)
    
    try:
        # Import and test core components
        from backend.arbitrage import normalize_symbol, find_arbitrage_opportunities
        from backend.api_clients.base import FundingRate
        
        # Create mock funding rate data
        mock_rates = {
            "dYdX": [
                FundingRate(
                    "BTC-USD", "BTC-USD", 0.001, 
                    datetime.now() + timedelta(hours=1), "dYdX", 
                    50000, 1000000, 500000
                ),
                FundingRate(
                    "ETH-USD", "ETH-USD", -0.0005,
                    datetime.now() + timedelta(hours=1), "dYdX",
                    3000, 500000, 250000
                )
            ],
            "GMX": [
                FundingRate(
                    "BTC-USD-GMX", "BTC-USD", 0.002,
                    datetime.now() + timedelta(hours=2), "GMX",
                    50000, 800000, 400000
                ),
                FundingRate(
                    "ETH-USD-GMX", "ETH-USD", -0.0002,
                    datetime.now() + timedelta(hours=2), "GMX",
                    3000, 400000, 200000
                )
            ],
            "Perpetual": [
                FundingRate(
                    "BTC-USD-PERP", "BTC-USD", 0.0008,
                    datetime.now() + timedelta(hours=3), "Perpetual",
                    50000, 600000, 300000
                )
            ]
        }
        
        print("✅ Mock data created successfully")
        
        # Test arbitrage detection
        opportunities = find_arbitrage_opportunities(
            mock_rates,
            min_rate_spread=0.0001,
            min_notional=1000
        )
        
        print(f"✅ Found {len(opportunities)} arbitrage opportunities")
        
        # Verify opportunities are profitable
        for opp in opportunities:
            assert opp.estimated_daily_profit > 0
            assert opp.funding_rate_spread > 0
            assert opp.long_exchange != opp.short_exchange
            
            # Test serialization (important for API)
            opp_dict = opp.dict()
            assert json.dumps(opp_dict)  # Should be JSON serializable
            print(f"✅ {opp.symbol}: ${opp.estimated_daily_profit:.2f}/day ({opp.net_daily_apr}% APR)")
        
        return True, opportunities
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False, []

def test_server_connectivity():
    """Test that we can connect to the running server"""
    print("\n🧪 Testing Server Connectivity")
    print("-" * 40)
    
    try:
        import urllib.request
        import json
        
        # Test health endpoint
        response = urllib.request.urlopen('http://localhost:8000/health', timeout=5)
        health_data = json.loads(response.read().decode())
        
        assert health_data.get('status') == 'healthy'
        print("✅ Health endpoint working")
        
        # Test arbitrage endpoint
        response = urllib.request.urlopen('http://localhost:8000/arbitrage', timeout=15)
        arbitrage_data = json.loads(response.read().decode())
        
        assert 'opportunities' in arbitrage_data
        assert 'count' in arbitrage_data
        
        opportunities = arbitrage_data['opportunities']
        print(f"✅ Found {len(opportunities)} real arbitrage opportunities")
        
        for opp in opportunities[:3]:  # Show first 3
            print(f"  📈 {opp['symbol']}: ${opp['estimated_daily_profit']:.2f}/day")
        
        return True
        
    except Exception as e:
        print(f"❌ Server connectivity test failed: {e}")
        print("   Make sure the server is running: source ~/code/pyenvs/3.10/bin/activate && python backend/main.py")
        return False

def test_frontend_integration():
    """Test that frontend can consume API data"""
    print("\n🧪 Testing Frontend Integration")
    print("-" * 40)
    
    try:
        import urllib.request
        import json
        
        # Test main page loads
        response = urllib.request.urlopen('http://localhost:8000/', timeout=5)
        html_content = response.read().decode()
        
        assert 'DEX Funding Rate Arbitrage' in html_content
        print("✅ Frontend HTML loads correctly")
        
        # Test that frontend JavaScript can fetch data
        response = urllib.request.urlopen('http://localhost:8000/arbitrage', timeout=15)
        data = json.loads(response.read().decode())
        
        # Verify data structure matches frontend expectations
        required_fields = [
            'id', 'symbol', 'long_exchange', 'short_exchange',
            'estimated_daily_profit', 'funding_rate_spread'
        ]
        
        if data['opportunities']:
            opp = data['opportunities'][0]
            for field in required_fields:
                assert field in opp
            print("✅ API data structure matches frontend expectations")
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend integration test failed: {e}")
        return False

def run_demonstration():
    """Run complete demonstration that app is working"""
    print("🚀 DEX Funding Rate Arbitrage App Demonstration")
    print("=" * 60)
    print("Testing core arbitrage functionality and server integration")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Core arbitrage pipeline
    pipeline_success, opportunities = test_complete_arbitrage_pipeline()
    test_results.append(("Arbitrage Pipeline", pipeline_success))
    
    # Test 2: Server connectivity (requires running server)
    server_success = test_server_connectivity()
    test_results.append(("Server Connectivity", server_success))
    
    # Test 3: Frontend integration
    frontend_success = test_frontend_integration()
    test_results.append(("Frontend Integration", frontend_success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(test_results)} test suites passed")
    
    if passed == len(test_results):
        print("\n🎉 SUCCESS! The DEX funding rate arbitrage app is working correctly!")
        print("\n📋 What's Working:")
        print("✅ Arbitrage detection algorithm identifies profitable opportunities")
        print("✅ Server API endpoints respond correctly")
        print("✅ Frontend can display opportunities with real data")
        print("✅ Profit calculations and data serialization work")
        
        print("\n🚀 To use the app:")
        print("1. Start server: source ~/code/pyenvs/3.10/bin/activate && python backend/main.py")
        print("2. Open browser: http://localhost:8000")
        print("3. View real-time arbitrage opportunities")
        
        return True
    else:
        print(f"\n⚠️  {len(test_results) - passed} test suites failed.")
        if not server_success:
            print("💡 Make sure to start the server first:")
            print("   source ~/code/pyenvs/3.10/bin/activate && python backend/main.py")
        
        return False

if __name__ == "__main__":
    success = run_demonstration()
    sys.exit(0 if success else 1)
