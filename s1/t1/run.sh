#!/bin/bash

echo "Starting Prediction Markets Arbitrage App..."

# Check if virtual environment exists
# if [ ! -d "venv" ]; then
#     echo "Creating virtual environment..."
#     python3 -m venv venv
# fi

# Activate virtual environment
# source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Start backend server
echo "Starting backend server on http://localhost:8000..."
cd backend
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "Starting frontend server on http://localhost:8080..."
cd ../frontend
python3 -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "✅ App is running!"
echo "📊 Frontend: http://localhost:8080"
echo "🔌 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
