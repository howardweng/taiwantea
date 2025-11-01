#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Restarting TAIWANTEA (All Services)${NC}"
echo "============================================================"
echo ""

# Restart backend
echo -e "${BLUE}━━━ RESTARTING BACKEND API ━━━${NC}"
if [ -f "$SCRIPT_DIR/restart.sh" ]; then
    "$SCRIPT_DIR/restart.sh"
    BACKEND_EXIT=$?
else
    echo -e "${RED}❌ Backend restart script not found${NC}"
    BACKEND_EXIT=1
fi

echo ""
echo ""

# Restart frontend
echo -e "${BLUE}━━━ RESTARTING REACT FRONTEND ━━━${NC}"
if [ -f "$SCRIPT_DIR/restart_frontend.sh" ]; then
    "$SCRIPT_DIR/restart_frontend.sh"
    FRONTEND_EXIT=$?
else
    echo -e "${RED}❌ Frontend restart script not found${NC}"
    FRONTEND_EXIT=1
fi

echo ""
echo "============================================================"

# Summary
if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${GREEN}🎉 All services restarted successfully!${NC}"
    echo ""
    echo "Backend API:    http://localhost:8585"
    echo "React Frontend: http://localhost:5173"
    echo ""
    echo "Check status: ./taiwantea-server/status_all.sh"
    exit 0
elif [ $BACKEND_EXIT -eq 0 ] || [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Partial restart successful${NC}"
    if [ $BACKEND_EXIT -ne 0 ]; then
        echo -e "${RED}   Backend: FAILED${NC}"
    else
        echo -e "${GREEN}   Backend: OK${NC}"
    fi
    if [ $FRONTEND_EXIT -ne 0 ]; then
        echo -e "${RED}   Frontend: FAILED${NC}"
    else
        echo -e "${GREEN}   Frontend: OK${NC}"
    fi
    exit 1
else
    echo -e "${RED}❌ All services failed to restart${NC}"
    exit 1
fi
