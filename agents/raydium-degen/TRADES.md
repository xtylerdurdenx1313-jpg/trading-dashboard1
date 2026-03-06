# 📈 Trade Log

## Format
Each trade entry includes: timestamp, signal, token, entry/exit, P&L, win/loss, notes.

---

## Trade Template

```
### Trade #[N]
**Date:** [YYYY-MM-DD HH:MM:SS EST]
**Status:** [OPEN / CLOSED]

#### Entry
- **Signal Source:** [Tier 1/2/3/4]
- **Signal Details:** [e.g., "Whale 4Be9C bought DOGE", "FIRST 70 BUYER alert", "GMGN score 3"]
- **Token:** [SYMBOL] ([Contract Address])
- **Entry Time:** [HH:MM:SS EST]
- **Entry Price:** $[price]
- **Size:** $[usd] ([token_count] tokens)
- **Position:** [e.g., "$50 position, GMGN score 3"]

#### Whale Context (if applicable)
- **Whale Address:** [if Tier 1]
- **Whale Type:** [Conservative / Aggressive]
- **Whale Position Size:** [estimated]
- **Our Scaling:** [e.g., "25% of whale buy"]

#### On-Chain Data at Entry
- **Top 5 Buyers:** [addresses]
- **Holder Concentration:** [%]
- **Dev Wallet %:** [%]
- **Liquidity Locked:** [Yes/No, days]

#### Exit(s)
- **Exit 1:** [Time] - Sold [qty] at $[price] = [profit] (2x target)
- **Exit 2:** [Time] - Sold [qty] at $[price] = [profit] (5x target)
- **Exit 3:** [Time] - Sold [qty] at $[price] = [profit] (10x target or timeout)

#### Outcome
- **Total P&L:** $[+/-]
- **P&L %:** [+/- %]
- **Win/Loss:** [WIN / LOSS]
- **Days Held:** [N]

#### Notes
[Any observations, pattern notes, decisions made, unusual market behavior, etc.]

---
```

## Trading History

### Trade #1
**Date:** [Awaiting first trade]
**Status:** PENDING

#### Entry
- **Signal Source:** TBD
- **Signal Details:** TBD
- **Token:** TBD
- **Entry Time:** TBD
- **Entry Price:** TBD
- **Size:** TBD
- **Position:** TBD

#### Exit(s)
- **Status:** Awaiting execution

#### Outcome
- **Total P&L:** Pending
- **Win/Loss:** Pending

#### Notes
Awaiting first trading signal. Ready to execute on qualified alert.

---

## Statistics (Live Updated)

| Metric | Value |
|--------|-------|
| Total Trades | 0 |
| Winning Trades | 0 |
| Losing Trades | 0 |
| Win Rate | 0% |
| Total P&L | $0.00 |
| Avg Win | $0.00 |
| Avg Loss | $0.00 |
| Largest Win | $0.00 |
| Largest Loss | $0.00 |
| Consecutive Losses | 0 |
| Days Active | 0 |

---

## Trade Entry Instructions

When a trade closes, add an entry to this log immediately:

1. **Copy the template** (above)
2. **Increment trade #** from last entry
3. **Fill all fields** accurately
4. **Add timestamp** when trade completes
5. **Calculate P&L** carefully
6. **Update statistics table** (recalculate from all trades)
7. **Add any relevant notes** (unusual patterns, lessons learned)

### P&L Calculation
```
Total P&L = (Exit 1 Proceeds) + (Exit 2 Proceeds) + (Exit 3 Proceeds) - (Entry Cost)
P&L % = (Total P&L / Entry Cost) × 100
```

### Example
```
Entry: $50 (10,000 tokens @ $0.005)
Exit 1: Sell 3,333 @ $0.01 (2x) = $33.33
Exit 2: Sell 3,333 @ $0.025 (5x) = $83.33
Exit 3: Sell 3,334 @ $0.05 (10x) = $166.70
---
Total Proceeds: $283.36
Total Cost: $50.00
Total P&L: +$233.36 (466% return, 4.66x on the dollar)
```

---

## Notes for Trade Analysis

### What to Include in Notes
- Why you entered (which signal fired?)
- Any correlations with whale wallets?
- Unexpected market behavior?
- Why you exited at each tier?
- Any regrets or lessons?
- Market context (SOL price, volume trends)?
- Time between signal and entry?

### Example Notes
```
"Entered on Altcoinist FIRST 70 alert. GMGN showed whale 4Be9C in top 3 buyers. 
Sold 1st third at 2x after 15 minutes. Hit 5x in 45 minutes (sold 2nd third). 
Timed out at 4h, sold remainder at 9.5x (just shy of 10x target). Strong trade. 
Whale wallet seems extremely reliable for early momentum."
```

---

## Trade Review Schedule
- **After each trade:** Log immediately
- **Daily:** Calculate daily P&L, check if loss limit hit
- **Weekly:** Analyze win rate, average win/loss, identify patterns
- **Monthly:** Review strategy effectiveness, adjust position sizing if needed
