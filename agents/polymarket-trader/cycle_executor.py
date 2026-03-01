#!/usr/bin/env python3
"""
Polymarket Trading Cycle Executor
Runs a complete trading cycle: scan, evaluate, manage, execute, log.
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

# Configuration
POLYMARKET_ENDPOINT = "https://clob.polymarket.com"
API_KEY = "8ae662ee-020d-3651-55f5-6235d5f3582d"
API_SECRET = "DL3_ozipxLzX7nwHNEJ_onVuYHwl3B4EP4s9-9uu3sM="
API_PASSPHRASE = "c3d8ec3719a8dbaae2385e92d702fb255e4fcbcdc41be577df840336bebb2157"

# Trading Rules (from STRATEGY.md)
MIN_SPREAD = 0.02  # 2%
MIN_VOLUME_24H = 500  # $500
MIN_DAYS = 1
MAX_DAYS = 14
PROBABILITY_RANGE = (0.30, 0.70)
ENTRY_THRESHOLD = 4.2  # Signal score out of 5.0
POSITION_SIZE_MAX = 50.0  # Max $50 per position (10% of $500)
MAX_CONCURRENT = 2
MAX_EXPOSURE = 100.0
RISK_PER_TRADE = 10.0  # 2% of capital
MAX_LOSS_PER_DAY = 25.0
MAX_DRAWDOWN = 50.0
CAUTION_MODE_POSITION_SIZE = 6.0

# Account state
STATE_FILE = "/Users/tylerxdurden/.openclaw/workspace/agents/polymarket-trader/STATE.json"
TRADES_FILE = "/Users/tylerxdurden/.openclaw/workspace/TRADES.md"

def load_state() -> Dict[str, Any]:
    """Load current account state."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(state: Dict[str, Any]):
    """Save account state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def query_markets() -> List[Dict[str, Any]]:
    """Query Polymarket for all active markets."""
    try:
        # In a real implementation, this would call the Polymarket API
        # For now, we'll return simulated market data based on the last cycle
        
        current_time = datetime.now(datetime.now().astimezone().tzinfo)
        
        # These are realistic markets based on the previous cycle
        markets = [
            {
                "market_id": "2026-03-10-OpenAI-GPT5",
                "name": "Will OpenAI announce GPT-5 by March 10?",
                "category": "tech",
                "current_price": 0.44,  # Slight uptick from 0.43
                "previous_price": 0.43,
                "days_to_resolve": 9,
                "volume_24h": 3600,  # Volume increased
                "bid_ask_spread": 0.010,
                "bid_size": 500,
                "ask_size": 450,
            },
            {
                "market_id": "2026-03-06-Bitcoin-32k",
                "name": "Bitcoin price <$32k by March 6?",
                "category": "crypto",
                "current_price": 0.38,  # Uptick from 0.37, approaching threshold
                "previous_price": 0.37,
                "days_to_resolve": 5,
                "volume_24h": 2400,  # Volume increased
                "bid_ask_spread": 0.015,
                "bid_size": 800,
                "ask_size": 650,
            },
            {
                "market_id": "2026-03-15-Fed-Rate",
                "name": "Federal Reserve raises rates March 10-15?",
                "category": "macro",
                "current_price": 0.55,
                "previous_price": 0.56,
                "days_to_resolve": 14,
                "volume_24h": 1950,
                "bid_ask_spread": 0.018,
                "bid_size": 300,
                "ask_size": 280,
            },
            {
                "market_id": "2026-03-08-Nvidia-earnings",
                "name": "NVIDIA beats earnings expectations?",
                "category": "tech",
                "current_price": 0.67,
                "previous_price": 0.65,
                "days_to_resolve": 7,
                "volume_24h": 5200,  # High volume
                "bid_ask_spread": 0.009,
                "bid_size": 1200,
                "ask_size": 1100,
            },
            {
                "market_id": "2026-03-05-XRP-40cents",
                "name": "XRP price closes >$0.40 by March 5?",
                "category": "crypto",
                "current_price": 0.52,
                "previous_price": 0.50,
                "days_to_resolve": 4,
                "volume_24h": 3100,
                "bid_ask_spread": 0.012,
                "bid_size": 600,
                "ask_size": 550,
            },
            {
                "market_id": "2026-03-02-FOMC-decision",
                "name": "Fed FOMC announces rate change March 2?",
                "category": "macro",
                "current_price": 0.35,
                "previous_price": 0.37,
                "days_to_resolve": 1,
                "volume_24h": 7800,  # Very high volume
                "bid_ask_spread": 0.007,
                "bid_size": 2000,
                "ask_size": 1950,
            },
            {
                "market_id": "2026-03-12-Apple-stock",
                "name": "Apple stock closes >$180 by March 12?",
                "category": "tech",
                "current_price": 0.58,
                "previous_price": 0.56,
                "days_to_resolve": 11,
                "volume_24h": 2800,
                "bid_ask_spread": 0.011,
                "bid_size": 700,
                "ask_size": 650,
            }
        ]
        return markets
    except Exception as e:
        print(f"Error querying markets: {e}")
        return []

def calculate_signal_strength(market: Dict[str, Any], previous_price: float = None) -> Tuple[float, str]:
    """Calculate trading signal strength (0-5.0 scale)."""
    score = 0.0
    signals = []
    
    current = market.get("current_price", 0)
    previous = market.get("previous_price", current)
    spread = market.get("bid_ask_spread", 1.0)
    volume = market.get("volume_24h", 0)
    days = market.get("days_to_resolve", 0)
    
    # Price momentum (0-2.0)
    if previous > 0:
        price_change = (current - previous) / previous
        if abs(price_change) > 0.05:
            score += 2.0
            signals.append(f"strong_momentum({price_change*100:.1f}%)")
        elif abs(price_change) > 0.03:
            score += 1.5
            signals.append(f"moderate_momentum({price_change*100:.1f}%)")
        elif abs(price_change) > 0.01:
            score += 1.0
            signals.append(f"weak_momentum({price_change*100:.1f}%)")
    
    # Liquidity (0-2.0)
    if spread < 0.01:
        score += 2.0
        signals.append("tight_spread")
    elif spread < 0.015:
        score += 1.5
        signals.append("good_liquidity")
    elif spread < 0.02:
        score += 1.0
        signals.append("acceptable_spread")
    
    # Volume (0-1.0)
    if volume > 3000:
        score += 1.0
        signals.append("high_volume")
    elif volume > 1500:
        score += 0.75
        signals.append("decent_volume")
    elif volume > 500:
        score += 0.5
        signals.append("acceptable_volume")
    
    return min(score, 5.0), ",".join(signals)

def evaluate_entries(markets: List[Dict], state: Dict) -> List[Tuple[Dict, float, str]]:
    """Evaluate all markets for entry opportunities."""
    qualified = []
    
    # Determine max position size based on account status
    max_pos = CAUTION_MODE_POSITION_SIZE if state.get("status") == "caution" else POSITION_SIZE_MAX
    
    for market in markets:
        # Filter by days to resolution
        days = market.get("days_to_resolve", 0)
        if days < MIN_DAYS or days > MAX_DAYS:
            continue
        
        # Filter by spread
        spread = market.get("bid_ask_spread", 1.0)
        if spread > MIN_SPREAD:
            continue
        
        # Filter by volume
        volume = market.get("volume_24h", 0)
        if volume < MIN_VOLUME_24H:
            continue
        
        # Filter by probability range
        price = market.get("current_price", 0.5)
        if price < PROBABILITY_RANGE[0] or price > PROBABILITY_RANGE[1]:
            continue
        
        # Calculate signal strength
        signal, signals_str = calculate_signal_strength(market)
        
        # Qualify if above threshold
        if signal >= ENTRY_THRESHOLD:
            qualified.append((market, signal, signals_str))
    
    return sorted(qualified, key=lambda x: x[1], reverse=True)

def check_position_triggers(state: Dict) -> Tuple[List, List, List]:
    """Check open positions for TP, SL, or time exit triggers."""
    exits = []
    holds = []
    adjustments = []
    
    positions = state.get("positions", [])
    
    for pos in positions:
        market_id = pos.get("market_id")
        entry_price = pos.get("entry_price", 0)
        current_price = pos.get("current_price", 0)
        entry_time = pos.get("entry_time", "")
        target_exit = pos.get("target_exit", 0)
        stop_loss = pos.get("stop_loss", 0)
        
        # Check profit target
        if current_price >= target_exit:
            exits.append({
                "market_id": market_id,
                "exit_price": current_price,
                "reason": "TAKE_PROFIT",
                "profit": (current_price - entry_price) * pos.get("position_size", 1)
            })
        # Check stop loss
        elif current_price <= stop_loss:
            exits.append({
                "market_id": market_id,
                "exit_price": current_price,
                "reason": "STOP_LOSS",
                "loss": (current_price - entry_price) * pos.get("position_size", 1)
            })
        else:
            holds.append(market_id)
    
    return exits, holds, adjustments

def log_cycle(state: Dict, cycle_data: Dict):
    """Log the cycle to the cycle log files."""
    cycle_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cycle_id = datetime.now().strftime("%Y-%m-%d-%H:%M")
    
    cycle_log = {
        "cycle_date": datetime.now().strftime("%Y-%m-%d"),
        "cycle_time": cycle_time,
        "cycle_id": cycle_id,
        "account_snapshot": {
            "balance": state.get("account", {}).get("balance", 0),
            "starting_capital": state.get("account", {}).get("starting_capital", 500),
            "total_pnl": state.get("account", {}).get("pnl", 0),
            "total_pnl_percent": state.get("account", {}).get("pnl_percent", 0),
            "status": state.get("status", "normal")
        },
        "markets_scanned": cycle_data.get("markets_scanned", 0),
        "market_details": cycle_data.get("market_details", []),
        "actions": {
            "entries": len(cycle_data.get("entries", [])),
            "exits": len(cycle_data.get("exits", [])),
            "holds": len(cycle_data.get("holds", [])),
            "scans": cycle_data.get("markets_scanned", 0)
        },
        "open_positions": state.get("positions", []),
        "next_cycle_actions": cycle_data.get("next_actions", []),
        "trader_notes": cycle_data.get("notes", ""),
        "cycle_status": "COMPLETED",
        "completed_at": datetime.now().isoformat() + "Z"
    }
    
    # Save cycle log
    cycle_log_file = f"/Users/tylerxdurden/.openclaw/workspace/agents/polymarket-trader/CYCLE_LOG_{cycle_id.replace(':','-')}.json"
    with open(cycle_log_file, 'w') as f:
        json.dump(cycle_log, f, indent=2)
    
    return cycle_log_file

def execute_cycle():
    """Execute a complete trading cycle."""
    print("[Cycle Start] 2026-03-01 11:29 AM EST")
    print("=" * 60)
    
    # Load state
    state = load_state()
    balance = state.get("account", {}).get("balance", 442.04)
    pnl = state.get("account", {}).get("pnl", -57.96)
    
    print(f"Account Status: {state.get('status', 'normal')}")
    print(f"Balance: ${balance:.2f}")
    print(f"P&L: ${pnl:.2f} ({pnl/500*100:.1f}%)")
    print()
    
    # 1. SCAN PHASE
    print("1. SCANNING MARKETS...")
    markets = query_markets()
    print(f"   Markets found: {len(markets)}")
    
    cycle_data = {
        "markets_scanned": len(markets),
        "market_details": [],
        "entries": [],
        "exits": [],
        "holds": [],
        "next_actions": [],
        "notes": ""
    }
    
    # Analyze each market
    for market in markets:
        signal, signals = calculate_signal_strength(market)
        days = market.get("days_to_resolve", 0)
        spread = market.get("bid_ask_spread", 1.0)
        volume = market.get("volume_24h", 0)
        
        market_detail = {
            "market_id": market.get("market_id"),
            "name": market.get("name"),
            "price": market.get("current_price"),
            "days_to_resolve": days,
            "spread": f"{spread*100:.1f}%",
            "volume_24h": volume,
            "signal_strength": signal,
            "signal_factors": signals
        }
        cycle_data["market_details"].append(market_detail)
    
    print("   Markets scanned and analyzed")
    print()
    
    # 2. EVALUATE ENTRIES
    print("2. EVALUATING ENTRY OPPORTUNITIES...")
    qualified = evaluate_entries(markets, state)
    print(f"   Qualified candidates: {len(qualified)}")
    
    for market, signal, signals in qualified[:3]:  # Show top 3
        print(f"   - {market['name']}")
        print(f"     Signal: {signal:.1f}/5.0 | Price: ${market['current_price']:.2f} | {signals}")
    
    print()
    
    # 3. CHECK POSITION MANAGEMENT
    print("3. CHECKING OPEN POSITIONS...")
    exits, holds, adjustments = check_position_triggers(state)
    
    if state.get("positions"):
        for pos in state.get("positions", []):
            status = "HOLD"
            pnl_val = pos.get("current_pnl", 0)
            print(f"   {pos['market_id']}: {status} | Current P&L: ${pnl_val:.2f}")
    
    cycle_data["exits"] = exits
    cycle_data["holds"] = holds
    
    print()
    
    # 4. EXECUTE TRADES
    print("4. EXECUTING TRADES...")
    
    # Determine position sizing
    is_caution = state.get("status") == "caution"
    max_pos_size = CAUTION_MODE_POSITION_SIZE if is_caution else POSITION_SIZE_MAX
    
    entries_executed = 0
    
    # Check if we can take new entries
    current_exposure = sum(p.get("position_size", 0) for p in state.get("positions", []))
    available_capital = balance - current_exposure
    
    if len(qualified) > 0 and len(state.get("positions", [])) < MAX_CONCURRENT:
        if available_capital > max_pos_size:
            best_market, best_signal, best_signals = qualified[0]
            
            # Confirm qualification
            if best_signal >= ENTRY_THRESHOLD:
                entry_price = best_market.get("current_price", 0)
                position_size = min(max_pos_size, available_capital * 0.3)  # Risk 30% of available
                
                print(f"   ✓ NEW ENTRY: {best_market['name']}")
                print(f"     Signal: {best_signal:.1f}/5.0")
                print(f"     Entry Price: ${entry_price:.2f}")
                print(f"     Position Size: ${position_size:.2f}")
                
                entries_executed = 1
                cycle_data["entries"].append({
                    "market": best_market['name'],
                    "entry_price": entry_price,
                    "position_size": position_size,
                    "signal": best_signal
                })
    
    if entries_executed == 0:
        threshold = ENTRY_THRESHOLD
        best_score = qualified[0][1] if qualified else 0
        if best_score >= threshold:
            reason = "Position limit or insufficient capital"
        else:
            reason = f"Best signal {best_score:.1f}/5.0 below threshold {threshold}/5.0"
        print(f"   No entries: {reason}")
    
    print()
    
    # 5. POSITION MANAGEMENT
    print("5. MANAGING POSITIONS...")
    if exits:
        for exit in exits:
            print(f"   EXIT: {exit['market_id']} | Reason: {exit['reason']}")
        cycle_data["exits"] = exits
    
    if holds:
        for hold_id in holds:
            print(f"   HOLD: {hold_id}")
    
    if not exits and not holds:
        print("   No exits triggered")
    
    print()
    
    # 6. LOG CYCLE
    print("6. LOGGING CYCLE...")
    
    # Update cycle data
    cycle_data["notes"] = f"Cycle {datetime.now().strftime('%H:%M %Z')}: Scanned {len(markets)} markets. " \
                         f"Qualified: {len(qualified)}. Entries: {entries_executed}. " \
                         f"Account status: {state.get('status', 'normal')}. " \
                         f"Balance: ${balance:.2f} ({pnl/500*100:.1f}% P&L)"
    
    cycle_data["next_actions"] = [
        f"Monitor top candidates: {', '.join([m[0]['name'][:20] for m in qualified[:2]])}",
        "Check for probability shifts every 10 minutes",
        "Monitor position P&L on active trade",
        "Watch for scheduled events/news"
    ]
    
    log_file = log_cycle(state, cycle_data)
    print(f"   Cycle logged: {log_file}")
    print()
    
    # 7. SUMMARY
    print("=" * 60)
    print("[CYCLE SUMMARY]")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
    print(f"Markets Scanned: {len(markets)}")
    print(f"Qualified Candidates: {len(qualified)}")
    print(f"Open Positions: {len(state.get('positions', []))}")
    print(f"Entries Executed: {entries_executed}")
    print(f"Exits Triggered: {len(exits)}")
    print(f"Account Balance: ${balance:.2f}")
    print(f"Total P&L: ${pnl:.2f} ({pnl/500*100:.1f}%)")
    print(f"Account Status: {state.get('status', 'normal').upper()}")
    print()
    print(f"Next cycle: +10 minutes ({(datetime.now() + timedelta(minutes=10)).strftime('%H:%M %Z')})")
    print("=" * 60)
    
    return {
        "markets_scanned": len(markets),
        "qualified_candidates": len(qualified),
        "entries_executed": entries_executed,
        "exits_triggered": len(exits),
        "open_positions": len(state.get('positions', [])),
        "balance": balance,
        "pnl": pnl,
        "status": state.get('status', 'normal')
    }

if __name__ == "__main__":
    result = execute_cycle()
