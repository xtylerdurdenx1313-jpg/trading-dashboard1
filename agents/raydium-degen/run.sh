#!/bin/bash
# Raydium Degen Trading Agent — Launch Script

set -e

AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AGENT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function: print colored output
log() {
    local level=$1
    shift
    case $level in
        info)  echo -e "${BLUE}[INFO]${NC} $*" ;;
        success) echo -e "${GREEN}[✓]${NC} $*" ;;
        warn)  echo -e "${YELLOW}[WARN]${NC} $*" ;;
        error) echo -e "${RED}[ERROR]${NC} $*" ;;
    esac
}

# Function: check prerequisites
check_prerequisites() {
    log info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log error "Python3 not found. Please install Python 3.8+"
        exit 1
    fi
    log success "Python3 found: $(python3 --version)"
    
    # Check if .env exists
    if [ ! -f .env ]; then
        log warn ".env not found. Creating from template..."
        if [ -f .env.template ]; then
            cp .env.template .env
            log success "Created .env from template. Please edit with your API keys."
            log info "Run: nano .env"
            return 1
        else
            log error ".env.template not found"
            exit 1
        fi
    fi
    log success ".env file exists"
    
    # Check logs directory
    if [ ! -d logs ]; then
        mkdir -p logs
        log success "Created logs directory"
    fi
}

# Function: run one execution cycle
run_cycle() {
    log info "Starting execution cycle..."
    python3 execute_cycle.py
    if [ $? -eq 0 ]; then
        log success "Cycle completed"
    else
        log error "Cycle failed"
        exit 1
    fi
}

# Function: show status
show_status() {
    log info "Agent Status"
    echo "────────────────────────────────────────"
    
    if [ -f STATE.json ]; then
        log info "Account State:"
        python3 -c "
import json
with open('STATE.json') as f:
    state = json.load(f)
    acc = state['account']
    trd = state['trading']
    daily = state['daily_metrics']
    print(f\"  Equity: \${acc['current_equity']:.2f}\")
    print(f\"  Total P&L: \${acc['total_pnl']:.2f} ({acc['total_pnl_pct']:+.1f}%)\")
    print(f\"  Win Rate: {trd['win_rate']:.1f}% ({trd['trades_won']}/{trd['trades_total']})\")
    print(f\"  Daily P&L: \${daily['daily_pnl']:.2f}\")
    print(f\"  Open Positions: {state['positions']['open_position_count']}\")
    print(f\"  Cooldown Active: {daily['cooldown_active']}\")
" 2>/dev/null || log warn "Could not parse STATE.json"
    else
        log warn "STATE.json not found (agent not initialized)"
    fi
    
    if [ -f logs/execution.log ]; then
        log info "Recent Log:"
        tail -3 logs/execution.log | sed 's/^/  /'
    fi
}

# Function: show help
show_help() {
    cat << EOF
${BLUE}Raydium Degen Trading Agent${NC}

Usage: $0 [COMMAND]

Commands:
  run         Run one execution cycle (default)
  status      Show current account status
  logs        Tail the execution log (live)
  edit-env    Edit .env configuration
  edit-strat  Edit STRATEGY.md
  test        Test Python environment
  help        Show this help message

Environment:
  Set .env with your API keys before first run.

Examples:
  $0 run              # Execute one cycle
  $0 status           # Check account status
  $0 logs             # View live logs
  
For production, use cron:
  */5 9-20 * * * cd $AGENT_DIR && ./run.sh run >> logs/cron.log 2>&1

EOF
}

# Main logic
main() {
    local cmd=${1:-run}
    
    case $cmd in
        run)
            check_prerequisites && run_cycle
            ;;
        status)
            show_status
            ;;
        logs)
            if [ -f logs/execution.log ]; then
                tail -f logs/execution.log
            else
                log error "No logs found"
                exit 1
            fi
            ;;
        edit-env)
            nano .env
            ;;
        edit-strat)
            nano STRATEGY.md
            ;;
        test)
            log info "Testing Python environment..."
            python3 << 'PYEOF'
import sys
import json
print(f"Python: {sys.version}")
print(f"JSON support: OK")
try:
    import requests
    print(f"Requests: OK")
except ImportError:
    print("Requests: NOT INSTALLED (optional, used for API calls)")
PYEOF
            log success "Python environment OK"
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            log error "Unknown command: $cmd"
            show_help
            exit 1
            ;;
    esac
}

# Run main
main "$@"
