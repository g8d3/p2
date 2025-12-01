# Quick Start Guide

## 🚀 Get Started in 30 Seconds

### Option 1: One Command (Recommended)
```bash
./run.sh
```

Then open your browser to:
- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs

### Option 2: Manual Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start backend**:
```bash
cd backend
python main.py
```

3. **Start frontend** (new terminal):
```bash
cd frontend
python -m http.server 8080
```

4. **Open browser**: http://localhost:8080

## 🧪 Run Tests
```bash
python test_arbitrage.py
```

## 🔑 Optional: Add API Keys

For authenticated access (higher rate limits):

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your API keys:
```bash
KALSHI_API_KEY=your_key_here
KALSHI_API_SECRET=your_secret_here
POLYMARKET_API_KEY=your_key_here
```

**Note**: The app works without API keys using public endpoints!

## 📖 How to Use

1. **Open the web app** at http://localhost:8080
2. **Click "Find Opportunities"** to search for arbitrage
3. **Adjust settings**:
   - Min ROI: Filter by minimum return percentage
   - Markets per platform: How many markets to analyze
4. **View results**: See profitable opportunities with direct links
5. **Optional**: Enable auto-refresh for continuous monitoring

## 📊 API Endpoints

Test the API directly:

```bash
# Find arbitrage opportunities
curl "http://localhost:8000/arbitrage?min_roi=1.0&limit=50"

# Get all markets
curl "http://localhost:8000/markets?limit=50"

# Health check
curl "http://localhost:8000/health"
```

## 🎯 What You'll See

The app will show you:
- **ROI %**: Your return on investment
- **Profit per $1**: How much you make per dollar invested
- **Strategy**: Which markets to buy on
- **Direct links**: To both markets for easy trading

## ⚠️ Important Notes

- Prices change rapidly - opportunities may disappear quickly
- This is for educational purposes
- Consider transaction fees when trading
- Requires accounts on each platform to actually trade

## 🆘 Troubleshooting

**Backend won't start?**
```bash
pip install --upgrade -r requirements.txt
```

**Frontend shows error?**
- Make sure backend is running on port 8000
- Check http://localhost:8000/health

**No opportunities found?**
- Try lowering the Min ROI
- Increase markets per platform
- Markets may not have arbitrage at this time

## 📚 More Info

- Full documentation: `README.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Test the arbitrage logic: `python test_arbitrage.py`

## 🎉 That's It!

You're now finding arbitrage opportunities across prediction markets!
