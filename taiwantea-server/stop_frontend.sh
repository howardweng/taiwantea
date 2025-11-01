#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/taiwantea_frontend.pid"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping TAIWANTEA Frontend...${NC}"

# Try to stop using PID file first
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping frontend process $PID...${NC}"
        kill "$PID"

        # Wait for process to stop (max 10 seconds)
        for i in {1..10}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Frontend stopped successfully${NC}"
                rm "$PID_FILE"
                break
            fi
            echo -n "."
            sleep 1
        done

        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
            echo ""
            echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Forcing shutdown...${NC}"
            kill -9 "$PID"
            sleep 1
        fi
    else
        echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Process $PID not found${NC}"
        rm "$PID_FILE"
    fi
fi

# Also kill any process on port 5173
PIDS=$(lsof -ti:5173 2>/dev/null)

if [ -n "$PIDS" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Killing processes on port 5173: $PIDS${NC}"
    echo "$PIDS" | xargs kill -9 2>/dev/null
    sleep 2

    # Verify stopped
    if lsof -ti:5173 > /dev/null 2>&1; then
        echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to stop frontend${NC}"
        exit 1
    else
        echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Frontend stopped${NC}"
    fi
else
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] No process found on port 5173${NC}"
fi

exit 0
