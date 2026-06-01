import { generateMockArbitrageOpportunities, generateMockFundingRates } from '@/lib/mockData';
import { SUPPORTED_EXCHANGES } from '@/lib/constants';

describe('Mock Data Generators', () => {
  describe('generateMockFundingRates', () => {
    it('should generate funding rates for supported exchanges', () => {
      const rates = generateMockFundingRates();
      const exchangeIds = Object.keys(rates);
      
      expect(exchangeIds.length).toBeGreaterThan(0);
      
      Object.values(rates).forEach(tokenRates => {
        expect(tokenRates).toHaveLength(SUPPORTED_EXCHANGES.length);
        tokenRates.forEach(rate => {
          expect(rate).toHaveProperty('exchange');
          expect(rate).toHaveProperty('symbol');
          expect(rate).toHaveProperty('rate');
          expect(rate).toHaveProperty('nextFundingTime');
          expect(rate).toHaveProperty('openInterest');
          expect(rate).toHaveProperty('volume24h');
        });
      });
    });
  });

  describe('generateMockArbitrageOpportunities', () => {
    it('should generate valid arbitrage opportunities', () => {
      const opportunities = generateMockArbitrageOpportunities();
      
      expect(Array.isArray(opportunities)).toBe(true);
      
      opportunities.forEach(opp => {
        expect(opp).toHaveProperty('symbol');
        expect(opp).toHaveProperty('exchange1');
        expect(opp).toHaveProperty('exchange2');
        expect(opp).toHaveProperty('spread');
        expect(opp).toHaveProperty('apy');
        expect(opp).toHaveProperty('rate1');
        expect(opp).toHaveProperty('rate2');
        expect(opp.spread).toBeGreaterThan(50); // Should only include meaningful opportunities
        expect(opp.exchange1).not.toBe(opp.exchange2); // Should be different exchanges
      });
    });

    it('should sort opportunities by spread descending', () => {
      const opportunities = generateMockArbitrageOpportunities();
      
      for (let i = 1; i < opportunities.length; i++) {
        expect(opportunities[i - 1].spread).toBeGreaterThanOrEqual(opportunities[i].spread);
      }
    });
  });
});
