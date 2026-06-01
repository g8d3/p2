import axios from 'axios';

export interface ExchangeAPIConfig {
  name: string;
  baseURL: string;
  headers?: Record<string, string>;
  rateLimitMs: number;
}

export abstract class BaseExchangeAPI {
  protected config: ExchangeAPIConfig;
  protected lastRequestTime = 0;

  constructor(config: ExchangeAPIConfig) {
    this.config = config;
  }

  protected async makeRequest<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    // Rate limiting
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    
    if (timeSinceLastRequest < this.config.rateLimitMs) {
      await new Promise(resolve => 
        setTimeout(resolve, this.config.rateLimitMs - timeSinceLastRequest)
      );
    }

    try {
      const response = await axios.get<T>(`${this.config.baseURL}${endpoint}`, {
        params,
        headers: {
          'Content-Type': 'application/json',
          ...this.config.headers,
        },
        timeout: 10000,
      });

      this.lastRequestTime = Date.now();
      return response.data;
    } catch (error) {
      console.error(`Error fetching from ${this.config.name}:`, error);
      throw error;
    }
  }

  abstract getFundingRates(): Promise<any>;
  abstract getMarkets(): Promise<any>;
}
