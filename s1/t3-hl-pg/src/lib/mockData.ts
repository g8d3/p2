import { FundingRate, ArbitrageOpportunity } from '@/types';
import { SUPPORTED_EXCHANGES } from './constants';

// Mock funding rates for demonstration
export const generateMockFundingRates = (): Record<string, FundingRate[]> => {
  const rates: Record<string, FundingRate[]> = {};
  
  const tokens = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC'];
  
  tokens.forEach(token => {
    rates[token] = SUPPORTED_EXCHANGES.map(exchange => ({
      exchange: exchange.id,
      symbol: token,
      rate: Math.random() * 200 - 100, // Random rate between -100 and +100 bps
      nextFundingTime: new Date(Date.now() + Math.random() * 3600000), // Next funding within 1 hour
      openInterest: Math.random() * 1000000000, // Random OI up to 1B
      volume24h: Math.random() * 100000000, // Random volume up to 100M
    }));
  });
  
  return rates;
};

// Mock arbitrage opportunities
export const generateMockArbitrageOpportunities = (): ArbitrageOpportunity[] => {
  const opportunities: ArbitrageOpportunity[] = [];
  const tokens = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC'];
  
  tokens.forEach(token => {
    // Generate 1-3 opportunities per token
    const numOpportunities = Math.floor(Math.random() * 3) + 1;
    
    for (let i = 0; i < numOpportunities; i++) {
      const exchange1 = SUPPORTED_EXCHANGES[Math.floor(Math.random() * SUPPORTED_EXCHANGES.length)];
      let exchange2 = SUPPORTED_EXCHANGES[Math.floor(Math.random() * SUPPORTED_EXCHANGES.length)];
      
      // Ensure different exchanges
      while (exchange2.id === exchange1.id) {
        exchange2 = SUPPORTED_EXCHANGES[Math.floor(Math.random() * SUPPORTED_EXCHANGES.length)];
      }
      
      const rate1 = Math.random() * 200 - 100;
      const rate2 = Math.random() * 200 - 100;
      const spread = Math.abs(rate1 - rate2);
      
      // Only include opportunities with meaningful spreads (> 50 bps)
      if (spread > 50) {
        opportunities.push({
          symbol: token,
          exchange1: exchange1.id,
          exchange2: exchange2.id,
          spread,
          apy: (spread * 365 * 24) / (Math.max(exchange1.fundingInterval, exchange2.fundingInterval)),
          rate1,
          rate2,
          nextFunding1: new Date(Date.now() + Math.random() * 3600000),
          nextFunding2: new Date(Date.now() + Math.random() * 3600000),
          volume1: Math.random() * 100000000,
          volume2: Math.random() * 100000000,
          oi1: Math.random() * 1000000000,
          oi2: Math.random() * 1000000000,
        });
      }
    }
  });
  
  // Sort by spread descending
  return opportunities.sort((a, b) => b.spread - a.spread);
};
