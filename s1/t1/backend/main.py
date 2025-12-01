from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import logging
import os
from dotenv import load_dotenv

from api_clients import PolymarketClient, KalshiClient, ManifoldClient
from arbitrage import find_arbitrage_opportunities

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Prediction Markets Arbitrage API",
    description="Find arbitrage opportunities across prediction markets",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

polymarket_client = PolymarketClient(os.getenv("POLYMARKET_API_KEY"))
kalshi_client = KalshiClient(
    os.getenv("KALSHI_API_KEY"),
    os.getenv("KALSHI_API_SECRET")
)
manifold_client = ManifoldClient()


@app.get("/")
async def root():
    return {
        "message": "Prediction Markets Arbitrage API",
        "endpoints": {
            "/markets": "Get all markets from all platforms",
            "/arbitrage": "Find arbitrage opportunities",
            "/health": "Health check"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/markets")
async def get_all_markets(limit: int = 50) -> Dict[str, List[Dict]]:
    """Fetch markets from all platforms"""
    try:
        polymarket_markets = await polymarket_client.get_markets(limit=limit)
        kalshi_markets = await kalshi_client.get_markets(limit=limit)
        manifold_markets = await manifold_client.get_markets(limit=limit)
        
        return {
            "polymarket": polymarket_markets,
            "kalshi": kalshi_markets,
            "manifold": manifold_markets,
            "total": len(polymarket_markets) + len(kalshi_markets) + len(manifold_markets)
        }
    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/arbitrage")
async def get_arbitrage_opportunities(
    limit: int = 50,
    min_roi: float = 1.0,
    similarity_threshold: float = 0.75
) -> Dict:
    """Find arbitrage opportunities across platforms"""
    try:
        # Fetch markets from all platforms
        polymarket_markets = await polymarket_client.get_markets(limit=limit)
        kalshi_markets = await kalshi_client.get_markets(limit=limit)
        manifold_markets = await manifold_client.get_markets(limit=limit)
        
        markets_by_platform = {
            "polymarket": polymarket_markets,
            "kalshi": kalshi_markets,
            "manifold": manifold_markets
        }
        
        # Find arbitrage opportunities
        opportunities = find_arbitrage_opportunities(
            markets_by_platform,
            min_roi=min_roi
        )
        
        return {
            "opportunities": opportunities,
            "count": len(opportunities),
            "markets_analyzed": {
                "polymarket": len(polymarket_markets),
                "kalshi": len(kalshi_markets),
                "manifold": len(manifold_markets)
            }
        }
    except Exception as e:
        logger.error(f"Error finding arbitrage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    await polymarket_client.close()
    await kalshi_client.close()
    await manifold_client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
