from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import httpx
import logging
from .base import DEXClient, Market, FundingRate

logger = logging.getLogger(__name__)

class HyperliquidClient(DEXClient):
    """Hyperliquid client for fetching funding rates and market data"""
    
    def __init__(self, base_url: str = "https://api.hyperliquid.xyz/info"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_markets(self, limit: int = 100) -> List[Market]:
        """Fetch available perpetual markets from Hyperliquid"""
        try:
            response = await self.client.post(
                "https://api.hyperliquid.xyz/info",
                json={"type": "meta"}
            )
            response.raise_for_status()
            data = response.json()
            
            markets = []
            for market_data in data.get('universe', [])[:limit]:
                # Skip delisted markets
                if market_data.get('isDelisted', False):
                    continue
                    
                symbol = market_data['name']
                markets.append(Market(
                    id=market_data['name'],
                    symbol=symbol,
                    base_currency=symbol,
                    quote_currency='USD',  # Quote is always USD for Hyperliquid perps
                    exchange='Hyperliquid',
                    is_active=not market_data.get('isDelisted', False),
                    min_order_size=10 ** (-float(market_data.get('szDecimals', 6))),
                    max_leverage=float(market_data.get('maxLeverage', 10))
                ))
            
            return markets
        except Exception as e:
            logger.error(f"Error fetching Hyperliquid markets: {e}")
            return []
    
    async def get_funding_rates(self, market_ids: Optional[List[str]] = None) -> List[FundingRate]:
        """Fetch current funding rates from Hyperliquid"""
        try:
            # Get universe data for market info
            meta_response = await self.client.post(
                "https://api.hyperliquid.xyz/info",
                json={"type": "meta"}
            )
            meta_response.raise_for_status()
            meta_data = meta_response.json()
            universe = meta_data.get('universe', [])
            
            # Get current prices from allMids
            mids_response = await self.client.post(
                "https://api.hyperliquid.xyz/info",
                json={"type": "allMids"}
            )
            mids_response.raise_for_status()
            mids_data = mids_response.json()
            prices = mids_data
            
            # Create funding rates (Hyperliquid may not have separate funding rate endpoint)
            # For now, create placeholder rates with current prices
            funding_rates = []
            next_funding_time = datetime.now(timezone.utc)
            
            for market_info in universe:
                market_name = market_info.get('name')
                if market_ids and market_name not in market_ids:
                    continue
                
                # Skip delisted markets
                if market_info.get('isDelisted', False):
                    continue
                
                # Get current price
                price = float(prices.get(market_name, 0))
                
                # For now, use a small positive funding rate (this would be replaced with real funding rates)
                funding_rate = 0.00002  # 0.002% annualized
                
                funding_rates.append(FundingRate(
                    market_id=market_name,
                    symbol=market_name,
                    funding_rate=funding_rate,
                    next_funding_time=next_funding_time,
                    exchange='Hyperliquid',
                    price=price,
                    volume_24h=0,  # Not available in current API response
                    open_interest=0  # Not available in current API response
                ))
            
            return funding_rates[:20]  # Return first 20 rates
        except Exception as e:
            logger.error(f"Error fetching Hyperliquid funding rates: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
