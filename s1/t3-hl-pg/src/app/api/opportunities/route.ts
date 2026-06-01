import { NextResponse } from 'next/server';
import { ExchangeAPIManager } from '@/api';
import { generateMockArbitrageOpportunities } from '@/lib/mockData';

export async function GET() {
  try {
    // For now, use mock data. In production, you would uncomment the real API calls:
    // const apiManager = new ExchangeAPIManager();
    // const opportunities = await apiManager.getArbitrageOpportunities();
    
    // Mock data for demonstration
    const opportunities = generateMockArbitrageOpportunities();
    
    return NextResponse.json({
      opportunities,
      lastUpdated: new Date().toISOString(),
      count: opportunities.length,
    });
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    return NextResponse.json(
      { error: 'Failed to fetch arbitrage opportunities' },
      { status: 500 }
    );
  }
}
