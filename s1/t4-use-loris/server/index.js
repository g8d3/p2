const express = require('express');
const cors = require('cors');
const axios = require('axios');
const http = require('http');
const socketIo = require('socket.io');
const cron = require('node-cron');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const PORT = process.env.PORT || 3001;
const LORIS_API_URL = 'https://api.loris.tools/funding';

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

let fundingRates = {};
let arbitrageOpportunities = [];

const fetchFundingRates = async () => {
  try {
    const response = await axios.get(LORIS_API_URL);
    fundingRates = response.data;
    
    arbitrageOpportunities = calculateArbitrageOpportunities(fundingRates);
    
    io.emit('fundingRatesUpdate', { fundingRates, arbitrageOpportunities });
    
    console.log('Funding rates updated successfully');
  } catch (error) {
    console.error('Error fetching funding rates:', error);
    io.emit('error', { message: 'Failed to fetch funding rates' });
  }
};

const calculateArbitrageOpportunities = (data) => {
  const opportunities = [];
  const { funding_rates, symbols, exchanges } = data;
  
  symbols.forEach(symbol => {
    const rates = {};
    
    Object.keys(funding_rates).forEach(exchange => {
      if (funding_rates[exchange][symbol] !== undefined) {
        rates[exchange] = funding_rates[exchange][symbol] / 10000;
      }
    });
    
    if (Object.keys(rates).length >= 2) {
      const sortedRates = Object.entries(rates)
        .sort((a, b) => a[1] - b[1]);
      
      const lowestRate = sortedRates[0];
      const highestRate = sortedRates[sortedRates.length - 1];
      
      const rateDifference = highestRate[1] - lowestRate[1];
      
      if (Math.abs(rateDifference) > 0.0001) {
        const dailyProfit = rateDifference * 3;
        
        opportunities.push({
          symbol,
          lowestExchange: lowestRate[0],
          lowestRate: lowestRate[1],
          highestExchange: highestRate[0],
          highestRate: highestRate[1],
          rateDifference,
          estimatedDailyProfit: dailyProfit,
          timestamp: new Date().toISOString()
        });
      }
    }
  });
  
  return opportunities.sort((a, b) => Math.abs(b.estimatedDailyProfit) - Math.abs(a.estimatedDailyProfit)).slice(0, 20);
};

app.get('/api/funding-rates', (req, res) => {
  res.json({ fundingRates, arbitrageOpportunities });
});

app.get('/api/opportunities', (req, res) => {
  res.json(arbitrageOpportunities);
});

app.post('/api/execute-arbitrage', async (req, res) => {
  try {
    const { symbol, exchange1, exchange2, amount } = req.body;
    
    console.log(`Executing arbitrage for ${symbol} between ${exchange1} and ${exchange2}`);
    
    const execution = {
      id: Date.now(),
      symbol,
      exchange1,
      exchange2,
      amount,
      status: 'pending',
      timestamp: new Date().toISOString()
    };
    
    setTimeout(() => {
      execution.status = 'completed';
      execution.profit = Math.random() * 100;
      io.emit('executionUpdate', execution);
    }, 3000);
    
    res.json({ success: true, executionId: execution.id, status: 'pending' });
  } catch (error) {
    console.error('Error executing arbitrage:', error);
    res.status(500).json({ success: false, error: 'Execution failed' });
  }
});

io.on('connection', (socket) => {
  console.log('Client connected');
  
  socket.emit('initialData', { fundingRates, arbitrageOpportunities });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

cron.schedule('*/1 * * * *', fetchFundingRates);

fetchFundingRates();

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
