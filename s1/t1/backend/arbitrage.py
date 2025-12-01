from typing import List, Dict, Tuple
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


def similar(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matching_markets(markets_by_platform: Dict[str, List[Dict]], 
                         similarity_threshold: float = 0.75) -> List[Tuple[Dict, Dict]]:
    """Find markets across platforms that are likely about the same event"""
    matches = []
    platforms = list(markets_by_platform.keys())
    
    for i in range(len(platforms)):
        for j in range(i + 1, len(platforms)):
            platform1 = platforms[i]
            platform2 = platforms[j]
            
            markets1 = markets_by_platform.get(platform1, [])
            markets2 = markets_by_platform.get(platform2, [])
            
            for m1 in markets1:
                for m2 in markets2:
                    similarity = similar(m1["question"], m2["question"])
                    if similarity >= similarity_threshold:
                        matches.append((m1, m2))
    
    return matches


def calculate_arbitrage(market1: Dict, market2: Dict, 
                       outcome: str = "Yes") -> Dict:
    """Calculate arbitrage opportunity between two markets"""
    price1 = market1["prices"].get(outcome, 0)
    price2 = market2["prices"].get(outcome, 0)
    
    opposite_outcome = "No" if outcome == "Yes" else "Yes"
    opposite_price1 = market1["prices"].get(opposite_outcome, 0)
    opposite_price2 = market2["prices"].get(opposite_outcome, 0)
    
    # Strategy 1: Buy Yes on market1, buy No on market2
    cost1 = price1 + opposite_price2
    profit1 = 1 - cost1 if cost1 < 1 else 0
    roi1 = (profit1 / cost1 * 100) if cost1 > 0 else 0
    
    # Strategy 2: Buy No on market1, buy Yes on market2
    cost2 = opposite_price1 + price2
    profit2 = 1 - cost2 if cost2 < 1 else 0
    roi2 = (profit2 / cost2 * 100) if cost2 > 0 else 0
    
    best_roi = max(roi1, roi2)
    best_profit = profit1 if roi1 > roi2 else profit2
    best_strategy = "strategy1" if roi1 > roi2 else "strategy2"
    
    return {
        "market1": {
            "platform": market1["platform"],
            "question": market1["question"],
            "url": market1["url"],
            "prices": market1["prices"]
        },
        "market2": {
            "platform": market2["platform"],
            "question": market2["question"],
            "url": market2["url"],
            "prices": market2["prices"]
        },
        "arbitrage": {
            "exists": best_roi > 0,
            "roi_percentage": round(best_roi, 2),
            "profit_per_dollar": round(best_profit, 4),
            "strategy": best_strategy,
            "description": _get_strategy_description(market1, market2, best_strategy, outcome)
        }
    }


def _get_strategy_description(market1: Dict, market2: Dict, 
                              strategy: str, outcome: str) -> str:
    """Generate human-readable strategy description"""
    if strategy == "strategy1":
        return f"Buy '{outcome}' on {market1['platform']} and '{opposite(outcome)}' on {market2['platform']}"
    else:
        return f"Buy '{opposite(outcome)}' on {market1['platform']} and '{outcome}' on {market2['platform']}"


def opposite(outcome: str) -> str:
    """Get opposite outcome"""
    return "No" if outcome == "Yes" else "Yes"


def find_arbitrage_opportunities(markets_by_platform: Dict[str, List[Dict]], 
                                min_roi: float = 1.0) -> List[Dict]:
    """Find all arbitrage opportunities across platforms"""
    matching_markets = find_matching_markets(markets_by_platform)
    opportunities = []
    
    for market1, market2 in matching_markets:
        arb = calculate_arbitrage(market1, market2)
        
        if arb["arbitrage"]["exists"] and arb["arbitrage"]["roi_percentage"] >= min_roi:
            opportunities.append(arb)
    
    # Sort by ROI descending
    opportunities.sort(key=lambda x: x["arbitrage"]["roi_percentage"], reverse=True)
    
    return opportunities
