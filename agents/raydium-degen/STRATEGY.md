# 📊 Raydium Degen Trading Strategy

## Entry Signals (Ranked by Power)

### Tier 1: Whale Wallet Mirroring
**Power:** ⭐⭐⭐⭐⭐

Mirror buys from identified whale wallets:
- **4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t** — Conservative whale. Known for 50x flips. Low drawdown. Follow within 2 blocks.
- **H72yLkhTnoBfhBTXXaj1RBXuirm8s8G5fcVh2XpQLggM** — Aggressive whale. High volume plays. Captures early momentum. Follow within 1 block.

**Action:** When whale wallet shows buy transaction on Raydium/Pump.fun new token → Entry signal. Size based on whale's transaction size (scale down for paper account).

### Tier 2: Altcoinist Telegram Alerts
**Power:** ⭐⭐⭐⭐

Subscribe to @altcoinist_trenchbot alerts for:
- New token launches
- Whale wallet transactions
- Unusual volume spikes
- First-mover buys

**Alert Types:**
- "FIRST 70 BUYER" — Highest confidence entry
- "WHALE WALLET: [address] bought [amount]" — Mirror immediately
- "NEW LAUNCH: [token]" — Scout token, wait for whale confirmation or volume spike

**Action:** Enter on FIRST 70 BUYER alerts. Scale for WHALE WALLET alerts based on size.

### Tier 3: GMGN.ai On-Chain Signals
**Power:** ⭐⭐⭐⭐

GMGN (gmgn.ai) first 70 buyer detection:
- Check within 30 seconds of token launch
- Identify top 5 buyers
- Correlate with known whale wallets
- Check transaction history of top buyers

**Signal Scoring:**
- Known whale in top 3 buyers → +3 points (strong entry)
- Multiple whales in top 10 → +2 points
- Unusual buyer count pattern (coordinated buys) → +1 point
- Any suspicious patterns (wash trading, obvious bots) → -5 points (skip)

**Action:** Entry confidence = signal score. Score ≥2 → Enter. Score 1 → Scout only (wait for confirmation). Score <1 → Skip.

### Tier 4: Dune Analytics Patterns
**Power:** ⭐⭐⭐

Monitor Raydium/Pump.fun dashboards:
- Token liquidity unlocking patterns
- Holder concentration (avoid rug risk)
- Buy/sell ratio trends (early momentum)
- Whale wallet accumulation history

**Risk Filters:**
- Holder concentration >50% → Skip (rug risk)
- Dev wallet >30% → Skip (exit risk)
- Liquidity locked <24h → Extra caution

**Action:** Use as confirmation layer. If on-chain data shows rug red flags → Veto entry regardless of alert.

---

## Position Sizing

### Entry Rules
- **Base Position:** $50-100 per trade
- **Entry Price:** Market or limit within 2% of market
- **Max Position:** Single trade never exceeds $100
- **Account-Based Limits:** Never use >10% of account per trade ($50 at $500 start)

### Scaling
- **Normal Entry:** $50 standard size
- **High Conviction** (multiple Tier 1 signals + whale correlation): $75-100
- **Scout/Low Conviction:** $25-50
- **After 2 consecutive losses:** Reduce to $25 minimum, wait for cooldown

### Stop Loss
- **Hard Stop:** -20% from entry price (non-negotiable)
- **Daily Loss Limit:** -$25 aggregate per day (max 2.5 trades at max loss)
- **After 2 Consecutive Losses:** Pause trading for 2 hours, next trade size $25 max
- **Account Floor:** If balance drops to $450 → No new trades, reduce position size to $25, protect capital

---

## Exit Strategy (Scaled Exits)

### Baseline: 3-Tier Exit
- **1st Exit: 33% of position** — Sell at 2x entry price (take profit, reduce risk)
- **2nd Exit: 33% of position** — Sell at 5x entry price (capture mid-range gains)
- **3rd Exit: 34% of position** — Sell at 10x entry price OR 4 hours after entry (timeout rule)

### Timeout Rule
If position doesn't hit 2x within 4 hours → Liquidate entire position at market. Prevents bagholding, frees capital for next cycle.

### Modifications
- **Early Exit on Bearish On-Chain Data:** If holders start dumping, whale wallets sell, or volume collapses → Exit immediately (don't wait for targets)
- **News/Market Shock:** If broader market crashing, SOL down >3% → Close position, pause 30 min
- **Profit Locking:** If 5x hit early → Can exit full position instead of holding for 10x (discretionary for very high-momentum plays)

### Example Fills
```
Entry: $0.01, Position: $100 (10,000 tokens)
Exit 1: Sell 3,333 tokens at $0.02 (2x) → +$33.33 profit
Exit 2: Sell 3,333 tokens at $0.05 (5x) → +$133.33 profit
Exit 3: Sell 3,334 tokens at $0.10 (10x) OR at 4h timeout
```

---

## Daily Risk Limits

### Loss Cap
- **Max daily loss:** $25 (hard limit)
- **Equals:** ~5% of account
- **Trigger:** Once hit, no new trades until next day

### Consecutive Loss Cooldown
- **After 2 losing trades in a row:**
  - Pause trading for 2 hours
  - Next entry: $25 max size (half minimum)
  - Resume normal sizing after first winning trade

### Account Protection
- **Account falls below $450:** 
  - No new trades
  - Reduce all position sizes to $25
  - Focus on exiting winners at any profit level
  - Resume normal trading once back above $475

---

## Trade Logging & State

Every trade logged to TRADES.md with:
- Entry timestamp
- Entry signal (which Tier)
- Token symbol and address
- Entry price and size
- Exit prices and times
- P&L
- Win/loss status
- Notes (whale correlation, unusual data, etc.)

STATE.json updated after every trade:
- Current equity
- Total P&L (since start)
- Trade count (total, wins, losses)
- Win rate %
- Daily P&L
- Last trade timestamp
- Current open positions

---

## Signal Priority Flowchart

```
New Launch Detected?
├─ Whale wallet in top 5 buyers (Tier 1 + 2)?
│  └─ YES → ENTER $75-100, high confidence
├─ Altcoinist FIRST 70 alert (Tier 2)?
│  └─ YES + GMGN score ≥2 → ENTER $50-75
├─ GMGN score ≥3 + no red flags (Tier 3)?
│  └─ YES → ENTER $50
├─ Multiple signals but low score?
│  └─ SCOUT (25-50 size) OR SKIP
└─ Any rug red flags (Tier 4)?
   └─ YES → VETO, skip trade entirely
```

---

## Notes on Whale Wallets

### Conservative Whale: 4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t
- Track record: 50x average flips
- Entry pattern: Enters early, patient holding
- Exit pattern: Graduated exits around 20-50x
- Risk profile: Low drawdown, highly selective
- **Action:** Enter when this whale enters, hold longer (up to 10x target)

### Aggressive Whale: H72yLkhTnoBfhBTXXaj1RBXuirm8s8G5fcVh2XpQLggM
- Track record: High-volume captures, 5-20x typical
- Entry pattern: Fast entries on momentum
- Exit pattern: Quick exits at 2-5x
- Risk profile: Higher volatility, frequent small wins
- **Action:** Enter immediately on buy signal, use 5x exit target (don't hold for 10x)

---

## Risk Calibration

### Daily Win Rate Targets
- 50% win rate = sustainable
- 60%+ = excellent (adjust position sizing up if proven)
- <40% = strategy adjustment needed

### Position Adjustment
- Win rate consistently >60% → Can increase to $100-125 per trade
- Win rate 40-50% → Stick to $50-75
- Win rate <40% → Reduce to $25-50, audit strategy

---

## Final Rules (Non-Negotiable)

1. **Never** exceed hard stop loss (-20% from entry)
2. **Never** trade after account hits $25 daily loss limit
3. **Never** open new positions without clear exit plan
4. **Always** scale into winners, retreat into losers
5. **Always** exit on timeout (4h) if targets not hit
6. **Always** log every trade with full reasoning
7. **Always** cool down 2h after 2 consecutive losses
8. **Always** protect the $450 account minimum
