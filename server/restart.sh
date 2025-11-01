#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/exam_api.pid"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Restarting Exam Image Generator API...${NC}"

# Check if server is running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Server is running (PID: $PID) - stopping first...${NC}"
        "$SCRIPT_DIR/stop.sh"
        if [ $? -ne 0 ]; then
            echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to stop server${NC}"
            exit 1
        fi
        sleep 1
    fi
fi

# Start server
echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting server...${NC}"
"$SCRIPT_DIR/start.sh"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Restart completed!${NC}"
else
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Restart failed${NC}"
    exit 1
fi
