# DEX Funding Rate Arbitrage Test Suite

This directory contains comprehensive tests for the DEX funding rate arbitrage application.

## Test Files

- `test_arbitrage.py` - Unit tests for arbitrage detection logic and DEX clients
- `test_e2e.py` - End-to-end tests for the complete application workflow

## Running Tests

### Unit Tests
```bash
pytest tests/test_arbitrage.py -v
```

### End-to-End Tests
```bash
# Start the application first
python backend/main.py

# In another terminal, run E2E tests
python tests/test_e2e.py
```

### All Tests
```bash
pytest tests/ -v
```

## Test Coverage

### Core Functionality
- Arbitrage opportunity detection algorithm
- DEX client implementations
- Funding rate calculation and validation
- Symbol normalization and matching

### API Endpoints
- Health check endpoint
- Markets data retrieval
- Funding rates collection
- Arbitrage opportunity detection with filters

### Data Validation
- Funding rate consistency checks
- Market data structure validation
- Error handling and edge cases

### E2E Workflow
- Complete user journey from startup to arbitrage detection
- Frontend data consumption testing
- Performance benchmarking
- Real DEX API integration testing

## Test Scenarios

### Happy Path
- ✅ Detect profitable arbitrage opportunities
- ✅ Display correct profit calculations
- ✅ Sort opportunities by profitability
- ✅ Filter results by minimum spread

### Edge Cases
- ✅ Empty market data handling
- ✅ Single exchange scenarios (no arbitrage)
- ✅ Invalid API responses
- ✅ Network timeouts and errors

### Data Validation
- ✅ Funding rate ranges (-10% to +10% annually)
- ✅ Funding time validation (next 24 hours)
- ✅ Market symbol consistency
- ✅ Profit calculation accuracy

## Requirements for E2E Tests

- **App Running**: The FastAPI server must be running on port 8000
- **Network Access**: Tests attempt to connect to real DEX APIs
- **Dependencies**: Install `requests` in addition to requirements.txt

```bash
pip install requests
```

## Troubleshooting

If E2E tests fail:

1. **Server Not Running**: Start the application with `python backend/main.py`
2. **API Rate Limits**: Some DEX APIs may have rate limits
3. **Network Issues**: Check internet connectivity for DEX API access
4. **Test Retry**: External API calls may be flaky, rerun tests

## Expected Test Results

When working correctly, the app should:
- Load markets from at least 2 DEXs
- Calculate funding rates correctly
- Find arbitrage opportunities when funding rates differ
- Display profitable opportunities with proper metadata
- Handle errors gracefully when APIs are unavailable

## Performance Benchmarks

- **Health Check**: < 1 second response time
- **Arbitrage Analysis**: < 10 seconds with external API calls
- **Frontend Loading**: < 5 seconds to display opportunities
