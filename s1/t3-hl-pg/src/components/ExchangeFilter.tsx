'use client'

import { useState } from 'react';
import { SUPPORTED_EXCHANGES } from '@/lib/constants';
import { Filter } from 'lucide-react';

export default function ExchangeFilter() {
  const [selectedExchanges, setSelectedExchanges] = useState<Set<string>>(
    new Set(SUPPORTED_EXCHANGES.map(e => e.id))
  );
  const [isOpen, setIsOpen] = useState(false);

  const toggleExchange = (exchangeId: string) => {
    const newSelected = new Set(selectedExchanges);
    if (newSelected.has(exchangeId)) {
      newSelected.delete(exchangeId);
    } else {
      newSelected.add(exchangeId);
    }
    setSelectedExchanges(newSelected);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-gray-900 border border-gray-800 rounded-lg hover:bg-gray-800 transition-colors"
      >
        <Filter className="w-4 h-4" />
        <span>Exchanges ({selectedExchanges.size})</span>
      </button>

      {isOpen && (
        <div className="absolute top-12 left-0 z-10 w-80 bg-gray-900 border border-gray-800 rounded-lg shadow-xl p-4">
          <div className="max-h-60 overflow-y-auto">
            {SUPPORTED_EXCHANGES.map(exchange => (
              <label
                key={exchange.id}
                className="flex items-center gap-3 p-2 hover:bg-gray-800 rounded cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedExchanges.has(exchange.id)}
                  onChange={() => toggleExchange(exchange.id)}
                  className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                />
                <div className="flex-1">
                  <div className="font-medium">{exchange.name}</div>
                  <div className="text-xs text-gray-400">
                    {exchange.type.toUpperCase()} • {exchange.chain}
                  </div>
                </div>
                <div className="text-xs px-2 py-1 bg-gray-800 rounded">
                  {exchange.fundingInterval}h
                </div>
              </label>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-800 flex justify-between">
            <button
              onClick={() => setSelectedExchanges(new Set(SUPPORTED_EXCHANGES.map(e => e.id)))}
              className="text-sm text-blue-400 hover:text-blue-300"
            >
              Select All
            </button>
            <button
              onClick={() => setSelectedExchanges(new Set())}
              className="text-sm text-red-400 hover:text-red-300"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
