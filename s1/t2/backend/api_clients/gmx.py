from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import httpx
import logging
from .base import DEXClient, Market, FundingRate

logger = logging.getLogger(__name__)

class GMXClient(DEXClient):
    """GMX V2 client for fetching funding rates and market data"""
    
    def __init__(self, base_url: str = "https://api.gmx.io/v2"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_markets(self, limit: int = 100) -> List[Market]:
        """Fetch available perpetual markets from GMX"""
        try:
            response = await self.client.get(f"{self.base_url}/synths")
            response.raise_for_status()
            data = response.json()
            
            markets = []
            for market_data in data.get('synths', [])[:limit]:
                markets.append(Market(
                    id=market_data.get('address', ''),
                    symbol=market_data.get('symbol', '').replace('-', '/'),
                    base_currency=market_data.get('symbol', '').split('/')[0],
                    quote_currency='USD',
                    exchange='GMX',
                    is_active=market_data.get('is_enabled', True),
                    min_order_size=float(market_data.get('min_size', 0)),
                    max_leverage=float(market_data.get('max_leverage', 50))
                ))
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching GMX markets: {e}")
            return []
    
    async def get_funding_rates(self, market_ids: Optional[List[str]] = None) -> List[FundingRate]:
        """Fetch current funding rates from GMX"""
        try:
            response = await self.client.get(f"{self.base_url}/v2/public/funding-rates")
            response.raise_for_status()
            data = response.json()
            
            funding_rates = []
            for rate_data in data.get('funding_rates', []):
                market_address = rate_data.get('market_address')
                if market_ids and market_address not in market_ids:
                    continue
                
                next_funding_time = datetime.fromtimestamp(rate_data.get('next_funding_timestamp', 0))
                
                funding_rates.append(FundingRate(
                    market_id=market_address,
                    symbol=rate_data.get('market_symbol', ''),
                    funding_rate=float(rate_data.get('funding_rate', 0)),
                    next_funding_time=next_funding_time,
                    exchange='GMX',
                    price=float(rate_data.get('index_price', 0)),
                    volume_24h=float(rate_data.get('volume_24h', 0)),
                    open_interest=float(rate_data.get('open_interest', 0))
                ))
            
            return funding_rates
        except Exception as e:
            logger.error(f"Error fetching GMX funding rates: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
