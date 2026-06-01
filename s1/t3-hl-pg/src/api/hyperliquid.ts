import { BaseExchangeAPI } from './base';
import { FundingRate, Token } from '@/types';

export class HyperliquidAPI extends BaseExchangeAPI {
  constructor() {
    super({
      name: 'Hyperliquid',
      baseURL: 'https://api.hyperliquid.xyz/info',
      rateLimitMs: 1000,
    });
  }

  async getFundingRates(): Promise<FundingRate[]> {
    try {
      const response = await this.makeRequest('/meta') as any;
      const fundingRates: FundingRate[] = [];
      
      if (response.universe) {
        response.universe.forEach((market: any) => {
          if (market.funding) {
            fundingRates.push({
              exchange: 'hyperliquid',
              symbol: market.name.replace('USDT', ''),
              rate: market.funding.rate * 10000, // Convert to basis points
              nextFundingTime: new Date(Date.now() + 3600000), // 1 hour
              openInterest: market.openInterest || 0,
              volume24h: market.volume24h || 0,
            });
          }
        });
      }
      
      return fundingRates;
    } catch (error) {
      console.error('Failed to fetch Hyperliquid funding rates:', error);
      return [];
    }
  }

  async getMarkets(): Promise<Token[]> {
    try {
      const response = await this.makeRequest('/meta') as any;
      
      if (response.universe) {
        return response.universe.map((market: any) => ({
          symbol: market.name.replace('USDT', ''),
          name: market.name,
          decimals: market.szDecimals || 6,
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Failed to fetch Hyperliquid markets:', error);
      return [];
    }
  }
}
