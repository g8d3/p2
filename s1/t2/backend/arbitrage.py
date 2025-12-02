from typing import List, Dict, Any, Optional
from datetime import datetime
from api_clients import FundingRate
import logging

logger = logging.getLogger(__name__)

class ArbitrageOpportunity:
    def __init__(self, id: str, symbol: str, long_exchange: str, short_exchange: str,
                 long_funding_rate: float, short_funding_rate: float, funding_rate_spread: float,
                 estimated_daily_profit: float, estimated_weekly_profit: float,
                 estimated_monthly_profit: float, time_to_next_funding: str,
                 min_notional_value: float, trading_fees: float, net_daily_apr: float):
        self.id = id
        self.symbol = symbol
        self.long_exchange = long_exchange
        self.short_exchange = short_exchange
        self.long_funding_rate = long_funding_rate
        self.short_funding_rate = short_funding_rate
        self.funding_rate_spread = funding_rate_spread
        self.estimated_daily_profit = estimated_daily_profit
        self.estimated_weekly_profit = estimated_weekly_profit
        self.estimated_monthly_profit = estimated_monthly_profit
        self.time_to_next_funding = time_to_next_funding
        self.min_notional_value = min_notional_value
        self.trading_fees = trading_fees
        self.net_daily_apr = net_daily_apr
    
    def dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "long_exchange": self.long_exchange,
            "short_exchange": self.short_exchange,
            "long_funding_rate": self.long_funding_rate,
            "short_funding_rate": self.short_funding_rate,
            "funding_rate_spread": self.funding_rate_spread,
            "estimated_daily_profit": self.estimated_daily_profit,
            "estimated_weekly_profit": self.estimated_weekly_profit,
            "estimated_monthly_profit": self.estimated_monthly_profit,
            "time_to_next_funding": self.time_to_next_funding,
            "min_notional_value": self.min_notional_value,
            "trading_fees": self.trading_fees,
            "net_daily_apr": self.net_daily_apr
        }
    
def normalize_symbol(symbol: str) -> str:
    """Normalize symbol name for matching across exchanges"""
    return symbol.upper().replace('-', '').replace('_', '').strip()

def calculate_trading_fees(exchange: str, notional: float) -> float:
    """Calculate trading fees for different DEXs"""
    fee_rates = {
        'dYdX': 0.0002,  # 0.02%
        'GMX': 0.001,    # 0.1%
        'Perpetual': 0.0003  # 0.03%
    }
    base_fee = notional * fee_rates.get(exchange, 0.001)
    # Add spread and slippage estimates
    return base_fee * 1.5  # Conservative estimate including slippage

def find_arbitrage_opportunities(
    funding_rates_by_exchange: Dict[str, List[FundingRate]],
    min_rate_spread: float = 0.0001,
    min_notional: float = 1000
) -> List[ArbitrageOpportunity]:
    """
    Find arbitrage opportunities between funding rates across exchanges
    
    Args:
        funding_rates_by_exchange: Dict mapping exchange names to funding rate lists
        min_rate_spread: Minimum rate spread to consider for arbitrage
        min_notional: Minimum notional value for trade
    
    Returns:
        List of arbitrage opportunities
    """
    opportunities = []
    exchanges = list(funding_rates_by_exchange.keys())
    
    if len(exchanges) < 2:
        return opportunities
    
    # Group funding rates by normalized symbol
    symbols_to_rates = {}
    for exchange, rates in funding_rates_by_exchange.items():
        for rate in rates:
            symbol = normalize_symbol(rate.symbol)
            if symbol not in symbols_to_rates:
                symbols_to_rates[symbol] = {}
            symbols_to_rates[symbol][exchange] = rate
    
    # Find arbitrage opportunities for each symbol
    for symbol, exchange_rates in symbols_to_rates.items():
        if len(exchange_rates) < 2:
            continue
        
        # Find extreme rates
        exchanges_list = list(exchange_rates.keys())
        rate_pairs = []
        
        for i, exchange_a in enumerate(exchanges_list):
            for exchange_b in exchanges_list[i+1:]:
                rate_a = exchange_rates[exchange_a]  # Higher rate (pay funding)
                rate_b = exchange_rates[exchange_b]  # Lower rate (receive funding)
                
                # Calculate spread (difference in funding rates)
                rate_spread = abs(rate_a.funding_rate - rate_b.funding_rate)
                
                if rate_spread >= min_rate_spread:
                    # Determine which exchange to go long vs short
                    if rate_a.funding_rate > rate_b.funding_rate:
                        short_exchange = exchange_a
                        long_exchange = exchange_b
                        short_rate = rate_a.funding_rate
                        long_rate = rate_b.funding_rate
                    else:
                        short_exchange = exchange_b
                        long_exchange = exchange_a
                        short_rate = rate_b.funding_rate
                        long_rate = rate_a.funding_rate
                    
                    # Calculate profits for $10,000 notional (can be adjusted)
                    notional = max(min_notional, 10000)
                    
                    # Trading fees for opening positions
                    short_fees = calculate_trading_fees(short_exchange, notional)
                    long_fees = calculate_trading_fees(long_exchange, notional)
                    total_fees = short_fees + long_fees
                    
                    # Funding rate difference creates profit/loss
                    daily_funding_diff = (short_rate - long_rate) * notional
                    
                    # Net profit after fees
                    net_daily_profit = daily_funding_diff
                    weekly_profit = net_daily_profit * 7
                    monthly_profit = net_daily_profit * 30
                    
                    # Calculate time to next funding
                    now = datetime.utcnow()
                    time_to_funding = min(
                        exchange_rates[short_exchange].next_funding_time,
                        exchange_rates[long_exchange].next_funding_time
                    )
                    time_diff = time_to_funding - now if time_to_funding > now else datetime.utcnow() - now
                    hours_to_funding = max(0, time_diff.total_seconds() / 3600)
                    
                    # Calculate net APR after trading fees amortized over time
                    if hours_to_funding > 0:
                        fee_factor = total_fees / notional
                        spread_apr = short_rate - long_rate
                        net_apr = spread_apr * 365 - fee_factor * 365 / (hours_to_funding / 24)
                    else:
                        net_apr = 0
                    
                    if net_daily_profit > 0:  # Only show profitable opportunities
                        opportunity = ArbitrageOpportunity(
                            id=f"{symbol}_{short_exchange}_{long_exchange}",
                            symbol=symbol,
                            long_exchange=long_exchange,
                            short_exchange=short_exchange,
                            long_funding_rate=long_rate,
                            short_funding_rate=short_rate,
                            funding_rate_spread=rate_spread,
                            estimated_daily_profit=round(net_daily_profit, 2),
                            estimated_weekly_profit=round(weekly_profit, 2),
                            estimated_monthly_profit=round(monthly_profit, 2),
                            time_to_next_funding=f"{hours_to_funding:.1f} hours",
                            min_notional_value=notional,
                            trading_fees=round(total_fees, 2),
                            net_daily_apr=round(net_apr * 100, 2)
                        )
                        opportunities.append(opportunity)
    
    # Sort by highest daily profit
    opportunities.sort(key=lambda x: x.estimated_daily_profit, reverse=True)
    return opportunities
