# Polymarket Trader Agent

Specialized trading agent for Polymarket prediction markets.

## What This Agent Does

- Monitors Polymarket event markets (politics, sports, crypto, etc.)
- Analyzes market conditions and probability shifts
- Executes trades based on strategy rules
- Tracks positions and P&L across markets
- Reports performance and market insights

## Files

- **CONFIG.md** — API setup and credentials
- **STRATEGY.md** — Trading rules and logic
- **TRADES.md** — Trade log and history
- **STATE.json** — Current positions and account state

## Quick Start

1. Set up API credentials in CONFIG.md
2. Define your strategy in STRATEGY.md
3. Spawn the agent with clear instructions
4. Agent will begin monitoring and trading

## Commands

```
spawn polymarket-trader --task "scan markets and execute trades"
```

---

Ready to trade.
