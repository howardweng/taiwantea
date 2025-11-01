#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_PID_FILE="$SCRIPT_DIR/taiwantea_api.pid"
FRONTEND_PID_FILE="$SCRIPT_DIR/taiwantea_frontend.pid"

echo "================================================================"
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] TAIWANTEA System Status${NC}"
echo "================================================================"
echo ""

# Backend Status
echo -e "${BLUE}━━━ BACKEND API STATUS ━━━${NC}"
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
        echo -e "${GREEN}Status: ✅ RUNNING (PID: $BACKEND_PID)${NC}"

        # Test health endpoint
        if curl -s http://localhost:8585/api/health > /dev/null 2>&1; then
            echo -e "${GREEN}Health: ✅ API is responding${NC}"
        else
            echo -e "${YELLOW}Health: ⚠️  API not responding${NC}"
        fi

        echo "URL:    http://localhost:8585"
        echo "Docs:   http://localhost:8585/docs"
    else
        echo -e "${RED}Status: ❌ NOT RUNNING (stale PID)${NC}"
        rm "$BACKEND_PID_FILE"
    fi
else
    echo -e "${RED}Status: ❌ NOT RUNNING${NC}"
fi

echo ""

# Frontend Status
echo -e "${BLUE}━━━ FRONTEND STATUS ━━━${NC}"
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
        echo -e "${GREEN}Status: ✅ RUNNING (PID: $FRONTEND_PID)${NC}"

        # Test frontend endpoint
        if curl -s http://localhost:5173 > /dev/null 2>&1; then
            echo -e "${GREEN}Health: ✅ Frontend is responding${NC}"
        else
            echo -e "${YELLOW}Health: ⚠️  Frontend not responding${NC}"
        fi

        echo "URL:    http://localhost:5173"
        echo "Admin:  http://localhost:5173/admin/login"
    else
        echo -e "${RED}Status: ❌ NOT RUNNING (stale PID)${NC}"
        rm "$FRONTEND_PID_FILE"
    fi
else
    echo -e "${RED}Status: ❌ NOT RUNNING${NC}"
fi

echo ""
echo "================================================================"
echo ""

# Show available commands
echo "Available Commands:"
echo "  ./taiwantea-server/start_all.sh     - Start all services"
echo "  ./taiwantea-server/stop_all.sh      - Stop all services"
echo "  ./taiwantea-server/restart_all.sh   - Restart all services"
echo "  ./taiwantea-server/status_all.sh    - Show this status"
echo ""
echo "Individual Service Commands:"
echo "  Backend:  ./taiwantea-server/start.sh | stop.sh | restart.sh | status.sh"
echo "  Frontend: ./taiwantea-server/start_frontend.sh | stop_frontend.sh | restart_frontend.sh"
echo ""

# Check if both are running and show success message
BACKEND_RUNNING=false
FRONTEND_RUNNING=false

if [ -f "$BACKEND_PID_FILE" ] && ps -p "$(cat "$BACKEND_PID_FILE")" > /dev/null 2>&1; then
    BACKEND_RUNNING=true
fi

if [ -f "$FRONTEND_PID_FILE" ] && ps -p "$(cat "$FRONTEND_PID_FILE")" > /dev/null 2>&1; then
    FRONTEND_RUNNING=true
fi

if $BACKEND_RUNNING && $FRONTEND_RUNNING; then
    echo -e "${GREEN}🎉 All systems operational!${NC}"
    exit 0
elif $BACKEND_RUNNING || $FRONTEND_RUNNING; then
    echo -e "${YELLOW}⚠️  Some services are not running${NC}"
    exit 1
else
    echo -e "${RED}❌ All services are stopped${NC}"
    echo ""
    echo "To start all services, run: ./taiwantea-server/start_all.sh"
    exit 1
fi
