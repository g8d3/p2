'use client'

import { ArbitrageOpportunity } from '@/types';
import { TrendingUp, DollarSign, Activity, Clock } from 'lucide-react';

interface StatsCardsProps {
  opportunities: ArbitrageOpportunity[];
}

export default function StatsCards({ opportunities }: StatsCardsProps) {
  // Calculate statistics
  const totalOpportunities = opportunities.length;
  const avgSpread = opportunities.length > 0 
    ? opportunities.reduce((sum, opp) => sum + opp.spread, 0) / opportunities.length 
    : 0;
  const maxApy = opportunities.length > 0 
    ? Math.max(...opportunities.map(opp => opp.apy))
    : 0;
  const totalVolume = opportunities.reduce((sum, opp) => sum + opp.volume1 + opp.volume2, 0);

  const cards = [
    {
      title: 'Total Opportunities',
      value: totalOpportunities.toString(),
      icon: Activity,
      color: 'text-blue-400',
      bgGradient: 'from-blue-500/20 to-blue-600/20',
    },
    {
      title: 'Average Spread',
      value: `${avgSpread.toFixed(1)} bps`,
      icon: TrendingUp,
      color: 'text-green-400',
      bgGradient: 'from-green-500/20 to-green-600/20',
    },
    {
      title: 'Max APY',
      value: `${maxApy.toFixed(0)}%`,
      icon: DollarSign,
      color: 'text-purple-400',
      bgGradient: 'from-purple-500/20 to-purple-600/20',
    },
    {
      title: 'Total Volume 24h',
      value: totalVolume > 1000000 
        ? `$${(totalVolume / 1000000).toFixed(1)}M`
        : totalVolume > 1000 
          ? `$${(totalVolume / 1000).toFixed(1)}K`
          : `$${totalVolume.toFixed(0)}`,
      icon: Clock,
      color: 'text-yellow-400',
      bgGradient: 'from-yellow-500/20 to-yellow-600/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {cards.map((card, index) => (
        <div
          key={index}
          className={`bg-gray-900 border border-gray-800 rounded-xl p-6 bg-gradient-to-br ${card.bgGradient}`}
        >
          <div className="flex items-center justify-between mb-2">
            <card.icon className={`w-5 h-5 ${card.color}`} />
            <div className={`text-xs px-2 py-1 rounded-full bg-gray-800 text-gray-400`}>
              {card.title.includes('Total') ? 'All' : 'Avg'}
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {card.value}
          </div>
          <div className="text-sm text-gray-400">
            {card.title}
          </div>
        </div>
      ))}
    </div>
  );
}
