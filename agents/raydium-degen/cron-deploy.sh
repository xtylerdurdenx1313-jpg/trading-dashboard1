#!/bin/bash

# Raydium Degen Agent - Cron Deployment Script
# Runs: Every 5 minutes, 9 AM - 8 PM EST

AGENT_DIR="/Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen"
LOG_DIR="$AGENT_DIR/logs"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Run the trading cycle
cd "$AGENT_DIR"
python3 execute_cycle.py >> "$LOG_DIR/cycle.log" 2>&1

# Log execution
echo "[$TIMESTAMP] Cycle executed" >> "$LOG_DIR/executions.log"
