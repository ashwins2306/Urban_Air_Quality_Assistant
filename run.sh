#!/usr/bin/env bash
# BreatheEasy - Start both Backend and Frontend

echo "🌬️ Starting BreatheEasy..."

# Start Backend
echo "Starting Python FastAPI backend on http://localhost:8000..."
cd "$(dirname "$0")/backend"
python3 main.py &
BACKEND_PID=$!

# Start Frontend
echo "Starting React Vite frontend on http://localhost:3000..."
cd "../frontend"
npm run dev -- --host &
FRONTEND_PID=$!

echo "Both servers launched! Press Ctrl+C to terminate."

cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID 2>/dev/null
  kill $FRONTEND_PID 2>/dev/null
  exit 0
}

trap cleanup INT TERM
wait
