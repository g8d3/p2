import { HyperliquidAPI } from './hyperliquid';
import { FundingRate } from '@/types';

export class ExchangeAPIManager {
  private apis: Map<string, any> = new Map();

  constructor() {
    // Initialize exchange APIs
    this.apis.set('hyperliquid', new HyperliquidAPI());
    // Add more exchanges here as they're implemented
  }

  async getFundingRates(exchangeId?: string): Promise<FundingRate[]> {
    const rates: FundingRate[] = [];

    if (exchangeId && this.apis.has(exchangeId)) {
      try {
        const api = this.apis.get(exchangeId);
        const exchangeRates = await api.getFundingRates();
        rates.push(...exchangeRates);
      } catch (error) {
        console.error(`Failed to fetch rates for ${exchangeId}:`, error);
      }
    } else {
      // Fetch from all exchanges
      const promises = Array.from(this.apis.values()).map(async (api) => {
        try {
          return await api.getFundingRates();
        } catch (error) {
          console.error(`Failed to fetch rates:`, error);
          return [];
        }
      });

      const results = await Promise.all(promises);
      rates.push(...results.flat());
    }

    return rates;
  }

  async getArbitrageOpportunities() {
    const fundingRates = await this.getFundingRates();
    
    // Group rates by symbol
    const ratesBySymbol = new Map<string, FundingRate[]>();
    fundingRates.forEach(rate => {
      if (!ratesBySymbol.has(rate.symbol)) {
        ratesBySymbol.set(rate.symbol, []);
      }
      ratesBySymbol.get(rate.symbol)!.push(rate);
    });

    // Calculate arbitrage opportunities
    const opportunities = [];
    
    for (const [symbol, rates] of ratesBySymbol.entries()) {
      if (rates.length >= 2) {
        // Find the best arbitrage pair
        for (let i = 0; i < rates.length; i++) {
          for (let j = i + 1; j < rates.length; j++) {
            const rate1 = rates[i];
            const rate2 = rates[j];
            const spread = Math.abs(rate1.rate - rate2.rate);
            
            // Only include meaningful opportunities (> 50 bps)
            if (spread > 50) {
              const apy = (spread * 365 * 24) / 8; // Assuming 8-hour normalization
              
              opportunities.push({
                symbol,
                exchange1: rate1.exchange,
                exchange2: rate2.exchange,
                spread,
                apy,
                rate1: rate1.rate,
                rate2: rate2.rate,
                nextFunding1: rate1.nextFundingTime,
                nextFunding2: rate2.nextFundingTime,
                volume1: rate1.volume24h,
                volume2: rate2.volume24h,
                oi1: rate1.openInterest,
                oi2: rate2.openInterest,
              });
            }
          }
        }
      }
    }

    // Sort by spread descending
    return opportunities.sort((a, b) => b.spread - a.spread);
  }
}
