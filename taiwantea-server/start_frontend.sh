#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAIWANTEA_DIR="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$TAIWANTEA_DIR/frontend"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/taiwantea_frontend.pid"

# Log files
FRONTEND_LOG="$LOG_DIR/frontend.log"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting TAIWANTEA Frontend (Vite)...${NC}"

# Check if frontend is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Frontend is already running (PID: $PID)${NC}"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Use ./taiwantea-server/restart_frontend.sh to restart${NC}"
        exit 1
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Removing stale PID file${NC}"
        rm "$PID_FILE"
    fi
fi

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$FRONTEND_DIR/.env" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  .env file not found, copying from .env.example${NC}"
    if [ -f "$FRONTEND_DIR/.env.example" ]; then
        cp "$FRONTEND_DIR/.env.example" "$FRONTEND_DIR/.env"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Created .env file${NC}"
    fi
fi

# Check if node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  node_modules not found, installing dependencies...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Check if port 5173 is already in use
if lsof -ti:5173 > /dev/null 2>&1; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Port 5173 is already in use${NC}"
    echo "Processes on port 5173:"
    lsof -ti:5173 | xargs ps -p
    exit 1
fi

# Start Vite dev server
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting Vite dev server on port 5173...${NC}"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Logs will be written to: $FRONTEND_LOG${NC}"

cd "$FRONTEND_DIR"
nohup npm run dev > "$FRONTEND_LOG" 2>&1 &

PID=$!
echo $PID > "$PID_FILE"

echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Waiting for Vite dev server to start...${NC}"

# Wait up to 30 seconds for server to start
for i in {1..30}; do
    sleep 1
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Vite dev server started successfully!${NC}"
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] PID: $PID${NC}"
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Frontend URL: http://localhost:5173${NC}"
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Admin Login: http://localhost:5173/admin/login${NC}"
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Log File: $FRONTEND_LOG${NC}"
        echo ""
        echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] To stop the frontend, run: ./taiwantea-server/stop_frontend.sh${NC}"
        echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] To view logs, run: tail -f $FRONTEND_LOG${NC}"
        exit 0
    fi
    echo -n "."
done

echo ""
echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Frontend failed to start within 30 seconds${NC}"
echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Check log file: $FRONTEND_LOG${NC}"

# Check if process is still running
if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Process is still running, killing it...${NC}"
    kill "$PID"
fi

rm "$PID_FILE"
echo ""
echo "Recent errors:"
tail -20 "$FRONTEND_LOG"
exit 1
