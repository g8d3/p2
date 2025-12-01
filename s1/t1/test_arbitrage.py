#!/usr/bin/env python3
"""Simple test script to verify arbitrage detection works"""

import sys
sys.path.insert(0, './backend')

from arbitrage import find_arbitrage_opportunities, calculate_arbitrage


def test_simple_arbitrage():
    """Test a basic arbitrage scenario"""
    market1 = {
        "id": "test1",
        "question": "Will it rain tomorrow?",
        "outcomes": ["Yes", "No"],
        "prices": {"Yes": 0.60, "No": 0.40},
        "platform": "polymarket",
        "url": "https://polymarket.com/test",
        "volume": 1000
    }
    
    market2 = {
        "id": "test2",
        "question": "Will it rain tomorrow?",
        "outcomes": ["Yes", "No"],
        "prices": {"Yes": 0.35, "No": 0.65},
        "platform": "kalshi",
        "url": "https://kalshi.com/test",
        "volume": 500
    }
    
    result = calculate_arbitrage(market1, market2)
    
    print("=" * 60)
    print("ARBITRAGE TEST RESULTS")
    print("=" * 60)
    print(f"\nMarket 1 ({market1['platform']}): {market1['question']}")
    print(f"  Yes: {market1['prices']['Yes']*100:.1f}¢  No: {market1['prices']['No']*100:.1f}¢")
    print(f"\nMarket 2 ({market2['platform']}): {market2['question']}")
    print(f"  Yes: {market2['prices']['Yes']*100:.1f}¢  No: {market2['prices']['No']*100:.1f}¢")
    print(f"\nArbitrage exists: {result['arbitrage']['exists']}")
    print(f"ROI: {result['arbitrage']['roi_percentage']:.2f}%")
    print(f"Profit per $1: ${result['arbitrage']['profit_per_dollar']:.4f}")
    print(f"Strategy: {result['arbitrage']['description']}")
    
    assert result['arbitrage']['exists'], "Should find arbitrage opportunity"
    assert result['arbitrage']['roi_percentage'] > 0, "ROI should be positive"
    
    print("\n✅ Test passed!")
    print("=" * 60)


def test_find_opportunities():
    """Test finding opportunities across multiple markets"""
    markets_by_platform = {
        "polymarket": [
            {
                "id": "p1",
                "question": "Will Bitcoin reach $100k in 2025?",
                "outcomes": ["Yes", "No"],
                "prices": {"Yes": 0.70, "No": 0.30},
                "platform": "polymarket",
                "url": "https://polymarket.com/btc",
                "volume": 10000
            }
        ],
        "kalshi": [
            {
                "id": "k1",
                "question": "Will Bitcoin hit $100k by 2025?",
                "outcomes": ["Yes", "No"],
                "prices": {"Yes": 0.25, "No": 0.75},
                "platform": "kalshi",
                "url": "https://kalshi.com/btc",
                "volume": 5000
            }
        ],
        "manifold": []
    }
    
    opportunities = find_arbitrage_opportunities(markets_by_platform, min_roi=1.0)
    
    print("\n" + "=" * 60)
    print("FINDING OPPORTUNITIES TEST")
    print("=" * 60)
    print(f"\nMarkets analyzed:")
    print(f"  Polymarket: {len(markets_by_platform['polymarket'])}")
    print(f"  Kalshi: {len(markets_by_platform['kalshi'])}")
    print(f"  Manifold: {len(markets_by_platform['manifold'])}")
    print(f"\nOpportunities found: {len(opportunities)}")
    
    if opportunities:
        opp = opportunities[0]
        print(f"\nBest opportunity:")
        print(f"  ROI: {opp['arbitrage']['roi_percentage']:.2f}%")
        print(f"  Strategy: {opp['arbitrage']['description']}")
    
    assert len(opportunities) > 0, "Should find at least one opportunity"
    
    print("\n✅ Test passed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_simple_arbitrage()
        test_find_opportunities()
        print("\n🎉 All tests passed!\n")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
