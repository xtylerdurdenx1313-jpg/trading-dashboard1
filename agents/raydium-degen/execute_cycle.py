#!/usr/bin/env python3
"""
Raydium Degen Trading Agent — Execution Cycle
Paper trading driver for SOL-based token launches.

Spawns every 5 minutes (9 AM - 8 PM EST).
Monitors Altcoinist alerts, GMGN on-chain data, whale wallets.
Executes entries/exits based on STRATEGY.md rules.
Logs all actions to STATE.json and TRADES.md.
"""

import json
import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import time

# Configuration
AGENT_DIR = Path(__file__).parent
STATE_FILE = AGENT_DIR / "STATE.json"
TRADES_FILE = AGENT_DIR / "TRADES.md"
LOG_DIR = AGENT_DIR / "logs"
LOGS_FILE = LOG_DIR / "execution.log"
ENV_FILE = AGENT_DIR / ".env"

# Constants
PAPER_TRADING = True
STARTING_CAPITAL = 500.0
ACTIVE_HOURS = ("09:00", "20:00")
SPAWN_INTERVAL = 5  # minutes
TRADE_TIMEOUT_HOURS = 4
MAX_TRADE_SIZE = 100.0
MIN_TRADE_SIZE = 25.0
DAILY_LOSS_LIMIT = 25.0
ACCOUNT_FLOOR = 450.0
HARD_STOP_LOSS_PCT = -20.0
WHALE_WALLETS = [
    "4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t",
    "H72yLkhTnoBfhBTXXaj1RBXuirm8s8G5fcVh2XpQLggM"
]

# Setup logging
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOGS_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TradingState:
    """Manages account state and position tracking."""
    
    def __init__(self):
        self.state = self.load_state()
    
    def load_state(self) -> Dict:
        """Load STATE.json or initialize fresh."""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        else:
            return self.default_state()
    
    def default_state(self) -> Dict:
        """Return default initial state."""
        return {
            "account": {
                "starting_capital": STARTING_CAPITAL,
                "current_equity": STARTING_CAPITAL,
                "available_cash": STARTING_CAPITAL,
                "total_pnl": 0.0,
                "total_pnl_pct": 0.0,
                "max_equity": STARTING_CAPITAL,
                "min_equity": STARTING_CAPITAL,
                "timestamp_created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "trading": {
                "trades_total": 0,
                "trades_won": 0,
                "trades_lost": 0,
                "win_rate": 0.0,
                "consecutive_wins": 0,
                "consecutive_losses": 0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "largest_win": 0.0,
                "largest_loss": 0.0
            },
            "daily_metrics": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "daily_pnl": 0.0,
                "daily_loss_accumulated": 0.0,
                "daily_trades": 0,
                "daily_wins": 0,
                "daily_losses": 0,
                "loss_limit_hit": False,
                "cooldown_active": False,
                "cooldown_until": None
            },
            "positions": {
                "open_positions": [],
                "open_position_count": 0,
                "total_exposure": 0.0,
                "last_entry_time": None,
                "last_exit_time": None
            }
        }
    
    def save(self):
        """Write state to STATE.json."""
        self.state["account"]["last_updated"] = datetime.now().isoformat()
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_equity(self) -> float:
        return self.state["account"]["current_equity"]
    
    def get_available_cash(self) -> float:
        return self.state["account"]["available_cash"]
    
    def get_daily_loss(self) -> float:
        return self.state["daily_metrics"]["daily_loss_accumulated"]
    
    def is_loss_limit_hit(self) -> bool:
        return self.state["daily_metrics"]["loss_limit_hit"]
    
    def is_cooldown_active(self) -> bool:
        if not self.state["daily_metrics"]["cooldown_active"]:
            return False
        cooldown_until = self.state["daily_metrics"]["cooldown_until"]
        if cooldown_until and datetime.fromisoformat(cooldown_until) > datetime.now():
            return True
        self.state["daily_metrics"]["cooldown_active"] = False
        return False
    
    def record_trade(self, token: str, entry_price: float, size_usd: float, 
                     signal_tier: int, whale_correlation: bool = False):
        """Record a trade entry."""
        position = {
            "token": token,
            "entry_time": datetime.now().isoformat(),
            "entry_price": entry_price,
            "size_usd": size_usd,
            "size_tokens": size_usd / entry_price if entry_price > 0 else 0,
            "signal_tier": signal_tier,
            "whale_correlation": whale_correlation,
            "exit_1_price": None,
            "exit_1_time": None,
            "exit_2_price": None,
            "exit_2_time": None,
            "exit_3_price": None,
            "exit_3_time": None,
            "status": "OPEN",
            "pnl": 0.0
        }
        self.state["positions"]["open_positions"].append(position)
        self.state["positions"]["open_position_count"] += 1
        self.state["positions"]["total_exposure"] += size_usd
        self.state["positions"]["last_entry_time"] = position["entry_time"]
        self.state["account"]["available_cash"] -= size_usd
        self.save()
        logger.info(f"[TRADE] ENTRY: {token} @ ${entry_price:.8f}, size ${size_usd}, signal: Tier{signal_tier}")
    
    def exit_position(self, position_idx: int, exit_tier: int, exit_price: float, 
                      qty: float, reason: str = ""):
        """Record a partial or full exit."""
        if position_idx >= len(self.state["positions"]["open_positions"]):
            return
        
        pos = self.state["positions"]["open_positions"][position_idx]
        entry_cost = pos["size_usd"]
        proceeds = qty * exit_price
        pnl = proceeds - (qty / pos["size_tokens"] * entry_cost if pos["size_tokens"] > 0 else 0)
        
        if exit_tier == 1:
            pos["exit_1_price"] = exit_price
            pos["exit_1_time"] = datetime.now().isoformat()
        elif exit_tier == 2:
            pos["exit_2_price"] = exit_price
            pos["exit_2_time"] = datetime.now().isoformat()
        elif exit_tier == 3:
            pos["exit_3_price"] = exit_price
            pos["exit_3_time"] = datetime.now().isoformat()
            pos["status"] = "CLOSED"
            pos["pnl"] = pnl
        
        # Update metrics
        self.state["account"]["current_equity"] += pnl
        self.state["account"]["available_cash"] += proceeds
        self.state["positions"]["total_exposure"] -= entry_cost * (qty / pos["size_tokens"])
        self.state["positions"]["last_exit_time"] = datetime.now().isoformat()
        
        # Handle loss limit and cooldown
        if pnl < 0:
            self.state["daily_metrics"]["daily_loss_accumulated"] += abs(pnl)
            self.state["daily_metrics"]["daily_losses"] += 1
            self.state["trading"]["consecutive_losses"] += 1
            self.state["trading"]["consecutive_wins"] = 0
            
            if self.state["daily_metrics"]["daily_loss_accumulated"] >= DAILY_LOSS_LIMIT:
                self.state["daily_metrics"]["loss_limit_hit"] = True
                logger.warning(f"[ALERT] Daily loss limit hit: ${self.get_daily_loss():.2f}")
            
            if self.state["trading"]["consecutive_losses"] >= 2:
                self.state["daily_metrics"]["cooldown_active"] = True
                self.state["daily_metrics"]["cooldown_until"] = (
                    datetime.now() + timedelta(hours=2)
                ).isoformat()
                logger.warning(f"[ALERT] 2 consecutive losses. Cooldown activated for 2 hours.")
        else:
            self.state["daily_metrics"]["daily_pnl"] += pnl
            self.state["daily_metrics"]["daily_wins"] += 1
            self.state["trading"]["consecutive_wins"] += 1
            self.state["trading"]["consecutive_losses"] = 0
        
        # Update account stats
        self.state["trading"]["trades_total"] += 1
        if pnl >= 0:
            self.state["trading"]["trades_won"] += 1
        else:
            self.state["trading"]["trades_lost"] += 1
        
        if self.state["trading"]["trades_total"] > 0:
            self.state["trading"]["win_rate"] = (
                self.state["trading"]["trades_won"] / self.state["trading"]["trades_total"]
            ) * 100
        
        # Update max/min equity
        if self.state["account"]["current_equity"] > self.state["account"]["max_equity"]:
            self.state["account"]["max_equity"] = self.state["account"]["current_equity"]
        if self.state["account"]["current_equity"] < self.state["account"]["min_equity"]:
            self.state["account"]["min_equity"] = self.state["account"]["current_equity"]
        
        self.save()
        logger.info(f"[EXIT] Tier {exit_tier}: {pos['token']}, ${pnl:+.2f} P&L ({pnl/entry_cost*100:+.1f}%), {reason}")


class AlertMonitor:
    """Monitors Telegram and GMGN alerts."""
    
    def check_altcoinist_alerts(self) -> List[Dict]:
        """Poll Telegram @altcoinist_trenchbot for alerts."""
        # This would connect to Telegram API in production
        # For now, returns empty list (manual mode)
        logger.info("[INFO] Checking Altcoinist alerts...")
        # In real implementation: fetch latest messages from Telegram bot
        # Parse for "FIRST 70", "WHALE WALLET", etc.
        return []
    
    def check_gmgn_new_launches(self) -> List[Dict]:
        """Query GMGN for new token launches and first 70 buyers."""
        logger.info("[INFO] Scanning GMGN for new launches...")
        # This would query GMGN.ai API or web scraping in production
        # For now, returns empty list (manual mode)
        # Returns: [{"token": "DOGE", "score": 3, "whale_detected": True, ...}]
        return []
    
    def check_whale_wallet_activity(self) -> List[Dict]:
        """Monitor whale wallet addresses for transactions."""
        logger.info(f"[INFO] Monitoring {len(WHALE_WALLETS)} whale wallets...")
        # This would query Solana RPC for recent transactions
        # For now, returns empty list
        # Returns: [{"wallet": "4Be9C...", "token": "DOGE", "size_usd": 500, ...}]
        return []


class StrategyExecutor:
    """Evaluates signals and executes trades."""
    
    def __init__(self, state: TradingState):
        self.state = state
        self.monitor = AlertMonitor()
    
    def evaluate_entry(self, signal: Dict) -> Optional[Dict]:
        """Evaluate if a signal meets entry criteria."""
        # Check trading hours
        current_time = datetime.now().strftime("%H:%M")
        if not (ACTIVE_HOURS[0] <= current_time <= ACTIVE_HOURS[1]):
            return None
        
        # Check loss limits
        if self.state.is_loss_limit_hit():
            logger.info("[INFO] Daily loss limit hit, skipping entries")
            return None
        
        # Check cooldown
        if self.state.is_cooldown_active():
            logger.info("[INFO] Cooldown active, skipping entries")
            return None
        
        # Check account floor
        if self.state.get_equity() <= ACCOUNT_FLOOR:
            logger.warning(f"[ALERT] Account below floor (${self.state.get_equity():.2f}), no new entries")
            return None
        
        # Placeholder: actual signal evaluation logic
        return None
    
    def execute_cycle(self):
        """Main execution cycle (runs every 5 minutes)."""
        logger.info(f"[CYCLE] Starting execution cycle. Equity: ${self.state.get_equity():.2f}")
        
        # 1. Check for new alerts
        altcoinist_alerts = self.monitor.check_altcoinist_alerts()
        gmgn_launches = self.monitor.check_gmgn_new_launches()
        whale_activity = self.monitor.check_whale_wallet_activity()
        
        # 2. Check for exit conditions on open positions
        now = datetime.now()
        for idx, pos in enumerate(self.state.state["positions"]["open_positions"]):
            if pos["status"] != "OPEN":
                continue
            
            entry_time = datetime.fromisoformat(pos["entry_time"])
            hours_held = (now - entry_time).total_seconds() / 3600
            
            # Check timeout (4 hours)
            if hours_held >= TRADE_TIMEOUT_HOURS and pos["exit_1_price"] is None:
                logger.warning(f"[TIMEOUT] {pos['token']} held {hours_held:.1f}h, liquidating")
                # In live mode: close position at market
                # For paper mode: simulate close at current market price (would fetch from GMGN)
                # self.state.exit_position(idx, 1, market_price, pos["size_tokens"], "timeout")
        
        # 3. Evaluate new signals
        for signal in altcoinist_alerts + gmgn_launches + whale_activity:
            entry = self.evaluate_entry(signal)
            if entry:
                self.state.record_trade(
                    token=entry["token"],
                    entry_price=entry["price"],
                    size_usd=entry["size"],
                    signal_tier=entry["tier"],
                    whale_correlation=entry.get("whale_correlation", False)
                )
        
        logger.info(f"[CYCLE] Complete. Open positions: {self.state.state['positions']['open_position_count']}")
        self.state.save()


def main():
    """Main entry point."""
    try:
        logger.info("=" * 60)
        logger.info("Raydium Degen Trading Agent - Execution Cycle")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info("=" * 60)
        
        # Load or initialize state
        state = TradingState()
        
        # Run execution cycle
        executor = StrategyExecutor(state)
        executor.execute_cycle()
        
        logger.info("Cycle completed successfully.\n")
        return 0
    
    except Exception as e:
        logger.error(f"[ERROR] Execution failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
