# CLOB Perpetual DEX Arbitrage Tools

A modern web application for identifying funding rate arbitrage opportunities across Central Limit Order Book (CLOB) perpetual decentralized exchanges.

## Features

- **Real-time Data**: Funding rates updated every minute from 15+ CLOB perpetual DEXes
- **Arbitrage Detection**: Automatically calculates the best arbitrage opportunities across exchanges
- **Interactive Filtering**: Filter by specific exchanges, tokens, or opportunity size
- **Advanced Analytics**: Calculate APY, volume metrics, and opportunity rankings
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS

## Supported Exchanges

### CLOB Perpetual DEXes
- **Hyperliquid** (Arbitrum) - 1h funding
- **Drift** (Solana) - 1h funding  
- **Aster** (Arbitrum) - 8h funding
- **Lighter** (Arbitrum) - 8h funding
- **Paradex** (Arbitrum) - 8h funding
- **EdgeX** (Arbitrum) - 8h funding
- **Hibachi** (Arbitrum) - 8h funding
- **Variational** (Arbitrum) - 8h funding
- **Kuma** (Arbitrum) - 8h funding
- **Pacifica** (Arbitrum) - 8h funding
- **Ethereal** (Arbitrum) - 8h funding
- **Vest** (Arbitrum) - 1h funding
- **Bluefin** (Arbitrum) - 1h funding
- **Extended** (Arbitrum) - 4h funding
- **WOOFi Pro** (Arbitrum) - 8h funding

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd clob-perp-arbitrage
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## How It Works

1. **Data Collection**: The application fetches funding rates from multiple CLOB perpetual DEXes using their respective APIs
2. **Normalization**: Rates are normalized to account for different funding intervals (1h, 4h, 8h)
3. **Arbitrage Calculation**: For each token, the system calculates the spread between exchanges
4. **Opportunity Ranking**: Opportunities are ranked by spread and APY potential
5. **Real-time Updates**: Data refreshes automatically every 60 seconds

## Architecture

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **SWR** for data fetching

### Backend
- **Next.js API Routes** for server-side data handling
- **Axios** for HTTP requests
- **Exchange API integrations** for real-time data

### Data Flow
```
Exchange APIs → API Manager → Next.js Route → Frontend → UI Components
```

## Key Components

- `src/app/page.tsx` - Main dashboard with arbitrage opportunities table
- `src/components/StatsCards.tsx` - Statistics overview cards
- `src/components/ExchangeFilter.tsx` - Exchange filtering component
- `src/api/` - Exchange API integrations
- `src/lib/constants.ts` - Exchange configurations and constants

## Mock Data

The application currently uses mock data for demonstration purposes. To enable real data:

1. Uncomment the real API calls in `src/app/api/opportunities/route.ts`
2. Add API keys and configurations for each exchange
3. Set up proper rate limiting and error handling

## Contributing

1. Fork the repository
2. Feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for informational purposes only. Cryptocurrency trading involves substantial risk of loss. Always do your own research before making any trading decisions.
