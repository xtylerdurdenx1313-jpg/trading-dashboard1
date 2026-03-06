# 🚀 Raydium Degen Trading Agent

A production-ready paper trading bot for SOL-based token launches on Raydium and Pump.fun.

**Status:** 🟢 Ready for deployment  
**Mode:** Paper trading ($500 starting capital)  
**Strategy:** Whale mirroring + on-chain signals + Altcoinist alerts  
**Spawn Frequency:** Every 5 minutes (9 AM - 8 PM EST)

---

## 📋 Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys
nano .env

# Required keys:
# - TELEGRAM_BOT_TOKEN (from @BotFather)
# - TELEGRAM_CHAT_ID (your Telegram ID)
# - SOLANA_RPC_ENDPOINT (already set to public default)
```

### 2. Create Logs Directory

```bash
mkdir -p logs
```

### 3. Initialize State

The agent auto-initializes `STATE.json` on first run with $500 starting capital.

### 4. Run a Test Cycle

```bash
# Run one execution cycle (manual test)
python3 execute_cycle.py

# Should log:
# [CYCLE] Starting execution cycle. Equity: $500.00
# [INFO] Checking Altcoinist alerts...
# [INFO] Scanning GMGN for new launches...
# [CYCLE] Complete. Open positions: 0
```

### 5. Enable Auto-Spawn (Production)

Add cron job to run every 5 minutes, 9 AM - 8 PM EST:

```bash
# Edit crontab
crontab -e

# Add this line:
# */5 9-20 * * * cd /Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen && python3 execute_cycle.py >> logs/cron.log 2>&1

# Or use OpenClaw cron scheduling:
# openclaw cron create "raydium-cycle" --interval "5 minutes" --hours "9-20" --tz "America/New_York" --command "python3 execute_cycle.py"
```

---

## 📁 File Guide

| File | Purpose |
|------|---------|
| **AGENT.md** | Agent overview and mission |
| **STRATEGY.md** | Complete trading strategy (entry/exit rules) |
| **CONFIG.md** | Operational configuration and data sources |
| **TRADES.md** | Trade log (append-only, append trades here) |
| **STATE.json** | Live account state (equity, P&L, open positions) |
| **execute_cycle.py** | Main execution script (spawned every 5 min) |
| **.env** | API keys and environment variables |
| **.env.template** | Environment template (copy to .env) |
| **logs/execution.log** | All cycle logs (auto-rotated) |
| **README.md** | This file |

---

## 🎯 How It Works

### Execution Cycle (Every 5 Minutes)

```
START
  ├─ Check Telegram @altcoinist_trenchbot for alerts
  ├─ Scan GMGN.ai for new launches + first 70 buyers
  ├─ Monitor whale wallet activity (2 addresses)
  ├─ Evaluate entry signals (Tier 1-4)
  ├─ Enter new trades if signals + risk checks pass
  ├─ Check exit conditions (targets hit, timeout expired)
  ├─ Close positions if exits triggered
  ├─ Update STATE.json (equity, P&L, metrics)
  └─ Log all actions to logs/execution.log
SLEEP 5 MINUTES
```

### Entry Signals (Priority Order)

1. **Tier 1 (Highest):** Whale wallet detected buying on Raydium/Pump.fun
2. **Tier 2:** Altcoinist @altcoinist_trenchbot "FIRST 70 BUYER" alert
3. **Tier 3:** GMGN on-chain signals (first 70 buyer correlation)
4. **Tier 4:** Dune analytics patterns + holder analysis

### Exit Strategy

- **Tier 1 (2x):** Sell 33% of position → Bank initial gains
- **Tier 2 (5x):** Sell 33% of position → Capture mid-range upside
- **Tier 3 (10x):** Sell remaining 34% OR 4-hour timeout → Take profits or reset capital
- **Hard Stop:** -20% from entry (non-negotiable)
- **Daily Cap:** -$25 max loss per day
- **Cooldown:** 2-hour pause after 2 consecutive losses

---

## 💰 Trading Rules (IRON CLAD)

### Position Sizing
- **Normal:** $50 per trade
- **High Conviction:** $75-100 (multiple signals + whale correlation)
- **Scout/Low:** $25-50
- **After Loss:** $25 minimum during cooldown

### Risk Management
- **Hard Stop:** -20% (exit if price drops 20% from entry)
- **Daily Max Loss:** -$25 (stop all trading if hit)
- **Account Floor:** Never let equity drop below $450
- **2 Loss Cooldown:** Pause 2 hours, reduce size to $25

### Exit Rules
- **Never** hold past timeout (4 hours max)
- **Always** take profits at targets (don't be greedy)
- **Always** respect the hard stop loss
- **Always** log every exit with reasoning

---

## 📊 Monitoring

### Check Current State

```bash
# View account state
cat STATE.json | jq '.account'

# View open positions
cat STATE.json | jq '.positions'

# View today's P&L
cat STATE.json | jq '.daily_metrics'

# View trade log
cat TRADES.md
```

### View Logs

```bash
# Latest 50 lines
tail -50 logs/execution.log

# Watch live (follow mode)
tail -f logs/execution.log

# Search for specific token
grep "DOGE" logs/execution.log
```

### Daily Summary

After each day, STATE.json contains:
- Total equity
- Daily P&L
- Win rate %
- Consecutive losses
- Cooldown status

---

## 🐋 Whale Wallets

### Wallet 1: Conservative (4Be9Cv...)
- Profile: Known for 50x flips, patient holding
- Strategy: Low drawdown, highly selective
- **Action:** Follow immediately on buy, hold longer (up to 10x)

### Wallet 2: Aggressive (H72yLk...)
- Profile: High-volume plays, 5-20x targets
- Strategy: Fast entries/exits, frequent wins
- **Action:** Follow immediately on buy, exit at 5x (don't hold for 10x)

Monitor both via Solana blockchain RPC or Solscan.io explorer.

---

## 🔌 Data Sources

### Altcoinist Telegram (@altcoinist_trenchbot)
- Highest conviction alerts
- Real-time new launches
- Whale transaction notifications
- Free, manual polling via Telegram API

### GMGN.ai (gmgn.ai)
- First 70 buyer detection
- On-chain signal scoring
- Rug risk analysis
- Free web access, optional API

### Dune Analytics (dune.com)
- Raydium/Pump.fun dashboards
- Holder concentration tracking
- Dev wallet monitoring
- Free dashboard queries

### Solana RPC (api.mainnet-beta.solana.com)
- Real-time balance/transaction queries
- Free public endpoint (may have rate limits)
- For production: use paid RPC (Quicknode, Helius)

---

## ⚠️ Important Notes

### Paper Trading Limitations
- No real funds at risk (safe testing)
- Price slippage & liquidity not simulated (may differ from live)
- No realistic fees charged
- Good for strategy testing, not exact live performance prediction

### Before Going Live
1. Run paper trading for 2-4 weeks minimum
2. Achieve win rate >50% consistently
3. Verify whale wallet tracking accuracy
4. Audit entry/exit signal reliability
5. Test live with minimal capital ($100)
6. Scale only after confirmed profitability

### API Rate Limits
- Solana public RPC: ~100 req/sec (may be throttled)
- Telegram API: Standard rate limits
- GMGN: Unknown (check their docs)
- Solution: Use paid RPC for production

### Market Risk
- Token launch volatility is HIGH
- Rug pull risk is REAL
- Always verify tokens on Solscan
- Never trade contracts with suspicious holders
- Trust the GMGN risk scoring

---

## 🐛 Troubleshooting

### "STATE.json not found"
→ Script auto-initializes on first run. If not, check permissions:
```bash
chmod 755 /Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen
```

### "Telegram API timeout"
→ Check TELEGRAM_BOT_TOKEN in .env. Verify bot has message access.
→ Try manual test: `python3 -c "import requests; requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe')"`

### "Solana RPC connection refused"
→ Check internet. Public RPC may be rate-limited.
→ Switch to paid RPC (Quicknode, Helius) in .env

### "No trades executed"
→ Likely no alerts received. Check Telegram polling.
→ Manually test: Run `python3 execute_cycle.py` at 9 AM - 8 PM EST
→ Check GMGN.ai manually for new launches

### "Equity dropped below $450"
→ Account floor protection triggered. Trading paused.
→ Reduce position sizes, focus on winners, review STRATEGY.md

### "2 consecutive losses, cooldown active"
→ Expected behavior. Wait 2 hours before next trade.
→ Next trade size limited to $25. Resume normal after first win.

---

## 📈 Performance Targets

### Short-term (2-4 weeks, paper trading)
- Win rate: 50%+
- Monthly return: 10-20%
- Days active: 20+

### Long-term (after live conversion)
- Win rate: 55%+
- Monthly return: 15-25%
- Sharpe ratio: >1.5
- Max drawdown: <10%

---

## 📞 Support & Updates

### Files to Monitor
- **STRATEGY.md** — Update if signal rules change
- **CONFIG.md** — Update if API endpoints/keys change
- **execute_cycle.py** — Add new logic here

### Debugging
- Enable DEBUG=true in .env for verbose logging
- Use DRY_RUN=true to test without executing trades
- Check logs/execution.log for detailed trace

### Updating Strategy
1. Edit STRATEGY.md with new rules
2. Update execute_cycle.py logic
3. Test in dry-run mode
4. Monitor STATE.json for changes
5. Document in logs/execution.log

---

## 🔒 Security Notes

- **Never** hardcode API keys in execute_cycle.py
- **Always** use .env file for secrets
- **Never** commit .env to version control
- **Monitor** TELEGRAM_BOT_TOKEN usage (revoke if exposed)
- **Backup** STATE.json and TRADES.md regularly
- **Review** logs for suspicious activity

---

## 🚀 Deployment Checklist

- [ ] Copy .env.template to .env
- [ ] Fill in all required API keys
- [ ] Run `python3 execute_cycle.py` (test cycle)
- [ ] Verify STATE.json created with $500 capital
- [ ] Check logs/execution.log for no errors
- [ ] Set up cron job for every 5 minutes, 9 AM - 8 PM EST
- [ ] Monitor for 24+ hours for any issues
- [ ] Review TRADES.md for first trades
- [ ] Adjust position sizing if needed
- [ ] Ready to run autonomous trading

---

## 📝 Quick Commands

```bash
# Test a cycle
python3 execute_cycle.py

# View account state
jq '.account' STATE.json

# View today's P&L
jq '.daily_metrics' STATE.json

# View recent log lines
tail -20 logs/execution.log

# Search for specific token
grep -i "dogecoin" logs/execution.log

# Count total trades
grep -c "^\[TRADE\]" logs/execution.log

# Show win rate
jq '.trading.win_rate' STATE.json
```

---

## 📚 References

- **Strategy:** See STRATEGY.md (entry/exit rules)
- **Config:** See CONFIG.md (APIs, timeouts, limits)
- **Data Sources:** GMGN (gmgn.ai), Dune (dune.com), Solscan (solscan.io)
- **Whale Tracking:** Solscan.io address lookup
- **Alerts:** Telegram @altcoinist_trenchbot

---

**Last Updated:** 2026-03-06  
**Version:** 1.0 (Production Ready)  
**Mode:** Paper Trading ($500 capital)  

Ready to run. Good luck! 🎯
