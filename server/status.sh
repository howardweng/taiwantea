#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/exam_api.pid"
LOG_DIR="$SCRIPT_DIR/logs"
API_LOG="$LOG_DIR/api.log"

echo "==================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Exam Image Generator API - Status${NC}"
echo "==================================="

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Status: ❌ NOT RUNNING (no PID file)${NC}"
    echo ""
    echo "To start the server, run: ./server/start.sh"
    exit 1
fi

PID=$(cat "$PID_FILE")

# Check if process is running
if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Status: ✅ RUNNING${NC}"
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] PID: $PID${NC}"
    echo ""

    # Get process info
    echo "Process Info:"
    ps -p "$PID" -o pid,ppid,%cpu,%mem,etime,cmd
    echo ""

    # Test health endpoint
    echo "Health Check:"
    if curl -s http://localhost:8100/health | grep -q "healthy"; then
        echo -e "${GREEN}✅ API is responding (http://localhost:8100/health)${NC}"
    else
        echo -e "${RED}❌ API is not responding${NC}"
    fi
    echo ""

    # Show API endpoints
    echo "API Endpoints:"
    echo "  Root:        http://localhost:8100/"
    echo "  Health:      http://localhost:8100/health"
    echo "  Docs:        http://localhost:8100/docs"
    echo "  Generate:    POST http://localhost:8100/api/exam-images/generate-all"
    echo "  Status:      GET http://localhost:8100/api/exam-images/status/{job_id}"
    echo "  List:        GET http://localhost:8100/api/exam-images/list"
    echo ""

    # Show recent log entries
    if [ -f "$API_LOG" ]; then
        echo "Recent Log Entries (last 5 lines):"
        echo "-----------------------------------"
        tail -5 "$API_LOG"
    fi
else
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] Status: ❌ NOT RUNNING (stale PID file)${NC}"
    echo ""
    echo "To start the server, run: ./server/start.sh"
    rm "$PID_FILE"
    exit 1
fi

echo ""
echo "Available Commands:"
echo "  ./server/start.sh   - Start the API server"
echo "  ./server/stop.sh    - Stop the API server"
echo "  ./server/restart.sh - Restart the API server"
echo "  ./server/status.sh  - Show this status"
