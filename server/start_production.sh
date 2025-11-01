#!/bin/bash

# Production-ready startup script with multiple workers

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KID_EXAM_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$KID_EXAM_DIR/backend"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/exam_api_prod.pid"

# Log files
API_LOG="$LOG_DIR/api_production.log"
ERROR_LOG="$LOG_DIR/error_production.log"

# Create log directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] Starting Exam API (PRODUCTION MODE)...${NC}"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Server already running (PID: $PID)${NC}"
        exit 1
    fi
fi

cd "$BACKEND_DIR"

# Production configuration:
# - Multiple workers based on CPU cores
# - No reload (stable)
# - Access log enabled
# - Timeout for long image generation
WORKERS=$(( $(nproc) * 2 + 1 ))  # Formula: (2 x CPU cores) + 1

echo -e "${BLUE}Starting with $WORKERS workers...${NC}"

nohup uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8100 \
    --workers $WORKERS \
    --log-level warning \
    --access-log \
    --timeout-keep-alive 300 \
    > "$API_LOG" 2> "$ERROR_LOG" &

PID=$!
echo $PID > "$PID_FILE"

sleep 3

if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Production server started!${NC}"
    echo -e "${GREEN}   PID: $PID${NC}"
    echo -e "${GREEN}   Workers: $WORKERS${NC}"
    echo -e "${GREEN}   API: http://0.0.0.0:8100${NC}"
    echo -e "${YELLOW}   Note: --reload disabled for stability${NC}"
else
    echo -e "${RED}❌ Failed to start${NC}"
    cat "$ERROR_LOG"
    exit 1
fi
