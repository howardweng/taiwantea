#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting TAIWANTEA (All Services)${NC}"
echo "============================================================"
echo ""

# Start backend
echo -e "${BLUE}━━━ STARTING BACKEND API ━━━${NC}"
if [ -f "$SCRIPT_DIR/start.sh" ]; then
    "$SCRIPT_DIR/start.sh"
    BACKEND_EXIT=$?
else
    echo -e "${RED}❌ Backend start script not found${NC}"
    BACKEND_EXIT=1
fi

echo ""
echo ""

# Start frontend
echo -e "${BLUE}━━━ STARTING REACT FRONTEND ━━━${NC}"
if [ -f "$SCRIPT_DIR/start_frontend.sh" ]; then
    "$SCRIPT_DIR/start_frontend.sh"
    FRONTEND_EXIT=$?
else
    echo -e "${RED}❌ Frontend start script not found${NC}"
    FRONTEND_EXIT=1
fi

echo ""
echo "============================================================"

# Summary
if [ $BACKEND_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${GREEN}🎉 All services started successfully!${NC}"
    echo ""
    echo "Backend API:    http://localhost:8585"
    echo "API Docs:       http://localhost:8585/docs"
    echo "React Frontend: http://localhost:5173"
    echo "Admin Login:    http://localhost:5173/admin/login"
    echo ""
    echo "Default admin credentials:"
    echo "  Email:    admin@taiwantea.com"
    echo "  Password: Admin123!"
    echo ""
    echo "Commands:"
    echo "  Status:  ./taiwantea-server/status_all.sh"
    echo "  Stop:    ./taiwantea-server/stop_all.sh"
    echo "  Restart: ./taiwantea-server/restart_all.sh"
    exit 0
elif [ $BACKEND_EXIT -eq 0 ] || [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Partial startup successful${NC}"
    if [ $BACKEND_EXIT -ne 0 ]; then
        echo -e "${RED}   Backend: FAILED${NC}"
    else
        echo -e "${GREEN}   Backend: OK (http://localhost:8585)${NC}"
    fi
    if [ $FRONTEND_EXIT -ne 0 ]; then
        echo -e "${RED}   Frontend: FAILED${NC}"
    else
        echo -e "${GREEN}   Frontend: OK (http://localhost:5173)${NC}"
    fi
    exit 1
else
    echo -e "${RED}❌ All services failed to start${NC}"
    exit 1
fi
