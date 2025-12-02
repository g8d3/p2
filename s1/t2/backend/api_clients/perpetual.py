from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
import logging
from .base import DEXClient, Market, FundingRate

logger = logging.getLogger(__name__)

class PerpetualClient(DEXClient):
    """Perpetual Protocol V2 client for fetching funding rates and market data"""
    
    def __init__(self, base_url: str = "https://api-staging.perp.exchange"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_markets(self, limit: int = 100) -> List[Market]:
        """Fetch available perpetual markets from Perpetual Protocol"""
        try:
            response = await self.client.get(f"{self.base_url}/markets")
            response.raise_for_status()
            data = response.json()
            
            markets = []
            for market_data in data[:limit]:
                markets.append(Market(
                    id=market_data['marketId'],
                    symbol=market_data['ticker'],
                    base_currency=market_data['baseCurrency'],
                    quote_currency=market_data['quoteCurrency'],
                    exchange='Perpetual',
                    is_active=market_data.get('isClosed') == False,
                    min_order_size=float(market_data.get('minOrderSize', 0)),
                    max_leverage=float(market_data.get('maxLeverage', 10))
                ))
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching Perpetual markets: {e}")
            return []
    
    async def get_funding_rates(self, market_ids: Optional[List[str]] = None) -> List[FundingRate]:
        """Fetch current funding rates from Perpetual Protocol"""
        try:
            response = await self.client.get(f"{self.base_url}/markets")
            response.raise_for_status()
            data = response.json()
            
            funding_rates = []
            for market_data in data:
                market_id = market_data['marketId']
                if market_ids and market_id not in market_ids:
                    continue
                
                next_funding_time = datetime.fromtimestamp(market_data.get('nextFundingTime', 0))
                
                funding_rates.append(FundingRate(
                    market_id=market_id,
                    symbol=market_data['ticker'],
                    funding_rate=float(market_data.get('currentFundingRate', 0)),
                    next_funding_time=next_funding_time,
                    exchange='Perpetual',
                    price=float(market_data.get('indexPrice', 0)),
                    volume_24h=float(market_data.get('volume24h', 0)),
                    open_interest=float(market_data.get('openInterest', 0))
                ))
            
            return funding_rates
        except Exception as e:
            logger.error(f"Error fetching Perpetual funding rates: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
