#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           PREDICTION MARKETS ARBITRAGE TEST SUITE            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if eval $test_command; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}"
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        FAILED=1
    fi
    echo ""
}

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"

# Run all tests
run_test "Unit Tests (Arbitrage Logic)" "python3 test_arbitrage.py"
run_test "E2E Tests (API Clients & Flow)" "python3 tests/test_e2e.py"
run_test "API Integration Tests" "python3 tests/test_api_integration.py"

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                      TEST SUMMARY                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All test suites passed!${NC}"
    echo ""
    echo "The application is functional and ready to use."
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    echo ""
    echo "Please check the output above for details."
    exit 1
fi
