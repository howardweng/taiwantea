#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Restarting TAIWANTEA Frontend${NC}"
echo "=========================================="

# Stop the frontend
echo -e "${BLUE}━━━ STOPPING FRONTEND ━━━${NC}"
if [ -f "$SCRIPT_DIR/stop_frontend.sh" ]; then
    "$SCRIPT_DIR/stop_frontend.sh"
else
    echo -e "${YELLOW}⚠️  Stop script not found, attempting direct stop...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null
fi

echo ""
sleep 2

# Start the frontend
echo -e "${BLUE}━━━ STARTING FRONTEND ━━━${NC}"
if [ -f "$SCRIPT_DIR/start_frontend.sh" ]; then
    "$SCRIPT_DIR/start_frontend.sh"
    EXIT_CODE=$?
else
    echo -e "${RED}❌ Start script not found${NC}"
    exit 1
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Frontend restarted successfully!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Failed to restart frontend${NC}"
    exit 1
fi
