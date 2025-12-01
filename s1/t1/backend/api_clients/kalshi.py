import httpx
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class KalshiClient:
    BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_markets(self, limit: int = 100) -> List[Dict]:
        """Fetch active markets from Kalshi"""
        try:
            params = {
                "limit": limit,
                "status": "open"
            }
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = await self.client.get(
                f"{self.BASE_URL}/markets",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            markets = []
            market_list = data.get("markets", [])
            
            for market in market_list:
                markets.append({
                    "id": market.get("ticker"),
                    "question": market.get("title"),
                    "outcomes": ["Yes", "No"],
                    "prices": {
                        "Yes": market.get("yes_bid", 0.5),
                        "No": market.get("no_bid", 0.5)
                    },
                    "volume": market.get("volume", 0),
                    "platform": "kalshi",
                    "url": f"https://kalshi.com/markets/{market.get('ticker', '')}"
                })
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching Kalshi markets: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
