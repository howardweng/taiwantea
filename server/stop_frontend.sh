#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Stopping React Frontend${NC}"
echo "=========================================="

# Find processes on port 3001
PIDS=$(lsof -ti:3001 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] No React dev server running on port 3001${NC}"
    exit 0
fi

echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Found processes on port 3001: $PIDS${NC}"

# Try graceful shutdown first
echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Attempting graceful shutdown...${NC}"
lsof -ti:3001 | xargs kill 2>/dev/null
sleep 2

# Check if still running
if lsof -ti:3001 > /dev/null 2>&1; then
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Graceful shutdown failed, forcing...${NC}"
    lsof -ti:3001 | xargs kill -9 2>/dev/null
    sleep 1
fi

# Verify stopped
if lsof -ti:3001 > /dev/null 2>&1; then
    echo -e "${RED}❌ Failed to stop React dev server${NC}"
    exit 1
else
    echo -e "${GREEN}✅ React dev server stopped successfully${NC}"
    exit 0
fi
