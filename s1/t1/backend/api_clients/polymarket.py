import httpx
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PolymarketClient:
    BASE_URL = "https://gamma-api.polymarket.com"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        # Add headers and increase timeout for better reliability
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ArbitrageBot/1.0)"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=headers,
            follow_redirects=True
        )
    
    async def get_markets(self, limit: int = 100, active: bool = True) -> List[Dict]:
        """Fetch active markets from Polymarket"""
        try:
            # Try events endpoint first as it's more stable
            params = {
                "limit": limit,
                "closed": "false"
            }
            
            # First try the events endpoint which includes markets
            try:
                response = await self.client.get(
                    f"{self.BASE_URL}/events",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                # Events endpoint returns different structure
                if data and len(data) > 0:
                    return self._process_events(data)
            except Exception as e:
                logger.warning(f"Events endpoint failed, trying markets endpoint: {e}")
            
            # Fallback to markets endpoint
            response = await self.client.get(
                f"{self.BASE_URL}/markets",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            markets = []
            for market in data:
                markets.append({
                    "id": market.get("condition_id"),
                    "question": market.get("question"),
                    "outcomes": market.get("outcomes", []),
                    "prices": self._extract_prices(market),
                    "volume": market.get("volume", 0),
                    "platform": "polymarket",
                    "url": f"https://polymarket.com/event/{market.get('slug', '')}"
                })
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching Polymarket markets: {e}")
            return []
    
    def _process_events(self, events: List[Dict]) -> List[Dict]:
        """Process events data from Polymarket API"""
        markets = []
        for event in events[:100]:  # Limit to avoid too much data
            # Each event can have multiple markets
            event_markets = event.get("markets", [])
            for market in event_markets:
                try:
                    outcomes = market.get("outcomes", ["Yes", "No"])
                    prices = self._extract_prices(market)
                    if prices:
                        markets.append({
                            "id": market.get("clobTokenIds", [""])[0] or market.get("id", ""),
                            "question": market.get("question", event.get("title", "")),
                            "outcomes": outcomes,
                            "prices": prices,
                            "volume": float(market.get("volume", 0)),
                            "platform": "polymarket",
                            "url": f"https://polymarket.com/event/{event.get('slug', '')}"
                        })
                except Exception as e:
                    logger.debug(f"Skipping market due to error: {e}")
                    continue
        return markets
    
    def _extract_prices(self, market: Dict) -> Dict[str, float]:
        """Extract outcome prices from market data"""
        prices = {}
        outcomes = market.get("outcomes", ["Yes", "No"])
        outcome_prices = market.get("outcomePrices", [])
        
        # Handle both string and numeric prices
        for i, outcome in enumerate(outcomes):
            if i < len(outcome_prices):
                try:
                    price = float(outcome_prices[i])
                    prices[outcome] = price
                except (ValueError, TypeError):
                    prices[outcome] = 0.5
            else:
                prices[outcome] = 0.5
        
        return prices if prices else {"Yes": 0.5, "No": 0.5}
    
    async def close(self):
        await self.client.aclose()
