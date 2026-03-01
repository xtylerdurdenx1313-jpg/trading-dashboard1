# Polybit Agent

**Bitcoin 15-Minute Binary Options Scalper**

## Quick Facts

- **Target:** Polymarket 15-min BTC options
- **Strategy:** Momentum scalping with tight risk management
- **Position Size:** $100-200 per trade (scalable)
- **Win Target:** 55-60% (2-3% per win)
- **Spawn Frequency:** Every 5 minutes
- **Mode:** Paper trading ($500 starting capital)

## How It Works

Each spawn cycle (5 minutes):

1. **Scan** — Find all 15-min BTC options on Polymarket
2. **Filter** — Apply liquidity/spread/time criteria
3. **Score** — Calculate momentum for top candidates
4. **Execute** — Enter best setup if threshold met
5. **Manage** — Monitor positions, exit on target/stop
6. **Log** — Record all trades to TRADES.md

Expected trades: 0-2 per cycle (selective)

## Monitoring

Real-time data available in:
- **STATE.json** — Account equity, positions, daily P&L
- **TRADES.md** — Individual trade details
- **REPORT.md** — Daily performance summary

Dashboard pulls from STATE.json automatically.

## Safety

Hard stops in place:
- Max 5% risk per trade
- Max 15% daily loss
- Max 4 concurrent positions
- Stop losses always set immediately

## One Week Test

Running through **2026-03-08** to validate:
- Win rate consistency
- Drawdown management
- Scalping edge on 15-min options
- Parameter optimization

---

**Status:** ✅ Live  
**Created:** 2026-03-01 14:18 UTC
