# Loris Arbitrage Executor

A web application that integrates with loris.tools to execute DEX funding arbitrage opportunities.

## Features

- **Real-time Data**: Fetches funding rates from loris.tools every 60 seconds
- **Opportunity Detection**: Identifies arbitrage opportunities across exchanges
- **Live Dashboard**: Interactive web interface with real-time updates
- **Execution Tracking**: Monitor arbitrage execution status and results
- **WebSocket Updates**: Live data streaming without page refresh

## Architecture

- **Backend**: Node.js/Express server with Socket.IO for real-time updates
- **Frontend**: Vanilla JavaScript with responsive design
- **Data Source**: loris.tools API for funding rates data
- **Real-time**: WebSocket connections for live updates

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy environment file:
   ```bash
   cp .env.example .env
   ```
4. Start the server:
   ```bash
   npm start
   ```
   
   For development with auto-reload:
   ```bash
   npm run dev
   ```

5. Open http://localhost:3001 in your browser

## API Endpoints

### GET /api/funding-rates
Returns current funding rates and arbitrage opportunities.

### GET /api/opportunities
Returns only the calculated arbitrage opportunities.

### POST /api/execute-arbitrage
Execute an arbitrage strategy:
```json
{
  "symbol": "BTC",
  "exchange1": "binance",
  "exchange2": "bybit",
  "amount": 1000
}
```

## Arbitrage Strategy

The application identifies funding rate arbitrage opportunities by:

1. **Rate Comparison**: Comparing funding rates for the same symbol across exchanges
2. **Profit Calculation**: Estimating daily profit based on rate differences
3. **Opportunity Ranking**: Sorting opportunities by potential profit
4. **Risk Management**: Filtering opportunities with minimum profit thresholds

## Data Attribution

Funding rate data provided by <a href="https://loris.tools">Loris Tools</a> in accordance with their API terms of service.

## Risk Warning

⚠️ **Important**: This application is for educational and demonstration purposes only. The execution logic simulated and does not perform real trades. Never rely on this or any automated system for production trading without proper testing and risk management.

## Development

Project structure:
```
├── server/
│   └── index.js          # Main server application
├── public/
│   └── index.html        # Frontend interface
├── package.json          # Dependencies and scripts
└── README.md            # This file
```

## License

MIT License
