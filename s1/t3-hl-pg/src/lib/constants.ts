import { Exchange } from '@/types';

export const SUPPORTED_EXCHANGES: Exchange[] = [
  // CLOB DEXes
  { id: 'hyperliquid', name: 'Hyperliquid', type: 'clob', chain: 'Arbitrum', fundingInterval: 1 },
  { id: 'drift', name: 'Drift', type: 'clob', chain: 'Solana', fundingInterval: 1 },
  { id: 'aster', name: 'Aster', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'lighter', name: 'Lighter', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'paradex', name: 'Paradex', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'edgex', name: 'EdgeX', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'hibachi', name: 'Hibachi', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'variational', name: 'Variational', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'kuma', name: 'Kuma', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'pacifica', name: 'Pacifica', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'ethereal', name: 'Ethereal', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
  { id: 'vest', name: 'Vest', type: 'clob', chain: 'Arbitrum', fundingInterval: 1 },
  { id: 'bluefin', name: 'Bluefin', type: 'clob', chain: 'Arbitrum', fundingInterval: 1 },
  { id: 'extended', name: 'Extended', type: 'clob', chain: 'Arbitrum', fundingInterval: 4 },
  { id: 'woofi', name: 'WOOFi Pro', type: 'clob', chain: 'Arbitrum', fundingInterval: 8 },
];

export const POPULAR_TOKENS = [
  'BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'MATIC', 'DOT', 'AVAX',
  'LINK', 'UNI', 'LTC', 'ATOM', 'FIL', 'ALGO', 'VET', 'ICP', 'HBAR', 'QNT'
];

export const REFRESH_INTERVAL = 60000; // 1 minute in milliseconds

export const CHAINS = {
  'Arbitrum': '#28A0F0',
  'Solana': '#9945FF',
  'Ethereum': '#627EEA',
  'Base': '#005DFF',
  'Optimism': '#FF0420',
};
