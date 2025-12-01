# Troubleshooting Guide

## Quick Diagnostics

### Check if Backend is Running
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

### Test Each API Client

#### 1. Kalshi (Should work)
```bash
curl "http://localhost:8000/markets?limit=3" | grep -o '"kalshi":\[[^]]*\]' | head -20
```

#### 2. Manifold Markets
```bash
curl "https://api.manifold.markets/v0/markets?limit=1"
```

#### 3. Polymarket Events
```bash
curl -H "User-Agent: Mozilla/5.0" "https://gamma-api.polymarket.com/events?limit=1"
```

## Common Issues & Solutions

### Issue: Dependencies Not Installed

**Error**: `ModuleNotFoundError: No module named 'httpx'`

**Solution**:
```bash
pip install -r requirements.txt
```

Or with venv:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port 8000 Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)

# Or run on different port
uvicorn main:app --port 8001
```

### Issue: Manifold 400 Error

**Error**: `400 Bad Request` for Manifold Markets

**Status**: ✅ **FIXED** in latest version

**What was fixed**: Removed invalid `filter=open` parameter

**Verify fix**:
```bash
# Check manifold.py doesn't have 'filter' in params
grep -n "filter" backend/api_clients/manifold.py
```

Should not show `"filter": "open"` in params

### Issue: Polymarket Connection Failed

**Error**: `All connection attempts failed`

**Status**: ⚠️ **Enhanced** - May need additional access

**What was improved**:
- Added User-Agent header
- Added dual-endpoint strategy (events + markets)
- Better error handling

**Check if accessible**:
```bash
# Test events endpoint
curl -v -H "User-Agent: Mozilla/5.0" \
  "https://gamma-api.polymarket.com/events?limit=1"

# Test markets endpoint  
curl -v -H "User-Agent: Mozilla/5.0" \
  "https://gamma-api.polymarket.com/markets?limit=1"
```

**Possible causes if still failing**:
1. Network/firewall blocking
2. Geographic restrictions
3. Rate limiting
4. Requires API authentication

**Workaround**: App still works with just Kalshi + Manifold

### Issue: No Arbitrage Opportunities Found

**Not an error** - This is normal if:
- Market prices are efficient
- Not enough markets analyzed
- ROI threshold too high

**Solutions**:
```bash
# Lower the minimum ROI
curl "http://localhost:8000/arbitrage?min_roi=0.5&limit=100"

# Increase markets analyzed
curl "http://localhost:8000/arbitrage?limit=200"
```

### Issue: CORS Errors in Browser

**Error**: `Access-Control-Allow-Origin`

**Status**: ✅ Should be configured

**Verify**:
```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

**Fix if needed**: Restart backend server

### Issue: Empty Response from /markets

**Check each platform**:
```bash
curl "http://localhost:8000/markets?limit=10" | python3 -m json.tool
```

**Expected structure**:
```json
{
  "polymarket": [...],
  "kalshi": [...],
  "manifold": [...],
  "total": 150
}
```

**If one platform is empty**, check logs:
```bash
# Start server with debug logging
cd backend
python main.py 2>&1 | tee server.log
```

## Debugging Tools

### View Live Logs
```bash
# In one terminal - start server
cd backend
python main.py

# In another terminal - watch requests
curl "http://localhost:8000/arbitrage?limit=5"
```

### Test Individual Functions

#### Test Manifold Client
```python
import asyncio
from api_clients.manifold import ManifoldClient

async def test():
    client = ManifoldClient()
    markets = await client.get_markets(limit=3)
    print(f"Found {len(markets)} markets")
    for m in markets[:3]:
        print(f"- {m['question'][:50]}...")
    await client.close()

asyncio.run(test())
```

#### Test Arbitrage Logic
```python
from arbitrage import calculate_arbitrage

market1 = {
    "platform": "manifold",
    "question": "Test market",
    "prices": {"Yes": 0.70, "No": 0.30},
    "url": "https://example.com"
}

market2 = {
    "platform": "kalshi", 
    "question": "Test market",
    "prices": {"Yes": 0.25, "No": 0.75},
    "url": "https://example.com"
}

result = calculate_arbitrage(market1, market2)
print(f"Arbitrage exists: {result['arbitrage']['exists']}")
print(f"ROI: {result['arbitrage']['roi_percentage']}%")
```

### Check API Endpoints Directly

#### FastAPI Auto Docs
```bash
# Open in browser
http://localhost:8000/docs
```

Interactive API documentation with try-it-out functionality

## Environment Variables

### Check Current Config
```bash
# View environment template
cat .env.example

# Check if .env exists
ls -la .env
```

### Set API Keys (Optional)
```bash
# Copy template
cp .env.example .env

# Edit with your keys
nano .env

# Add:
# KALSHI_API_KEY=your_key
# KALSHI_API_SECRET=your_secret
# POLYMARKET_API_KEY=your_key
```

**Note**: App works without API keys for read-only access

## Performance Issues

### Slow Response Times

**Check**:
1. Network latency to APIs
2. Number of markets being analyzed
3. Complexity of matching algorithm

**Solutions**:
```bash
# Reduce market limit
curl "http://localhost:8000/arbitrage?limit=20"

# Check response time
time curl "http://localhost:8000/arbitrage"
```

### High Memory Usage

**Check**:
```bash
# Monitor while running
top -p $(pgrep -f "main.py")
```

**Solutions**:
- Reduce `limit` parameter
- Implement pagination
- Add caching

## Network Issues

### Test Connectivity
```bash
# Test each API
ping api.manifold.markets
ping api.elections.kalshi.com
ping gamma-api.polymarket.com

# Test HTTPS
curl -I https://api.manifold.markets
curl -I https://api.elections.kalshi.com  
curl -I https://gamma-api.polymarket.com
```

### Behind Proxy/Firewall

**Set proxy** (if needed):
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

## Getting Help

### Collect Debug Info
```bash
# System info
python3 --version
curl --version

# Check dependencies
pip list | grep -E "fastapi|httpx|pydantic"

# Test endpoints
curl -v "http://localhost:8000/health"
curl -v "http://localhost:8000/markets?limit=1"

# Check logs
cd backend && python main.py 2>&1 | grep ERROR
```

### Report Issue
Include:
1. Error message
2. Python version
3. Operating system
4. Steps to reproduce
5. Relevant logs

## Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend starts without errors (`python backend/main.py`)
- [ ] Health check returns OK (`curl localhost:8000/health`)
- [ ] Markets endpoint returns data (`curl localhost:8000/markets`)
- [ ] Arbitrage endpoint works (`curl localhost:8000/arbitrage`)
- [ ] Frontend loads (open `frontend/index.html`)
- [ ] Can see opportunities in UI

## Quick Fixes Reference

| Issue | Quick Fix |
|-------|-----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Port in use | `kill -9 $(lsof -ti:8000)` |
| Manifold 400 | ✅ Already fixed (update code) |
| Polymarket fails | ⚠️ Expected, app still works |
| No opportunities | Lower `min_roi` or increase `limit` |
| CORS error | Restart backend server |
| Slow response | Reduce `limit` parameter |

## Still Having Issues?

1. Check `FIXES_APPLIED.md` for recent fixes
2. Review error logs in `errors/` directory
3. Test with minimal config (just Kalshi + Manifold)
4. Try running with verbose logging

The app is designed to be resilient - it should work even if one platform fails!
