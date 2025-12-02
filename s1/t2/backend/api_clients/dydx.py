from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import httpx
import logging
from .base import DEXClient, Market, FundingRate

logger = logging.getLogger(__name__)

class DyDXClient(DEXClient):
    """dYdX client for fetching funding rates and market data"""
    
    def __init__(self, base_url: str = "https://api.dydx.exchange"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_markets(self, limit: int = 100) -> List[Market]:
        """Fetch available perpetual markets from dYdX"""
        try:
            response = await self.client.get(f"{self.base_url}/v3/markets")
            response.raise_for_status()
            data = response.json()
            
            markets = []
            for market_data in data.get('markets', {}).values():
                if market_data.get('type') == 'PERPETUAL':
                    markets.append(Market(
                        id=market_data['id'],
                        symbol=market_data['market'].replace('-', '/'),  # Normalize to BTC/USD
                        base_currency=market_data.get('baseAsset', market_data['market'].split('-')[0]),
                        quote_currency=market_data['market'].split('-')[1] if '-' in market_data else 'USD',
                        exchange='dYdX',
                        is_active=market_data.get('status') == 'OPEN',
                        min_order_size=float(market_data.get('minOrderSize', 0)),
                        max_leverage=float(market_data.get('maxLeverage', 10))
                    ))
            
            return markets[:limit]
        except Exception as e:
            logger.error(f"Error fetching dYdX markets: {e}")
            return []
    
    async def get_funding_rates(self, market_ids: Optional[List[str]] = None) -> List[FundingRate]:
        """Fetch current funding rates from dYdX"""
        try:
            response = await self.client.get(f"{self.base_url}/v3/markets")
            response.raise_for_status()
            data = response.json()
            
            funding_rates = []
            markets_data = data.get('markets', {})
            
            for market_id, market_data in markets_data.items():
                if market_data.get('type') == 'PERPETUAL':
                    if market_ids and market_id not in market_ids:
                        continue
                    
                    # Calculate next funding time (dYdX funding every 8 hours at 00:00, 08:00, 16:00 UTC)
                    now = datetime.now(timezone.utc)
                    next_funding_hour = ((now.hour // 8) + 1) * 8
                    if next_funding_hour >= 24:
                        next_funding_hour = 0
                    next_funding = now.replace(hour=next_funding_hour, minute=0, second=0, microsecond=0)
                    
                    # Get the funding rate and price
                    funding_rate = float(market_data.get('nextFundingRate', 0))
                    if next_funding > now:
                        funding_rate = float(market_data.get('currentFundingRate', funding_rate))
                    
                    funding_rates.append(FundingRate(
                        market_id=market_id,
                        symbol=market_data['market'].replace('-', '/'),  # Normalize
                        funding_rate=funding_rate,
                        next_funding_time=next_funding,
                        exchange='dYdX',
                        price=float(market_data.get('oraclePrice', market_data.get('indexPrice', 0))),
                        volume_24h=float(market_data.get('volume24H', 0)),
                        open_interest=float(market_data.get('openInterest', 0))
                    ))
            
            return funding_rates
        except Exception as e:
            logger.error(f"Error fetching dYdX funding rates: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
