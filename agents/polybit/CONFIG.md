# Polybit Configuration

## Agent Overview

**Name:** Polybit (Bitcoin 15-min scalper)  
**Exchange:** Polymarket  
**Asset:** BTC binary options (15-minute expiry)  
**Trading Mode:** Paper (simulated)  
**Strategy Type:** Momentum scalping  

---

## Polymarket CLOB Authentication

✅ **Uses same credentials as polymarket-trader**

Stored in:
```
POLYMARKET_API_KEY = "8ae662ee-020d-3651-55f5-6235d5f3582d"
POLYMARKET_API_SECRET = "DL3_ozipxLzX7nwHNEJ_onVuYHwl3B4EP4s9-9uu3sM="
POLYMARKET_API_PASSPHRASE = "c3d8ec3719a8dbaae2385e92d702fb255e4fcbcdc41be577df840336bebb2157"
POLYMARKET_ENDPOINT = "https://clob.polymarket.com"
POLYMARKET_CHAIN_ID = 137  # Polygon mainnet
```

---

## Account Parameters

| Setting | Value | Notes |
|---------|-------|-------|
| **Starting Capital** | $500.00 | Paper trading (simulated) |
| **Position Size** | $100-200 | Scales with volatility |
| **Max Risk Per Trade** | 5% ($25) | Hard stop |
| **Max Daily Loss** | 15% ($75) | Stop all trading if hit |
| **Max Positions Open** | 4 | Fast rotation |

---

## Market Filters

Target options must match ALL:

| Filter | Requirement | Reason |
|--------|-------------|--------|
| Asset | BTC only | Bitcoin 15-min options |
| Time to Expiry | 14-16 min | Sweet spot for scalping |
| Spread | <2% | Tight, liquid markets |
| Volume | >$500 in 5 min | Enough liquidity to exit |
| Probability | 40-60% | Balanced odds = volatility |
| Liquidity Tier | HIGH | Fast fills, no slippage |

---

## Execution Parameters

| Parameter | Value | Adjustment |
|-----------|-------|-----------|
| Momentum Score Threshold | 7/10 | Increase to 8/10 if losing |
| Profit Target | 2-3% probability | Reduce to 1.5% if winning |
| Stop Loss | 5% against entry | Widen to 6% if volatile |
| Time Stop | 2 min before expiry | Fixed, no negotiation |
| Trailing Stop | +0.5% after 2% gain | Protect wins |

---

## Spawn Schedule

**Frequency:** Every 5 minutes  
**Runtime per spawn:** 30-60 seconds (decision window)  
**Expected trades per spawn:** 0-2 (selective)  
**Daily cycles:** 288 (5-min × 24h)  

---

## Performance Tracking

Log all trades to:
- `TRADES.md` — individual trade details
- `STATE.json` — account equity + positions
- `REPORT.md` — daily P&L summary

---

## Safety Switches

If any of these trigger, STOP ALL TRADING:

- [ ] Daily loss exceeds -$75 (15%)
- [ ] Account equity drops below $250
- [ ] 3 consecutive losing trades
- [ ] Spread widens >3% (market issue)
- [ ] No qualifying options available (market down)

---

## Notes

- Paper trading only — no real capital at risk
- 1-week test period (through 2026-03-08)
- Goal: Validate 15-min scalping edge
- Monitor: Win rate, drawdown, consistency
- Adjust: Strategy parameters based on live results

---

**Created:** 2026-03-01  
**Status:** Ready to deploy
