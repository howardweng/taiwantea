#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Restarting TAIWANTEA Backend API${NC}"
echo "=========================================="

# Stop the server
echo -e "${BLUE}━━━ STOPPING SERVER ━━━${NC}"
if [ -f "$SCRIPT_DIR/stop.sh" ]; then
    "$SCRIPT_DIR/stop.sh"
else
    echo -e "${YELLOW}⚠️  Stop script not found, attempting direct stop...${NC}"
    PID_FILE="$SCRIPT_DIR/taiwantea_api.pid"
    if [ -f "$PID_FILE" ]; then
        kill $(cat "$PID_FILE") 2>/dev/null
        rm "$PID_FILE"
    fi
fi

echo ""
sleep 2

# Start the server
echo -e "${BLUE}━━━ STARTING SERVER ━━━${NC}"
if [ -f "$SCRIPT_DIR/start.sh" ]; then
    "$SCRIPT_DIR/start.sh"
    EXIT_CODE=$?
else
    echo -e "${RED}❌ Start script not found${NC}"
    exit 1
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Backend API restarted successfully!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Failed to restart backend API${NC}"
    exit 1
fi
