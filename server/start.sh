#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KID_EXAM_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$KID_EXAM_DIR/backend"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/exam_api.pid"

# Log files
API_LOG="$LOG_DIR/api.log"
ERROR_LOG="$LOG_DIR/error.log"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting Exam Image Generator API...${NC}"

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Server is already running (PID: $PID)${NC}"
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Use ./server/restart.sh to restart or ./server/stop.sh to stop${NC}"
        exit 1
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Removing stale PID file${NC}"
        rm "$PID_FILE"
    fi
fi

# Start uvicorn server
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting uvicorn server on 0.0.0.0:8100...${NC}"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Logs will be written to: $API_LOG${NC}"

cd "$BACKEND_DIR"
nohup uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8100 \
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
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] API URL: http://0.0.0.0:8100${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Health Check: http://0.0.0.0:8100/health${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] API Documentation: http://0.0.0.0:8100/docs${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Log File: $API_LOG${NC}"

    # Test health endpoint
    sleep 2
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Testing health endpoint...${NC}"
    if curl -s http://localhost:8100/health | grep -q "healthy"; then
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Health check passed!${NC}"
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Server started but health check failed${NC}"
    fi

    echo ""
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] To stop the server, run: ./server/stop.sh${NC}"
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
