#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/../exam-frontend"

echo "=========================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Restarting React Frontend${NC}"
echo "=========================================="

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    exit 1
fi

# Kill any process on port 3001
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping React dev server...${NC}"
PIDS=$(lsof -ti:3001 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] No process found on port 3001${NC}"
else
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Killing processes: $PIDS${NC}"
    lsof -ti:3001 | xargs kill -9 2>/dev/null
    sleep 2

    # Verify stopped
    if lsof -ti:3001 > /dev/null 2>&1; then
        echo -e "${RED}❌ Failed to stop frontend${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Frontend stopped${NC}"
    fi
fi

# Start frontend
echo ""
echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] Starting React dev server...${NC}"
echo "Directory: $FRONTEND_DIR"
echo "Port: 3001"
echo ""

cd "$FRONTEND_DIR" || exit 1

# Start in background
PORT=3001 npm start > /dev/null 2>&1 &
FRONTEND_PID=$!

echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Waiting for React dev server to start...${NC}"

# Wait up to 30 seconds for server to start
for i in {1..30}; do
    sleep 1
    if curl -s http://localhost:3001 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ React dev server started successfully!${NC}"
        echo "   PID: $FRONTEND_PID"
        echo "   URL: http://localhost:3001"
        echo ""
        echo "Frontend restarted successfully!"
        exit 0
    fi
    echo -n "."
done

echo ""
echo -e "${RED}❌ Frontend failed to start within 30 seconds${NC}"
echo "Check logs for errors"
exit 1
