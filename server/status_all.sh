#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_PID_FILE="$SCRIPT_DIR/exam_api.pid"
FRONTEND_DIR="$SCRIPT_DIR/../exam-frontend"
LOG_DIR="$SCRIPT_DIR/logs"

echo "=========================================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Exam System - Full Status${NC}"
echo "=========================================================="
echo ""

# ===========================================
# BACKEND STATUS (Port 8100)
# ===========================================
echo -e "${BLUE}━━━ BACKEND API (Port 8100) ━━━${NC}"

if [ ! -f "$BACKEND_PID_FILE" ]; then
    echo -e "${RED}❌ NOT RUNNING (no PID file)${NC}"
    echo "   To start: ./server/start.sh"
else
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")

    if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ RUNNING${NC}"
        echo "   PID: $BACKEND_PID"

        # Test health endpoint
        if curl -s http://localhost:8100/health | grep -q "healthy"; then
            echo -e "   ${GREEN}✅ Health check passed${NC}"
            echo "   URL: http://localhost:8100"
        else
            echo -e "   ${RED}❌ Health check failed${NC}"
        fi

        # Show resource usage
        echo "   Resource usage:"
        ps -p "$BACKEND_PID" -o %cpu,%mem,etime --no-headers | awk '{printf "   CPU: %s%%  MEM: %s%%  Uptime: %s\n", $1, $2, $3}'
    else
        echo -e "${RED}❌ NOT RUNNING (stale PID)${NC}"
        echo "   To start: ./server/start.sh"
        rm "$BACKEND_PID_FILE"
    fi
fi

echo ""

# ===========================================
# FRONTEND STATUS (Port 3001)
# ===========================================
echo -e "${BLUE}━━━ REACT FRONTEND (Port 3001) ━━━${NC}"

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found${NC}"
    echo "   Expected: $FRONTEND_DIR"
else
    # Check if node process is running on port 3001
    FRONTEND_PIDS=$(lsof -ti:3001 2>/dev/null)

    if [ -z "$FRONTEND_PIDS" ]; then
        echo -e "${RED}❌ NOT RUNNING${NC}"
        echo "   To start: cd exam-frontend && PORT=3001 npm start"
    else
        # Get main PID (first one)
        FRONTEND_PID=$(echo "$FRONTEND_PIDS" | head -1)

        echo -e "${GREEN}✅ RUNNING${NC}"
        echo "   PID: $FRONTEND_PID"

        # Test if React dev server is responding
        if curl -s http://localhost:3001 > /dev/null 2>&1; then
            echo -e "   ${GREEN}✅ Dev server responding${NC}"
            echo "   URL: http://localhost:3001"
        else
            echo -e "   ${YELLOW}⚠️  Port occupied but not responding${NC}"
        fi

        # Show resource usage for main process
        if ps -p "$FRONTEND_PID" > /dev/null 2>&1; then
            echo "   Resource usage:"
            ps -p "$FRONTEND_PID" -o %cpu,%mem,etime --no-headers 2>/dev/null | awk '{printf "   CPU: %s%%  MEM: %s%%  Uptime: %s\n", $1, $2, $3}'
        fi

        # Check for webpack compilation
        if ps aux | grep -v grep | grep -q "webpack.*--mode development"; then
            echo -e "   ${GREEN}✅ Webpack running (hot reload enabled)${NC}"
        fi
    fi
fi

echo ""

# ===========================================
# SUMMARY
# ===========================================
echo -e "${BLUE}━━━ SYSTEM SUMMARY ━━━${NC}"

BACKEND_STATUS="❌"
FRONTEND_STATUS="❌"

# Check backend
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
        BACKEND_STATUS="✅"
    fi
fi

# Check frontend
if lsof -ti:3001 > /dev/null 2>&1; then
    FRONTEND_STATUS="✅"
fi

echo "Backend API:     $BACKEND_STATUS  (port 8100)"
echo "React Frontend:  $FRONTEND_STATUS  (port 3001)"

echo ""

# ===========================================
# AVAILABLE COMMANDS
# ===========================================
echo -e "${BLUE}━━━ AVAILABLE COMMANDS ━━━${NC}"
echo "Backend:"
echo "  ./server/start.sh         - Start backend API"
echo "  ./server/stop.sh          - Stop backend API"
echo "  ./server/restart.sh       - Restart backend API"
echo ""
echo "Frontend:"
echo "  ./server/restart_frontend.sh  - Restart React dev server"
echo "  ./server/stop_frontend.sh     - Stop React dev server"
echo ""
echo "Both Services:"
echo "  ./server/restart_all.sh   - Restart backend + frontend"
echo "  ./server/status_all.sh    - Show this status"
echo ""

# ===========================================
# RECENT LOGS
# ===========================================
if [ "$1" == "-l" ] || [ "$1" == "--logs" ]; then
    echo -e "${BLUE}━━━ RECENT BACKEND LOGS ━━━${NC}"
    if [ -f "$LOG_DIR/api.log" ]; then
        tail -10 "$LOG_DIR/api.log"
    else
        echo "No logs found"
    fi
    echo ""
fi

# Final status message
if [ "$BACKEND_STATUS" == "✅" ] && [ "$FRONTEND_STATUS" == "✅" ]; then
    echo -e "${GREEN}🎉 All systems operational!${NC}"
    exit 0
elif [ "$BACKEND_STATUS" == "✅" ] || [ "$FRONTEND_STATUS" == "✅" ]; then
    echo -e "${YELLOW}⚠️  Partial system running${NC}"
    exit 1
else
    echo -e "${RED}❌ No services running${NC}"
    exit 1
fi
