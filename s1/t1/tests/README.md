# Test Suite

## Quick Start

```bash
# From project root, run all tests:
./run_tests.sh

# Or iterate until functional:
./iterate_until_functional.sh
```

## Test Files

- `test_e2e.py` - End-to-end tests (API clients, arbitrage logic, full flow)
- `test_api_integration.py` - FastAPI endpoint tests

## What Gets Tested

### API Clients (test_e2e.py)
- ✅ Manifold Markets connectivity
- ✅ Kalshi connectivity
- ✅ Polymarket connectivity
- ✅ Market data structure
- ✅ Price validity (0-1 range)
- ✅ Error handling

### Arbitrage Logic (test_e2e.py)
- ✅ Calculation accuracy
- ✅ ROI computation
- ✅ Strategy generation
- ✅ Opportunity finding
- ✅ Question matching

### API Endpoints (test_api_integration.py)
- ✅ GET /health
- ✅ GET /
- ✅ GET /markets
- ✅ GET /arbitrage

### End-to-End Flow (test_e2e.py)
- ✅ Market fetching from all platforms
- ✅ Data aggregation
- ✅ Arbitrage detection
- ✅ Result structure validation

## Expected Results

### All Working
```
============================================================
TEST SUMMARY
============================================================
Total Tests: 18
✅ Passed: 18
❌ Failed: 0
⚠️  Warnings: 0
```

### Some APIs Unavailable (Normal)
```
============================================================
TEST SUMMARY
============================================================
Total Tests: 18
✅ Passed: 16
❌ Failed: 0
⚠️  Warnings: 2

Warnings:
  - Polymarket API connectivity: Connection timeout
  - Polymarket market structure: No markets to test
```

This is **expected** - app still works with Manifold + Kalshi.

## Running Individual Tests

```bash
# E2E tests only
python3 tests/test_e2e.py

# API integration tests only
python3 tests/test_api_integration.py

# Unit tests (from project root)
python3 test_arbitrage.py
```

## Test Output Explained

### ✅ Pass
Test completed successfully.

### ❌ Fail
Test encountered an error or assertion failure.

### ⚠️ Warning
Non-critical issue (e.g., API unavailable but app still works).

### ℹ️ Info
Informational message about test results.

## Troubleshooting

### Import Errors
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
python3 tests/test_e2e.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### All Tests Failing
Check that you're running from the project root directory:
```bash
cd /path/to/project/root
./run_tests.sh
```

## See Also

- `../TESTING.md` - Comprehensive testing documentation
- `../TROUBLESHOOTING.md` - Debug guide
- `../run_tests.sh` - Test runner script
- `../iterate_until_functional.sh` - Automated validation
