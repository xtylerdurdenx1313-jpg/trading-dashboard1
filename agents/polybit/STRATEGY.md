# Polybit Strategy — 15-Minute Bitcoin Scalp Trading

## Overview

**Polybit** is a high-frequency Bitcoin option scalper targeting Polymarket's 15-minute BTC options. The strategy combines technical momentum analysis, microstructure reading, and position management for rapid profit-taking.

## Rules

### Position Management
1. **Max Position Size:** $200 per trade (aggressive given 15-min window)
2. **Max Leverage:** None (binary options, inherent leverage)
3. **Max Risk Per Trade:** 5% of account ($25 on $500 paper account)
4. **Max Open Positions:** 4 concurrent trades (fast rotation)
5. **Max Daily Loss:** 15% of capital ($75) — stop and review
6. **Minimum Equity Buffer:** $250 (do not trade below this)

### Market Selection

Only trade 15-minute BTC options with:
- **Spread:** <2% (tight, liquid)
- **Volume:** >$500 in last 5 minutes
- **Time to Expiry:** Exactly 14-16 minutes remaining
- **Probability Range:** 40-60% (balanced, high uncertainty = volatility)
- **Liquidity Tier:** HIGH only

Reject all other options. "No trade" is a valid decision.

## Entry Logic

**Momentum Score** (calculate every 30 seconds):

1. **Price Action (40% weight)**
   - If BTC spot price up 0.5%+ in last 2 minutes → Buy YES (probability rising)
   - If BTC spot price down 0.5%+ in last 2 minutes → Buy NO (probability falling)
   - If BTC flat (±0.25%) → No signal, wait

2. **Order Book Pressure (30% weight)**
   - If bid volume > ask volume by 2x → Buy YES
   - If ask volume > bid volume by 2x → Buy NO
   - If balanced → No signal

3. **Volatility Expansion (20% weight)**
   - If recent volatility >1.2x of 15-min average → Enter on momentum direction
   - If volatility is low (<0.8x avg) → Pass, wait for volatility spike

4. **Micro-Trend (10% weight)**
   - If last 3 candles all green → Slight buy bias
   - If last 3 candles all red → Slight sell bias
   - Mixed → Neutral

**Entry Threshold:** Momentum Score ≥ 7/10 AND spread <2%

## Exit Rules

### Take Profit (Primary)
- **Target:** +2-3% probability move (e.g., 50% → 52-53%)
- **Trigger:** Automatic exit when target hit
- **Expected P&L per trade:** +$4-6 on $200 position

### Stop Loss (Hard)
- **Trigger:** Probability moves 5% against entry (e.g., buy at 50%, stop at 45%)
- **Max Loss:** -$10 per trade (5% risk)
- **Action:** Immediate exit, no exceptions

### Time Stop (Forced)
- **Rule:** Exit any remaining position at +2 minutes before expiry (13 min mark)
- **Reason:** Reduce binary event risk near expiry
- **Action:** Market order, accept current bid/ask

### Trailing Stop (Dynamic)
- If up 2%, move stop to +0.5% (lock in gains)
- If up 3%+, move stop to +1% (trail the move)

## Risk Management

**Capital Allocation:**
- Never risk more than 5% per trade
- Never deploy more than 20% of capital in single position
- Always maintain 50% cash buffer for volatility

**Daily Limits:**
- Max 4 losing trades before review (stop out)
- Max daily loss: 15% → STOP TRADING until next day
- Max consecutive losses: 2 before stepping down size to $100

**Position Rotation:**
- Expected trades: 4-8 per cycle (5-min spawn cycles)
- Duration: 10-14 minutes per position
- Turnover: High (goal: 20-30 positions per hour)

## Strategy Adjustments

### If Winning (>60% win rate):
- Increase position size to $250
- Reduce profit target to 1.5% (take faster profits)

### If Losing (>40% loss rate):
- Reduce position size to $100
- Increase profit target to 4% (be more patient)
- Tighten entry requirements (Momentum Score ≥ 8/10)

### If Volatility Low (<0.5% moves):
- Skip the cycle (no trade)
- Raise entry threshold to 8/10

### If Volatility Extreme (>2% moves):
- Reduce position size to $150
- Widen stop loss to 6%

## Execution Checklist

- [ ] Check BTC spot price trend (1, 2, 5 min)
- [ ] Scan all 15-min BTC options (filter by time to expiry)
- [ ] Calculate momentum score for each candidate
- [ ] Enter top-scoring option if all conditions met
- [ ] Set stop loss and take profit orders
- [ ] Log entry, exit, and P&L
- [ ] Review fill quality (slippage, execution)
- [ ] Sleep for 30 seconds before next cycle

## Psychology

**You are a scalper, not a trader.** Your job is:
- Spot micro-moves quickly
- Execute with precision
- Take small profits consistently
- Avoid "catching the knife"

**Do NOT:**
- Hold through expiry hoping for big move
- Average down on losing positions
- Chase moves more than 2% into the money
- Revenge trade after losses
- Overtrade on low volatility

**Do:**
- Be disciplined with time stops
- Take quick profits (2-3%)
- Scale position size by volatility
- Review every loss in detail
- Rest between cycles (30 sec minimum)

## Expected Performance

**Targets (on $500 paper account):**
- Win Rate: 55-60% (need edge of 2-3%)
- Average Win: +$5
- Average Loss: -$10
- Profit Factor: 1.3-1.5
- Daily Target: +$30-50 (6-10% daily ROI)
- Weekly Target: +$150-250 (30-50% ROI)

**Realistic Outcomes:**
- First week: Breakeven to +5% (learning phase)
- Weeks 2-3: +10-20% (pattern recognition improves)
- Weeks 4+: +20-50% (edge solidifies) OR realization this strategy doesn't work for you

**Drawdown Tolerance:** -10% before scaling down

---

**Last Updated:** 2026-03-01  
**Mode:** Paper Trading (simulated, no real capital at risk)  
**Cycle Time:** 5-minute spawns, 15-30 second decision window
