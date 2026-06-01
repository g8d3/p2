'use client'

import { useState, useEffect } from 'react';
import { ArbitrageOpportunity, SortField, SortDirection } from '@/types';
import { generateMockArbitrageOpportunities } from '@/lib/mockData';
import { SUPPORTED_EXCHANGES } from '@/lib/constants';
import { formatBps, formatApy, formatVolume, formatTimeUntil } from '@/lib/utils';
import { ArrowUpDown, ArrowUp, ArrowDown, Clock, TrendingUp } from 'lucide-react';
import ExchangeFilter from '@/components/ExchangeFilter';
import StatsCards from '@/components/StatsCards';

export default function Home() {
  const [opportunities, setOpportunities] = useState<ArbitrageOpportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortField, setSortField] = useState<SortField>('spread');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');
  const [refreshTime, setRefreshTime] = useState(new Date());
  const [countdown, setCountdown] = useState(60);

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          fetchData();
          return 60;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    setLoading(true);
    // In a real app, this would fetch from your API
    const data = generateMockArbitrageOpportunities();
    setOpportunities(data);
    setRefreshTime(new Date());
    setLoading(false);
  };

  const sortData = (field: SortField) => {
    const newDirection = sortField === field && sortDirection === 'desc' ? 'asc' : 'desc';
    setSortField(field);
    setSortDirection(newDirection);

    const sorted = [...opportunities].sort((a, b) => {
      let comparison = 0;
      
      switch (field) {
        case 'spread':
          comparison = a.spread - b.spread;
          break;
        case 'apy':
          comparison = a.apy - b.apy;
          break;
        case 'symbol':
          comparison = a.symbol.localeCompare(b.symbol);
          break;
        case 'volume':
          comparison = (a.volume1 + a.volume2) - (b.volume1 + b.volume2);
          break;
      }
      
      return newDirection === 'desc' ? -comparison : comparison;
    });

    setOpportunities(sorted);
  };

  const renderSortIcon = (field: SortField) => {
    if (sortField !== field) return <ArrowUpDown className="w-4 h-4" />;
    return sortDirection === 'desc' ? <ArrowDown className="w-4 h-4" /> : <ArrowUp className="w-4 h-4" />;
  };

  const getExchangeIcon = (exchangeId: string) => {
    const exchange = SUPPORTED_EXCHANGES.find(e => e.id === exchangeId);
    if (exchange) {
      return (
        <div className="flex items-center gap-1">
          <div className="w-4 h-4 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
            {exchange.name[0]}
          </div>
          <span className="text-xs font-medium">{exchange.name.toUpperCase()}</span>
        </div>
      );
    }
    return <span className="text-xs">{exchangeId.toUpperCase()}</span>;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
            <p className="mt-4">Loading arbitrage opportunities...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            CLOB Perpetual DEX Arbitrage Tools
          </h1>
          <p className="text-gray-400 mb-6">
            Real-time funding rate arbitrage opportunities across decentralized exchanges
          </p>
          
          {/* Status Bar */}
          <div className="flex items-center justify-between bg-gray-900 rounded-lg px-4 py-3 border border-gray-800">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-green-400" />
                <span className="text-sm">Auto-refresh: {countdown}s</span>
              </div>
              <div className="text-sm text-gray-400">
                Last updated: {refreshTime.toLocaleTimeString()}
              </div>
            </div>
            <div className="flex items-center gap-4">
              <ExchangeFilter />
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-green-400" />
                <span className="text-sm">
                  {opportunities.length} opportunities found
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Stats Cards */}
        <StatsCards opportunities={opportunities} />

        {/* Main Table */}
        <main>
          <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="text-left p-4 font-medium text-gray-400">
                      <button
                        onClick={() => sortData('symbol')}
                        className="flex items-center gap-2 hover:text-white transition-colors"
                      >
                        TOKEN
                        {renderSortIcon('symbol')}
                      </button>
                    </th>
                    <th className="text-left p-4 font-medium text-gray-400">TRADE</th>
                    <th className="text-left p-4 font-medium text-gray-400">
                      <button
                        onClick={() => sortData('spread')}
                        className="flex items-center gap-2 hover:text-white transition-colors"
                      >
                        SPREAD
                        {renderSortIcon('spread')}
                      </button>
                    </th>
                    <th className="text-left p-4 font-medium text-gray-400">
                      <button
                        onClick={() => sortData('apy')}
                        className="flex items-center gap-2 hover:text-white transition-colors"
                      >
                        APY
                        {renderSortIcon('apy')}
                      </button>
                    </th>
                    <th className="text-left p-4 font-medium text-gray-400">VOLUME</th>
                    <th className="text-left p-4 font-medium text-gray-400">NEXT FUNDING</th>
                  </tr>
                </thead>
                <tbody>
                  {opportunities.slice(0, 50).map((opp, index) => (
                    <tr key={`${opp.symbol}-${opp.exchange1}-${opp.exchange2}`} className="border-b border-gray-800 hover:bg-gray-800/50 transition-colors">
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <span className="text-2xl font-bold text-blue-400">#{index + 1}</span>
                          <div>
                            <div className="font-semibold">{opp.symbol}</div>
                            <div className="text-xs text-gray-400">
                              OI Rank: {Math.floor(Math.random() * 500) + 1}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          {getExchangeIcon(opp.exchange1)}
                          <span className="text-gray-400">→</span>
                          {getExchangeIcon(opp.exchange2)}
                        </div>
                      </td>
                      <td className="p-4">
                        <div>
                          <div className={`font-semibold ${opp.spread > 300 ? 'text-green-400' : opp.spread > 150 ? 'text-yellow-400' : 'text-gray-300'}`}>
                            {formatBps(opp.spread)}
                          </div>
                          <div className="text-xs text-gray-400">
                            {formatApy(opp.apy)}
                          </div>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="text-sm">
                          {opp.rate1 > 0 ? (
                            <span className="text-blue-400">{formatBps(opp.rate1)}</span>
                          ) : (
                            <span className="text-red-400">{formatBps(opp.rate1)}</span>
                          )}
                          <span className="text-gray-400 mx-1">/</span>
                          {opp.rate2 > 0 ? (
                            <span className="text-blue-400">{formatBps(opp.rate2)}</span>
                          ) : (
                            <span className="text-red-400">{formatBps(opp.rate2)}</span>
                          )}
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="text-sm">
                          {formatVolume(opp.volume1)}
                          <span className="text-gray-400 mx-1">/</span>
                          {formatVolume(opp.volume2)}
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="text-sm">
                          {formatTimeUntil(opp.nextFunding1)}
                          <span className="text-gray-400 mx-1">/</span>
                          {formatTimeUntil(opp.nextFunding2)}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-gray-400 text-sm">
            <p>Connected to {SUPPORTED_EXCHANGES.length} CLOB perpetual DEXes</p>
            <p className="mt-2">Data refreshes every 60 seconds • Last updated {refreshTime.toLocaleTimeString()}</p>
          </div>
        </main>
      </div>
    </div>
  );
}
