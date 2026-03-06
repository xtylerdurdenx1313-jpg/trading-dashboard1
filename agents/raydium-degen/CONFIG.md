# ⚙️ Raydium Degen Agent — Operational Configuration

## Paper Trading Account

```
Starting Capital: $500 USD (USDC equivalent)
Mode: Paper Trading (no real funds)
Target Equity Range: $450 - $1000
Max Daily Loss: $25 USD
Max Trade Size: $100 USD
Min Trade Size: $25 USD (after cooldown)
```

## Trading Pairs & Exchanges

### Primary Exchange: Raydium
- Protocol: Automated Market Maker (AMM) on Solana
- Focus: New token launches, liquidity pools
- Strategy: First 70 buyers, whale mirroring

### Secondary: Pump.fun
- Protocol: Fair-launch memecoin platform
- Focus: Early-stage token detection
- Strategy: Scout signals, confirm with Raydium data

### Token Selection Criteria
- **Age:** Brand new launches only (<10 minutes old preferred)
- **Blockchain:** SOL-based tokens exclusively
- **Liquidity:** Initial liquidity $10k-$1M (avoid low-float dumps)
- **Type:** Any (memecoins, utility, defi, etc.) if signals align

---

## Data Sources & Tools

### 1. GMGN.ai (gmgn.ai)
**Purpose:** On-chain first 70 buyer detection
- Real-time token tracking
- Top buyer identification
- Holder analysis
- Rug risk scoring
- **Update Frequency:** Real-time
- **Cost:** Free tier available
- **Integration:** Manual check or API (if available)

### 2. Telegram @altcoinist_trenchbot
**Purpose:** Real-time alert notifications
- New token launches
- Whale wallet transactions
- Volume anomalies
- First-mover alerts
- **Update Frequency:** Instant (alert-based)
- **Cost:** Free
- **Integration:** Bot polling or webhook (manual check every 1-2 minutes)

### 3. Dune Analytics (dune.com)
**Purpose:** Advanced on-chain analytics
- Raydium/Pump.fun dashboards
- Holder concentration tracking
- Dev wallet monitoring
- Buy/sell patterns
- **Update Frequency:** 2-5 minutes
- **Cost:** Free (dashboard queries)
- **Integration:** Dashboard review before entry

### 4. Raydium RPC Endpoint
**Purpose:** Direct blockchain queries
- Real-time balance checks
- Transaction status
- Pool state queries
- Gas monitoring
- **Endpoint:** https://api.mainnet-beta.solana.com (default free tier)
- **Cost:** Free (public RPC)
- **Integration:** Query via Python `solders` library

### 5. Solscan.io
**Purpose:** Token verification and explorer
- Verify token contracts
- Check holder lists
- Confirm transaction history
- Identify scams/rugs
- **Update Frequency:** Real-time
- **Cost:** Free
- **Integration:** Manual verification before entry

---

## Execution Environment

### Spawn Frequency
- **Cycle Interval:** Every 5 minutes (300 seconds)
- **Reason:** Capture new launches, check whale activity, exit timeout
- **Schedule:** 9 AM - 8 PM EST (11 hours per day)
- **Spawns per Day:** ~132 cycles (11 hours × 60 min ÷ 5 min)

### Monitoring Loop (per cycle)
```
1. Check Telegram alerts (Altcoinist) — 30 seconds
2. Query GMGN for new launches — 30 seconds
3. Monitor whale wallet addresses — 20 seconds
4. Check open position status — 10 seconds
5. Evaluate exit conditions (timeout, targets) — 10 seconds
6. Execute exits if triggered — 20 seconds
7. Log results to STATE.json — 10 seconds
8. Sleep until next cycle
```
**Total cycle time:** ~2-3 minutes (leaves buffer for delays)

### Time Window
- **Active Trading:** 9:00 AM - 8:00 PM EST
- **Closed Outside Window:** No new entries before 9 AM or after 8 PM
- **Exit Behavior:** Open positions can exit anytime, even outside window
- **Rationale:** Align with US market hours and peak pump.fun activity

---

## Account State Management

### STATE.json (Updated Every Cycle)
Tracks real-time account metrics:
```json
{
  "timestamp": "2026-03-06T07:19:00Z",
  "equity": 500.00,
  "starting_capital": 500.00,
  "total_pnl": 0.00,
  "total_pnl_pct": 0.0,
  "trades_total": 0,
  "trades_won": 0,
  "trades_lost": 0,
  "win_rate": 0.0,
  "daily_pnl": 0.00,
  "daily_loss_accumulated": 0.00,
  "consecutive_losses": 0,
  "last_trade_timestamp": null,
  "cooldown_until": null,
  "open_positions": [],
  "cash_available": 500.00
}
```

### TRADES.md (Append Only)
Each trade logged with:
- Entry timestamp
- Signal source (Tier 1/2/3/4)
- Token info
- Entry price & size
- Exit price(s) & time(s)
- P&L
- Win/loss
- Notes

---

## API Keys & Environment Variables

### Required (.env file)
```
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id

# Solana RPC
SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com

# Optional: Dune API (for dashboard queries)
DUNE_API_KEY=your_dune_key_here

# Optional: GMGN API (if available)
GMGN_API_KEY=your_gmgn_key_here

# Paper Trading Mode Flag
PAPER_TRADING=true
PAPER_TRADING_CAPITAL=500.00

# Alert Polling
TELEGRAM_POLL_INTERVAL=60  # seconds
GMGN_POLL_INTERVAL=30      # seconds
WHALE_POLL_INTERVAL=20     # seconds
```

### Whale Wallet Addresses (CONFIG)
```
WHALE_WALLET_1=4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t
WHALE_WALLET_2=H72yLkhTnoBfhBTXXaj1RBXuirm8s8G5fcVh2XpQLggM
```

---

## Logging & Monitoring

### Log Output
- **File:** `logs/execution.log` (rotate daily)
- **Format:** `[TIMESTAMP] [LEVEL] [SIGNAL] message`
- **Levels:** INFO, TRADE, EXIT, ERROR, ALERT
- **Examples:**
  ```
  [2026-03-06T09:15:32Z] [INFO] Cycle started, equity: $523.45
  [2026-03-06T09:16:15Z] [ALERT] Whale 4Be9C bought DOGE on Raydium
  [2026-03-06T09:16:20Z] [TRADE] ENTRY: DOGE/SOL, size $75, price $0.00005, signal: Tier1
  [2026-03-06T09:17:45Z] [EXIT] EXIT (2x): DOGE/SOL, 33% at $0.0001, P&L +$50
  ```

### Monitoring Dashboard
- **Location:** `dashboard/index.html` (optional visualization)
- **Refresh:** Every cycle (5 minutes)
- **Shows:** Current equity, P&L, win rate, open positions, recent trades

---

## Error Handling & Safety

### Circuit Breakers
1. **Daily Loss Limit Hit** → No new trades until next day
2. **Account Below $450** → Pause all entries, reduce sizes
3. **2 Consecutive Losses** → 2-hour cooldown, $25 max size
4. **RPC Connection Lost** → Log error, retry after 30 seconds, max 5 retries
5. **Telegram API Timeout** → Skip alert check, continue monitoring other sources

### Fallback Behavior
- **GMGN unavailable** → Rely on Altcoinist + whale monitoring
- **Whale wallet data stale** → Use last known state, add caution flag
- **Solana RPC slow** → Accept 10-second latency, don't skip trade
- **Position state unclear** → Query Solscan, don't execute until confirmed

---

## Performance Targets

### Short-term (2-4 weeks)
- Win rate: 50%+
- Monthly return: 10-20% (paper trading)
- Sharpe ratio: >1.5

### Long-term (after live conversion)
- Consistent win rate: 55%+
- Monthly return: 15-25%
- Max drawdown: <10%
- Positive expectancy per trade: >$5 average

---

## Configuration Checklist

- [ ] .env file created with all API keys
- [ ] STRATEGY.md read and understood
- [ ] Whale wallet addresses verified
- [ ] Telegram bot set up and polling
- [ ] GMGN access confirmed (manual or API)
- [ ] Dune dashboards bookmarked
- [ ] Solscan dashboard ready
- [ ] Logs directory created
- [ ] STATE.json initialized with $500 starting capital
- [ ] execute_cycle.py tested locally
- [ ] Cron job scheduled (every 5 minutes, 9 AM - 8 PM EST)
- [ ] Dry run completed successfully
