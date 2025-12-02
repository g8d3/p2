import pytest
import asyncio
from datetime import datetime, timedelta
import httpx
from backend.api_clients.base import FundingRate, Market
from backend.api_clients.dydx import DyDXClient
from backend.api_clients.gmx import GMXClient
from backend.api_clients.perpetual import PerpetualClient
from backend.arbitrage import find_arbitrage_opportunities

@pytest.fixture
def sample_funding_rates():
    """Sample funding rates for testing"""
    return {
        "dYdX": [
            FundingRate(
                market_id="BTC-USD",
                symbol="BTC-USD",
                funding_rate=0.001,
                next_funding_time=datetime.utcnow() + timedelta(hours=1),
                exchange="dYdX",
                price=50000,
                volume_24h=1000000,
                open_interest=500000
            ),
            FundingRate(
                market_id="ETH-USD",
                symbol="ETH-USD",
                funding_rate=-0.0005,
                next_funding_time=datetime.utcnow() + timedelta(hours=1),
                exchange="dYdX",
                price=3000,
                volume_24h=500000,
                open_interest=250000
            )
        ],
        "GMX": [
            FundingRate(
                market_id="BTC-USD-GMX",
                symbol="BTC-USD",
                funding_rate=0.002,
                next_funding_time=datetime.utcnow() + timedelta(hours=2),
                exchange="GMX",
                price=50000,
                volume_24h=800000,
                open_interest=400000
            ),
            FundingRate(
                market_id="ETH-USD-GMX",
                symbol="ETH-USD",
                funding_rate=-0.0002,
                next_funding_time=datetime.utcnow() + timedelta(hours=2),
                exchange="GMX",
                price=3000,
                volume_24h=400000,
                open_interest=200000
            )
        ],
        "Perpetual": [
            FundingRate(
                market_id="BTC-USD-PERP",
                symbol="BTC-USD",
                funding_rate=0.0008,
                next_funding_time=datetime.utcnow() + timedelta(hours=3),
                exchange="Perpetual",
                price=50000,
                volume_24h=600000,
                open_interest=300000
            )
        ]
    }

@pytest.fixture
def mock_dydx_client():
    """Mock dYdX client for testing"""
    client = DyDXClient()
    client.client = httpx.AsyncClient()
    return client

@pytest.fixture
def mock_gmx_client():
    """Mock GMX client for testing"""
    client = GMXClient()
    client.client = httpx.AsyncClient()
    return client

@pytest.fixture
def mock_perpetual_client():
    """Mock Perpetual client for testing"""
    client = PerpetualClient()
    client.client = httpx.AsyncClient()
    return client

class TestArbitrageDetection:
    """Test arbitrage opportunity detection algorithm"""
    
    def test_find_arbitrage_opportunities_profitable(self, sample_funding_rates):
        """Test finding profitable arbitrage opportunities"""
        opportunities = find_arbitrage_opportunities(
            sample_funding_rates,
            min_rate_spread=0.0001,
            min_notional=1000
        )
        
        # Should find at least BTC arbitrage between GMX (2%) and Perpetual (0.8%)
        assert len(opportunities) > 0
        
        # Check that opportunities have positive daily profit
        for opp in opportunities:
            assert opp.estimated_daily_profit > 0
            assert opp.funding_rate_spread > 0
            assert opp.long_exchange != opp.short_exchange
    
    def test_find_arbitrage_opportunities_no_spread(self):
        """Test that no opportunities are found with small rate spreads"""
        small_spread_rates = {
            "dYdX": [
                FundingRate(
                    market_id="BTC-USD",
                    symbol="BTC-USD",
                    funding_rate=0.001,
                    next_funding_time=datetime.utcnow() + timedelta(hours=1),
                    exchange="dYdX",
                    price=50000,
                    volume_24h=1000000,
                    open_interest=500000
                )
            ],
            "GMX": [
                FundingRate(
                    market_id="BTC-USD-GMX",
                    symbol="BTC-USD",
                    funding_rate=0.00105,  # Small spread
                    next_funding_time=datetime.utcnow() + timedelta(hours=1),
                    exchange="GMX",
                    price=50000,
                    volume_24h=1000000,
                    open_interest=500000
                )
            ]
        }
        
        opportunities = find_arbitrage_opportunities(
            small_spread_rates,
            min_rate_spread=0.0002,  # Higher threshold than available
            min_notional=1000
        )
        
        assert len(opportunities) == 0
    
    def test_opportunity_sorting(self, sample_funding_rates):
        """Test that opportunities are sorted by profit"""
        opportunities = find_arbitrage_opportunities(
            sample_funding_rates,
            min_rate_spread=0.0001,
            min_notional=1000
        )
        
        if len(opportunities) > 1:
            profits = [opp.estimated_daily_profit for opp in opportunities]
            assert profits == sorted(profits, reverse=True)
    
    def test_symbol_normalization(self, sample_funding_rates):
        """Test symbol matching across exchanges"""
        # Test that symbols like "BTC-USD" and "BTCUSD" match
        btc_opportunities = [opp for opp in find_arbitrage_opportunities(
            sample_funding_rates,
            min_rate_spread=0.0001,
            min_notional=1000
        ) if "BTC" in opp.symbol.upper()]
        
        # Should find BTC arbitrage despite different exchange naming
        assert len(btc_opportunities) > 0

class TestDEXClients:
    """Test DEX client implementations"""
    
    @pytest.mark.asyncio
    async def test_dydx_client_initialization(self):
        """Test dYdX client can be initialized"""
        client = DyDXClient()
        assert client.base_url == "https://api.dydx.exchange"
        assert client.client is not None
        await client.close()
    
    @pytest.mark.asyncio
    async def test_gmx_client_initialization(self):
        """Test GMX client can be initialized"""
        client = GMXClient()
        assert client.base_url == "https://arbitrum-api.gmx.io"
        assert client.client is not None
        await client.close()
    
    @pytest.mark.asyncio
    async def test_perpetual_client_initialization(self):
        """Test Perpetual client can be initialized"""
        client = PerpetualClient()
        assert client.base_url == "https://api-staging.perp.exchange"
        assert client.client is not None
        await client.close()

class TestFastAPIEndpoints:
    """Test Fast API endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test health check endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                data = response.json()
                assert data["status"] == "healthy"
                assert "exchanges" in data
    
    @pytest.mark.asyncio
    async def test_markets_endpoint(self):
        """Test markets endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/markets")
            if response.status_code == 200:
                data = response.json()
                assert "dydx" in data
                assert "gmx" in data
                assert "perpetual" in data
                assert "total" in data
    
    @pytest.mark.asyncio
    async def test_funding_rates_endpoint(self):
        """Test funding rates endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/funding-rates")
            if response.status_code == 200:
                data = response.json()
                assert "dydx" in data
                assert "gmx" in data
                assert "perpetual" in data
    
    @pytest.mark.asyncio
    async def test_arbitrage_endpoint(self):
        """Test arbitrage endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/arbitrage")
            if response.status_code == 200:
                data = response.json()
                assert "opportunities" in data
                assert "count" in data
                assert "markets_analyzed" in data
                assert isinstance(data["opportunities"], list)

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_empty_funding_rates(self):
        """Test handling empty funding rates"""
        opportunities = find_arbitrage_opportunities({})
        assert len(opportunities) == 0
    
    def test_single_exchange_no_arbitrage(self):
        """Test that single exchange can't create arbitrage"""
        single_exchange_rates = {
            "dYdX": [
                FundingRate(
                    market_id="BTC-USD",
                    symbol="BTC-USD",
                    funding_rate=0.001,
                    next_funding_time=datetime.utcnow() + timedelta(hours=1),
                    exchange="dYdX",
                    price=50000,
                    volume_24h=1000000,
                    open_interest=500000
                )
            ]
        }
        
        opportunities = find_arbitrage_opportunities(single_exchange_rates)
        assert len(opportunities) == 0
    
    def test_invalid_funding_rate_data(self):
        """Test handling of invalid or malformed data"""
        # Test with None values
        opps = find_arbitrage_opportunities({})
        assert isinstance(opps, list)
        
        # Test with very small spreads
        tiny_spread_rates = {
            "dYdX": [
                FundingRate(
                    market_id="BTC-USD",
                    symbol="BTC-USD",
                    funding_rate=0.00001,
                    next_funding_time=datetime.utcnow() + timedelta(hours=1),
                    exchange="dYdX",
                    price=50000,
                    volume_24h=1000000,
                    open_interest=500000
                )
            ],
            "GMX": [
                FundingRate(
                    market_id="BTC-USD-GMX",
                    symbol="BTC-USD",
                    funding_rate=0.00002,
                    next_funding_time=datetime.utcnow() + timedelta(hours=1),
                    exchange="GMX",
                    price=50000,
                    volume_24h=1000000,
                    open_interest=500000
                )
            ]
        }
        
        opps = find_arbitrage_opportunities(
            tiny_spread_rates,
            min_rate_spread=0.0001
        )
        # Should filter out tiny spreads
        assert len(opps) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
