from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

class FundingRate:
    def __init__(self, market_id: str, symbol: str, funding_rate: float, 
                 next_funding_time: datetime, exchange: str, price: float,
                 volume_24h: float, open_interest: float):
        self.market_id = market_id
        self.symbol = symbol
        self.funding_rate = funding_rate
        self.next_funding_time = next_funding_time
        self.exchange = exchange
        self.price = price
        self.volume_24h = volume_24h
        self.open_interest = open_interest
    
    def dict(self):
        return {
            "market_id": self.market_id,
            "symbol": self.symbol,
            "funding_rate": self.funding_rate,
            "next_funding_time": self.next_funding_time.isoformat(),
            "exchange": self.exchange,
            "price": self.price,
            "volume_24h": self.volume_24h,
            "open_interest": self.open_interest
        }

class Market:
    def __init__(self, id: str, symbol: str, base_currency: str, 
                 quote_currency: str, exchange: str, is_active: bool,
                 min_order_size: float, max_leverage: float):
        self.id = id
        self.symbol = symbol
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.exchange = exchange
        self.is_active = is_active
        self.min_order_size = min_order_size
        self.max_leverage = max_leverage
    
    def dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "base_currency": self.base_currency,
            "quote_currency": self.quote_currency,
            "exchange": self.exchange,
            "is_active": self.is_active,
            "min_order_size": self.min_order_size,
            "max_leverage": self.max_leverage
        }

class DEXClient(ABC):
    """Abstract base class for DEX API clients"""
    
    @abstractmethod
    async def get_markets(self, limit: int = 100) -> List[Market]:
        """Fetch available perpetual markets"""
        pass
    
    @abstractmethod
    async def get_funding_rates(self, market_ids: Optional[List[str]] = None) -> List[FundingRate]:
        """Fetch current funding rates for markets"""
        pass
    
    @abstractmethod
    async def close(self):
        """Clean up resources"""
        pass
