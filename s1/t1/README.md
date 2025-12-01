# Prediction Markets Arbitrage Web App

A web application that finds arbitrage opportunities across multiple prediction markets platforms: **Polymarket**, **Kalshi**, and **Manifold Markets**.

## Features

- 🔍 Real-time arbitrage detection across 3 major prediction markets
- 📊 Interactive web interface with live data
- 💰 ROI calculation and profit estimates
- 🎯 Smart question matching using similarity algorithms
- ⚡ Fast API built with FastAPI
- 🎨 Modern, responsive UI

## Architecture

### Backend
- **FastAPI**: High-performance REST API
- **httpx**: Async HTTP client for fetching market data
- **API Clients**: Custom clients for Polymarket, Kalshi, and Manifold
- **Arbitrage Engine**: Smart matching and profit calculation

### Frontend
- **Vanilla HTML/CSS/JavaScript**: Lightweight, no build step required
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Auto-refresh capability

## How It Works

1. **Fetch Markets**: Retrieves active markets from all three platforms
2. **Match Questions**: Uses string similarity to find equivalent markets
3. **Calculate Arbitrage**: Identifies price discrepancies that allow guaranteed profit
4. **Display Opportunities**: Shows ROI, strategy, and direct links to markets

### Arbitrage Strategy

The app finds two scenarios:
- **Strategy 1**: Buy "Yes" on Platform A, buy "No" on Platform B
- **Strategy 2**: Buy "No" on Platform A, buy "Yes" on Platform B

If the combined cost is less than $1, you make guaranteed profit regardless of outcome.

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment variables** (optional, for authenticated API access):
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Run the backend server**:
```bash
cd backend
python main.py
```

The API will start on `http://localhost:8000`

4. **Open the frontend**:
```bash
# Open in your browser
open frontend/index.html
```

Or use a simple HTTP server:
```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`

## API Endpoints

### GET /arbitrage
Find arbitrage opportunities

**Parameters**:
- `limit` (int): Markets to fetch per platform (default: 50)
- `min_roi` (float): Minimum ROI percentage (default: 1.0)

**Response**:
```json
{
  "opportunities": [...],
  "count": 5,
  "markets_analyzed": {
    "polymarket": 50,
    "kalshi": 50,
    "manifold": 50
  }
}
```

### GET /markets
Get all markets from all platforms

**Parameters**:
- `limit` (int): Markets to fetch per platform (default: 50)

### GET /health
Health check endpoint

## Prediction Markets Overview

### Polymarket
- **Type**: Decentralized, blockchain-based
- **Currency**: USDC on Polygon
- **Volume**: Highest trading volume
- **Markets**: Wide variety (politics, sports, crypto, etc.)

### Kalshi
- **Type**: CFTC-regulated exchange
- **Currency**: USD (traditional banking)
- **Markets**: Economic events, elections, weather
- **Compliance**: Full US regulatory compliance

### Manifold Markets
- **Type**: Play money markets
- **Currency**: "Mana" (virtual currency)
- **Markets**: Community-created, diverse topics
- **Access**: Free to use, great for testing

## Example Arbitrage Opportunity

```
Market: "Will Bitcoin reach $100k by end of 2025?"

Polymarket:
- Yes: 60¢
- No: 40¢

Kalshi:
- Yes: 35¢
- No: 65¢

Strategy: Buy Yes on Kalshi (35¢) + Buy No on Polymarket (40¢) = 75¢
Profit: $1.00 - $0.75 = $0.25 per trade
ROI: 33.3%
```

## Configuration

Edit parameters in the UI or via API query parameters:
- **Min ROI**: Filter opportunities by minimum return
- **Market Limit**: How many markets to analyze per platform
- **Similarity Threshold**: How closely questions must match (default: 0.75)

## Notes

- API keys are optional for read-only access to most markets
- Actual trading requires accounts on each platform
- Prices change rapidly - opportunities may disappear quickly
- Consider transaction fees and withdrawal limits when trading
- This is for educational purposes - trade at your own risk

## Project Structure

```
.
├── backend/
│   ├── api_clients/
│   │   ├── polymarket.py
│   │   ├── kalshi.py
│   │   └── manifold.py
│   ├── arbitrage.py
│   └── main.py
├── frontend/
│   └── index.html
├── requirements.txt
├── .env.example
└── README.md
```

## Future Enhancements

- WebSocket support for real-time price updates
- Historical arbitrage tracking
- Email/SMS alerts for opportunities
- Automated trading execution
- More prediction market integrations
- Advanced filtering and sorting options

## License

MIT
