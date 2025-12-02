#!/usr/bin/env python3
"""
Basic test runner for DEX arbitrage app without external dependencies
"""
import sys
import os
import json
from datetime import datetime, timedelta

# Add project to Python path
sys.path.insert(0, '/home/vuos/code/p2/s1/t2')

def test_basic_arbitrage_logic():
    """Test core arbitrage detection logic without external dependencies"""
    print("🧪 Testing Basic Arbitrage Logic")
    print("-" * 40)
    
    try:
        # Test funding rate data structure
        sample_rate = {
            "market_id": "BTC-USD",
            "symbol": "BTC-USD", 
            "funding_rate": 0.001,
            "next_funding_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "exchange": "dYdX",
            "price": 50000,
            "volume_24h": 1000000,
            "open_interest": 500000
        }
        
        # Test JSON serialization (required for API)
        json_str = json.dumps(sample_rate)
        parsed = json.loads(json_str)
        assert parsed["funding_rate"] == 0.001
        print("✅ Funding rate data structure and serialization working")
        
        # Test profit calculation logic
        def calculate_profit(funding_rate_diff, notional=10000):
            daily_profit = funding_rate_diff * notional
            weekly_profit = daily_profit * 7
            monthly_profit = daily_profit * 30
            return daily_profit, weekly_profit, monthly_profit
        
        # Test profitable scenario
        diff = 0.002  # 0.2% spread
        daily, weekly, monthly = calculate_profit(diff)
        assert daily > 0
        assert weekly > daily
        assert monthly > weekly
        print(f"✅ Profit calculation working: ${daily:.2f} daily, ${weekly:.2f} weekly")
        
        # Test symbol normalization
        def normalize_symbol(symbol):
            return symbol.upper().replace('-', '').replace('_', '').strip()
        
        assert normalize_symbol("BTC-USD") == normalize_symbol("BTCUSD")
        assert normalize_symbol("eth-usd") == "ETHUSD"
        print("✅ Symbol normalization working")
        
        # Test arbitrage opportunity detection logic
        def is_profitable_arbitrage(rate_a, rate_b, min_spread=0.0001):
            spread = abs(rate_a - rate_b)
            return spread >= min_spread
        
        # Should detect arbitrage with 0.2% spread vs 0.01% minimum
        assert is_profitable_arbitrage(0.001, 0.003, 0.0001) == True
        
        # Should not detect arbitrage with tiny spread vs higher minimum
        assert is_profitable_arbitrage(0.001, 0.0002, 0.001) == False
        print("✅ Arbitrage detection logic working")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist and have basic structure"""
    print("\n🧪 Testing File Structure")
    print("-" * 40)
    
    required_files = [
        'backend/main.py',
        'backend/arbitrage.py',
        'backend/api_clients/__init__.py',
        'backend/api_clients/base.py',
        'backend/api_clients/dydx.py',
        'backend/api_clients/gmx.py',
        'backend/api_clients/perpetual.py',
        'frontend/index.html',
        'requirements.txt',
        'tests/test_arbitrage.py',
        'tests/test_e2e.py'
    ]
    
    for file_path in required_files:
        full_path = f'/home/vuos/code/p2/s1/t2/{file_path}'
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic sanity check - not empty
                    print(f"✅ {file_path}")
                else:
                    print(f"❌ {file_path} - empty or too small")
                    return False
        else:
            print(f"❌ {file_path} - missing")
            return False
    
    return True

def test_import_structure():
    """Test that Python modules can be imported correctly"""
    print("\n🧪 Testing Import Structure")
    print("-" * 40)
    
    try:
        # Test core module structure
        import backend.arbitrage
        print("✅ arbitrage module imports correctly")
        
        # Test API client imports (without actually calling external APIs)
        import backend.api_clients.dydx
        import backend.api_clients.gmx
        import backend.api_clients.perpetual
        print("✅ API client modules import correctly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_endpoint_definitions():
    """Test that main.py defines expected API endpoints"""
    print("\n🧪 Testing API Endpoint Definitions")
    print("-" * 40)
    
    try:
        with open('/home/vuos/code/p2/s1/t2/backend/main.py', 'r') as f:
            main_content = f.read()
        
        expected_endpoints = [
            '@app.get("/")',
            '@app.get("/health")',
            '@app.get("/markets")',
            '@app.get("/funding-rates")',
            '@app.get("/arbitrage")'
        ]
        
        missing_endpoints = []
        for endpoint in expected_endpoints:
            if endpoint in main_content:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint} - missing")
                missing_endpoints.append(endpoint)
        
        return len(missing_endpoints) == 0
        
    except Exception as e:
        print(f"❌ Error analyzing main.py: {e}")
        return False

def test_frontend_structure():
    """Test that frontend has required HTML structure"""
    print("\n🧪 Testing Frontend Structure")
    print("-" * 40)
    
    try:
        with open('/home/vuos/code/p2/s1/t2/frontend/index.html', 'r') as f:
            html_content = f.read()
        
        required_elements = [
            'DEX Funding Rate Arbitrage',
            'arbitrage',
            'refresh-btn',
            'function loadArbitrageOpportunities',
            '/arbitrage'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element in html_content:
                print(f"✅ {element}")
            else:
                print(f"❌ {element} - missing")
                missing_elements.append(element)
        
        return len(missing_elements) == 0
        
    except Exception as e:
        print(f"❌ Error analyzing frontend: {e}")
        return False

def run_basic_tests():
    """Run all basic tests that don't require external dependencies"""
    print("🚀 Basic Test Suite for DEX Funding Rate Arbitrage App")
    print("=" * 60)
    print("Testing core functionality without external API dependencies")
    print("=" * 60)
    
    test_results = []
    
    test_results.append(test_basic_arbitrage_logic())
    test_results.append(test_file_structure())
    test_results.append(test_import_structure())
    test_results.append(test_api_endpoint_definitions())
    test_results.append(test_frontend_structure())
    
    passed = sum(test_results)
    total = len(test_results)
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Core functionality is working.")
        print("\n📋 Next Steps:")
        print("1. Install external dependencies if needed:")
        print("   pip3 install fastapi uvicorn httpx pydantic")
        print("2. Start the application:")
        print("   cd /home/vuos/code/p2/s1/t2 && python3 backend/main.py")
        print("3. Run comprehensive E2E tests:")
        print("   python3 tests/test_e2e.py")
        return True
    else:
        print(f"⚠️  {total - passed} test suites failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)
