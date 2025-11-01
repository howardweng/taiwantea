#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAIWANTEA_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$TAIWANTEA_DIR/backend"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/taiwantea_api.pid"

# Log files
API_LOG="$LOG_DIR/api.log"
ERROR_LOG="$LOG_DIR/error.log"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting TAIWANTEA Backend API...${NC}"

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Server is already running (PID: $PID)${NC}"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Use ./taiwantea-server/restart.sh to restart or ./taiwantea-server/stop.sh to stop${NC}"
        exit 1
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Removing stale PID file${NC}"
        rm "$PID_FILE"
    fi
fi

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Backend directory not found: $BACKEND_DIR${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  .env file not found, copying from .env.example${NC}"
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Please configure $BACKEND_DIR/.env with your settings${NC}"
    else
        echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ .env.example not found${NC}"
        exit 1
    fi
fi

# Start uvicorn server
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting uvicorn server on 0.0.0.0:8585...${NC}"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Logs will be written to: $API_LOG${NC}"

cd "$BACKEND_DIR"
nohup uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8585 \
    --reload \
    --log-level info \
    > "$API_LOG" 2> "$ERROR_LOG" &

PID=$!
echo $PID > "$PID_FILE"

# Wait a moment for server to start
sleep 3

# Check if process is still running
if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Server started successfully!${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] PID: $PID${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] API URL: http://localhost:8585${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Health Check: http://localhost:8585/api/health${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] API Documentation: http://localhost:8585/docs${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Log File: $API_LOG${NC}"

    # Test health endpoint
    sleep 2
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Testing health endpoint...${NC}"
    if curl -s http://localhost:8585/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Health check passed!${NC}"
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Server started but health check failed${NC}"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] This is normal if database is not configured yet${NC}"
    fi

    echo ""
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] To stop the server, run: ./taiwantea-server/stop.sh${NC}"
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] To view logs, run: tail -f $API_LOG${NC}"
else
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to start server${NC}"
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Check error log: $ERROR_LOG${NC}"
    rm "$PID_FILE"
    echo ""
    echo "Recent errors:"
    tail -20 "$ERROR_LOG"
    exit 1
fi
