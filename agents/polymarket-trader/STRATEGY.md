# Polymarket Trading Strategy — SHORT-TERM FOCUS

## Strategy Overview

**Goal:** Scalp short-term probability movements in high-liquidity markets

**Timeframe:** Days to hours (resolve within 1-14 days)

**Capital:** $500 USDC (paper trading)

---

## Market Selection

### Focus Categories
- **Hot Politics:** Current election developments, votes, appointments
- **Sports:** Near-term event outcomes (next game, round, match)
- **Crypto:** Bitcoin/Ethereum price moves, narrative shifts
- **Tech/Business:** Product launches, earnings, regulatory decisions
- **Entertainment:** Award ceremonies, show winners (high volume near date)

### Liquidity Requirements
- **Min Bid-Ask Spread:** <2% (avoid illiquid markets)
- **Min Volume (24h):** >$500 total
- **Min Days to Resolution:** 1 day (no same-day resolution markets)
- **Max Days to Resolution:** 14 days (focus on short-term movement)

### Probability Range
- **Enter:** 30-70% probability only (avoid edges where liquidity is thin)
- **Avoid:** <10% and >90% (liquidity traps, low volume)

---

## Entry Rules

**Entry Signal (Both conditions must be true):**

1. **Probability Shift:** Market probability moved 3-5% in your direction in last 2 hours
2. **Volume Confirmation:** Volume in last 1 hour is above 24h average volume
3. **Liquidity Check:** Bid-ask spread <2%, min $100 liquidity depth

**Trade Type:**
- **YES bets:** When probability is drifting down (fade the sellers)
- **NO bets:** When probability is drifting up (fade the buyers)

**Position Size Formula:**
```
Risk per trade = 2% of $500 = $10 max loss
Position size = $10 ÷ probability shift
```

Example: If market is at 50%, enter 5-10% of account ($25-50 USDC)

---

## Exit Rules

### Profit Taking
- **Quick Win:** Sell at +3-5% price improvement
- **Scalp Stop:** Exit if no movement after 30 min
- **Target:** 2:1 reward-to-risk (risk $10 to win $20)

### Stop Loss
- **Hard Stop:** -3% from entry (non-negotiable)
- **Time Stop:** Close position if unresolved and no movement after 4 hours

### Trailing Exit
- If profit reaches +5%, let it run with trailing stop at +3%

---

## Position Management

### Sizing
- **Max position:** 10% of account ($50 USDC)
- **Max open positions:** 2 concurrent markets
- **Max exposure:** 20% of account at any time ($100 USDC)

### Risk Control
- **Max loss per trade:** $10 (2% of capital)
- **Max loss per day:** $25 (5% of capital)
- **Max drawdown:** $50 (10% of capital) → STOP TRADING if hit

### Diversification
- Don't trade same category twice (no two crypto markets open at once)
- Mix politics, sports, and crypto for variety

---

## What NOT To Do

- ❌ **Don't chase:** If you missed the move, wait for the next opportunity
- ❌ **Don't revenge trade:** After a loss, wait 30 min before next entry
- ❌ **Don't hold through news:** Close before known announcements (elections, votes, etc.)
- ❌ **Don't average down:** If wrong, stop loss handles it
- ❌ **Don't overtrade:** "No setup found" is a valid decision every spawn
- ❌ **Don't trade illiquid:** Always check spread and volume first
- ❌ **Don't take extreme odds:** <15% and >85% are money traps

---

## Daily Checklist

Every spawn cycle:
- [ ] Check market liquidity (spread <2%)
- [ ] Scan for 3-5% probability shifts in last 2 hours
- [ ] Verify entry criteria: shift + volume + liquidity
- [ ] Size position to 2% max loss rule
- [ ] Set profit target (3-5%) and stop loss (-3%)
- [ ] Check open positions: any hitting TP/SL/time stops?
- [ ] Update STATE.json with new balance, trades, P&L
- [ ] Log all trades with entry/exit prices and reasoning

---

**Status:** ✅ Ready for paper trading. Focus on learning position sizing and entry discipline. Execution speed matters here.
