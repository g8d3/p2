from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Optional
import logging
import os
from dotenv import load_dotenv

from api_clients import DyDXClient, HyperliquidClient
from arbitrage import find_arbitrage_opportunities

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DEX Funding Rate Arbitrage API",
    description="Find arbitrage opportunities across DEX funding rates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DEX clients
dydx_client = DyDXClient()
hyperliquid_client = HyperliquidClient()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "exchanges": ["dYdX", "Hyperliquid"]}

@app.get("/markets")
async def get_all_markets(limit: int = 50) -> Dict[str, List[Dict]]:
    """Fetch markets from all DEX platforms"""
    try:
        dydx_markets = await dydx_client.get_markets(limit=limit)
        hyperliquid_markets = await hyperliquid_client.get_markets(limit=limit)
        
        return {
            "dydx": [market.dict() for market in dydx_markets],
            "hyperliquid": [market.dict() for market in hyperliquid_markets],
            "total": len(dydx_markets) + len(hyperliquid_markets)
        }
    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/funding-rates")
async def get_all_funding_rates(limit: int = 50) -> Dict[str, List[Dict]]:
    """Fetch funding rates from all DEX platforms"""
    try:
        dydx_rates = await dydx_client.get_funding_rates()
        logger.info(f"dYdX rates fetched: {len(dydx_rates)}")
        
        hyperliquid_rates = await hyperliquid_client.get_funding_rates()
        logger.info(f"Hyperliquid rates fetched: {len(hyperliquid_rates)}")
        
        return {
            "dydx": [rate.dict() for rate in dydx_rates[:limit]],
            "hyperliquid": [rate.dict() for rate in hyperliquid_rates[:limit]],
            "total": len(dydx_rates) + len(hyperliquid_rates) if isinstance(dydx_rates, list) and isinstance(hyperliquid_rates, list) else 0
        }
    except Exception as e:
        logger.error(f"Error fetching funding rates: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/arbitrage")
async def get_arbitrage_opportunities(
    limit: int = 20,
    min_rate_spread: float = 0.0001,
    min_notional: float = 1000
) -> Dict:
    """Find arbitrage opportunities across DEXs"""
    try:
        # Fetch funding rates from all exchanges
        dydx_rates = await dydx_client.get_funding_rates()
        hyperliquid_rates = await hyperliquid_client.get_funding_rates()
        
        funding_rates_by_exchange = {
            "dYdX": dydx_rates,
            "Hyperliquid": hyperliquid_rates
        }
        
        # Find arbitrage opportunities
        opportunities = find_arbitrage_opportunities(
            funding_rates_by_exchange,
            min_rate_spread=min_rate_spread,
            min_notional=min_notional
        )
        
        return {
            "opportunities": [opp.dict() for opp in opportunities[:limit]],
            "count": len(opportunities),
            "markets_analyzed": {
                "dYdX": len(dydx_rates),
                "Hyperliquid": len(hyperliquid_rates)
            },
            "filters_used": {
                "min_rate_spread": min_rate_spread,
                "min_notional": min_notional
            }
        }
    except Exception as e:
        logger.error(f"Error finding arbitrage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    await dydx_client.close()
    await hyperliquid_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
