import httpx
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ManifoldClient:
    # Updated to new domain per API docs
    BASE_URL = "https://api.manifold.markets/v0"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_markets(self, limit: int = 100) -> List[Dict]:
        """Fetch active markets from Manifold"""
        try:
            # Manifold API doesn't use 'filter' parameter in query string
            # Instead, we fetch all markets and limit the results
            params = {
                "limit": limit
            }
            
            response = await self.client.get(
                f"{self.BASE_URL}/markets",
                params=params
            )
            response.raise_for_status()
            markets_data = response.json()
            
            markets = []
            for market in markets_data:
                # Only include binary markets that are not resolved
                if (market.get("outcomeType") == "BINARY" and 
                    not market.get("isResolved", False)):
                    probability = market.get("probability", 0.5)
                    markets.append({
                        "id": market.get("id"),
                        "question": market.get("question"),
                        "outcomes": ["Yes", "No"],
                        "prices": {
                            "Yes": probability,
                            "No": 1 - probability
                        },
                        "volume": market.get("volume", 0),
                        "platform": "manifold",
                        "url": market.get("url", "")
                    })
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching Manifold markets: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
