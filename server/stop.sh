#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/exam_api.pid"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping Exam Image Generator API...${NC}"

if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ PID file not found. Server may not be running.${NC}"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Process $PID not found. Server may have already stopped.${NC}"
    rm "$PID_FILE"
    exit 1
fi

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping server process $PID...${NC}"

# Try graceful shutdown first
kill "$PID"

# Wait for process to stop (max 10 seconds)
for i in {1..10}; do
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Server stopped successfully${NC}"
        rm "$PID_FILE"
        exit 0
    fi
    echo -n "."
    sleep 1
done

echo ""
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Graceful shutdown timed out, forcing shutdown...${NC}"
kill -9 "$PID"

sleep 1

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Server stopped forcefully${NC}"
    rm "$PID_FILE"
    exit 0
else
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to stop server${NC}"
    exit 1
fi
