export interface Exchange {
  id: string;
  name: string;
  type: 'clob' | 'amm';
  chain?: string;
  fundingInterval: number; // in hours
  icon?: string;
}

export interface FundingRate {
  exchange: string;
  symbol: string;
  rate: number; // in basis points
  nextFundingTime: Date;
  openInterest: number;
  volume24h: number;
}

export interface ArbitrageOpportunity {
  symbol: string;
  exchange1: string;
  exchange2: string;
  spread: number; // in basis points
  apy: number; // annualized percentage yield
  rate1: number;
  rate2: number;
  nextFunding1: Date;
  nextFunding2: Date;
  volume1: number;
  volume2: number;
  oi1: number;
  oi2: number;
}

export interface Token {
  symbol: string;
  name: string;
  decimals: number;
}

export interface MarketData {
  [symbol: string]: {
    [exchange: string]: FundingRate;
  };
}

export type SortField = 'spread' | 'apy' | 'symbol' | 'volume';
export type SortDirection = 'asc' | 'desc';
