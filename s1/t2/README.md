# DEX Funding Rate Arbitrage Web App

A web application that finds arbitrage opportunities between DEX funding rates across decentralized perpetual exchanges.

## Features

- 🔍 Real-time funding rate monitoring across major DEXs
- 📊 Interactive web interface with live arbitrage opportunities
- 💰 ROI calculation and profit estimates
- ⚡ Fast API built with FastAPI
- 🎨 Modern, responsive UI

## Architecture

### Backend
- **FastAPI**: High-performance REST API
- **httpx**: Async HTTP client for fetching funding data
- **DEX Clients**: Custom clients for dYdX, GMX, and Perpetual Protocol
- **Arbitrage Engine**: Smart detection and profit calculation

### Frontend
- **Vanilla HTML/CSS/JavaScript**: Lightweight, no build step required
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Auto-refresh capability

## Supported DEXs

- **dYdX**: Decentralized perpetual exchange
- **GMX V2**: Multi-asset perpetual exchange on Arbitrum
- **Perpetual Protocol**: v2 decentralized perpetual exchange

## Arbitrage Strategy

The app detects funding rate differences between DEXs:
- **Long Strategy**: Short on higher funding rate DEX, long on lower funding rate DEX
- **Short Strategy**: Reverse position when rates invert
- **Profit**: Funding rate differential minus trading fees

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
python backend/main.py
```

3. **Access the web interface**:
Open http://localhost:8000 in your browser

## API Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /funding-rates` - Get current funding rates from all DEXs
- `GET `/arbitrage` - Find arbitrage opportunities
- `GET `/markets` - Get available markets across DEXs

## Testing

Run E2E tests:
```bash
pytest tests/ -v
```

## How It Works

1. **Fetch Funding Rates**: Retrieves current funding rates from all supported DEXs
2. **Match Markets**: Identifies equivalent perpetual markets across platforms
3. **Calculate Arbitrage**: Detects profitable funding rate differences
4. **Display Opportunities**: Shows potential profit, strategy, and market links
