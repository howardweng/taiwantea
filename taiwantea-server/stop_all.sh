#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping TAIWANTEA (All Services)${NC}"
echo "============================================================"
echo ""

# Stop frontend first
echo -e "${BLUE}━━━ STOPPING FRONTEND ━━━${NC}"
if [ -f "$SCRIPT_DIR/stop_frontend.sh" ]; then
    "$SCRIPT_DIR/stop_frontend.sh"
    FRONTEND_EXIT=$?
else
    echo -e "${YELLOW}⚠️  Frontend stop script not found${NC}"
    FRONTEND_EXIT=1
fi

echo ""

# Stop backend
echo -e "${BLUE}━━━ STOPPING BACKEND API ━━━${NC}"
if [ -f "$SCRIPT_DIR/stop.sh" ]; then
    "$SCRIPT_DIR/stop.sh"
    BACKEND_EXIT=$?
else
    echo -e "${YELLOW}⚠️  Backend stop script not found${NC}"
    BACKEND_EXIT=1
fi

echo ""
echo "============================================================"

# Summary
if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${GREEN}✅ All services stopped successfully!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some services may not have stopped properly${NC}"
    exit 1
fi
