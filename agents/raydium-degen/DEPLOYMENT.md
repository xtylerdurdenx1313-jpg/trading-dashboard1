# 🚀 Deployment Guide — Raydium Degen Trading Agent

**Agent Ready:** ✅ Complete, tested, production-ready  
**Start Date:** 2026-03-06  
**Mode:** Paper trading ($500 starting capital)  
**Status:** Awaiting API key configuration and cron setup

---

## ⚡ 5-Minute Quick Start

### Step 1: Configure Environment (2 minutes)

```bash
cd /Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen

# Copy template to .env
cp .env.template .env

# Edit with your API keys
nano .env
```

**Minimum required keys:**
- `TELEGRAM_BOT_TOKEN` — Get from @BotFather
- `TELEGRAM_CHAT_ID` — Your Telegram user ID
- `SOLANA_RPC_ENDPOINT` — Already set to free public RPC

### Step 2: Test Execution (1 minute)

```bash
# Run a test cycle
./run.sh run

# Should output:
# [CYCLE] Starting execution cycle. Equity: $500.00
# [INFO] Checking Altcoinist alerts...
# [CYCLE] Complete. Open positions: 0
```

### Step 3: Check Status (1 minute)

```bash
# View account state
./run.sh status

# Should show:
# Equity: $500.00
# Total P&L: $0.00
# Win Rate: 0.0% (0/0)
```

### Step 4: Enable Auto-Run (1 minute)

```bash
# Add to crontab for every 5 minutes, 9 AM - 8 PM EST
crontab -e

# Add this line:
*/5 9-20 * * * cd /Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen && ./run.sh run >> logs/cron.log 2>&1
```

**Done!** Agent is now running autonomously.

---

## 📋 Full Deployment Checklist

- [ ] **Environment Setup**
  - [ ] Copy .env.template → .env
  - [ ] Edit .env with API keys
  - [ ] Verify no hardcoded secrets in Python files
  
- [ ] **API Keys (Required)**
  - [ ] TELEGRAM_BOT_TOKEN (from @BotFather)
  - [ ] TELEGRAM_CHAT_ID (your Telegram ID)
  - [ ] Optional: SOLANA_RPC_ENDPOINT (use paid RPC for production)
  - [ ] Optional: DUNE_API_KEY, GMGN_API_KEY
  
- [ ] **Testing**
  - [ ] `./run.sh test` — Verify Python environment
  - [ ] `./run.sh run` — Test one execution cycle
  - [ ] Check STATE.json created successfully
  - [ ] Check logs/execution.log has no errors
  
- [ ] **Monitoring Setup**
  - [ ] Logs directory created: ✅ (auto-created)
  - [ ] Review logs/execution.log output
  - [ ] Set up daily summary checks (optional)
  
- [ ] **Schedule**
  - [ ] Add cron job for every 5 minutes
  - [ ] Hours: 9 AM - 8 PM EST (adjust if needed)
  - [ ] Timezone: America/New_York
  - [ ] Redirect output to logs/cron.log
  
- [ ] **First 24 Hours**
  - [ ] Monitor logs for any errors
  - [ ] Verify STATE.json updates every 5 minutes
  - [ ] Check for any missed alerts
  - [ ] Adjust position sizing if needed
  
- [ ] **Before Live Trading**
  - [ ] Run paper trading for 2-4 weeks minimum
  - [ ] Achieve >50% win rate consistently
  - [ ] Document all trade logic for auditing
  - [ ] Review STRATEGY.md and confirm understanding
  - [ ] Get approval from Tyler before switching to live

---

## 🔌 API Key Sources

### Telegram Bot Token
1. Open Telegram, find @BotFather
2. Send `/newbot`
3. Follow prompts to create bot
4. Copy the token (looks like `123456789:ABCDEfgh...`)
5. Paste into .env: `TELEGRAM_BOT_TOKEN=your_token_here`

### Your Telegram Chat ID
1. Start a chat with your new bot (send any message)
2. Open @userinfobot in Telegram
3. Forward a message from your bot
4. @userinfobot will show your ID
5. Paste into .env: `TELEGRAM_CHAT_ID=your_id_here`

### Solana RPC (Optional)
Default public RPC is included: `https://api.mainnet-beta.solana.com`

For better performance, upgrade to paid RPC:
- **Quicknode:** https://www.quicknode.com/
- **Helius:** https://helius.dev/
- **Alchemy:** https://www.alchemy.com/

### Dune API Key (Optional)
1. Go to dune.com
2. Sign up or log in
3. Go to Settings → API
4. Copy your API key
5. Paste into .env: `DUNE_API_KEY=your_key_here`

---

## 🧪 Testing Modes

### Dry-Run (Evaluate signals, no execution)
```bash
# Edit .env
DRY_RUN=true

# Run cycles without executing trades
./run.sh run

# Useful for: Testing signal detection without risking capital
```

### Debug Mode (Verbose logging)
```bash
# Edit .env
DEBUG=true

# Run with detailed output
./run.sh run

# Check logs/execution.log for verbose trace
# Useful for: Troubleshooting, signal analysis
```

### Manual Cycle Testing
```bash
# Run a single cycle manually
python3 execute_cycle.py

# Check logs
tail -50 logs/execution.log

# View state
cat STATE.json | jq '.account'
```

---

## 📊 Monitoring Daily

### Quick Status Check
```bash
# Run every morning
./run.sh status

# Shows: Equity, P&L, win rate, open positions
```

### Review Trades
```bash
# View all trades logged
cat TRADES.md

# Filter by status
grep -E "Status|P&L|Win" TRADES.md
```

### Check Equity
```bash
# View current balance
jq '.account.current_equity' STATE.json

# View daily P&L
jq '.daily_metrics.daily_pnl' STATE.json
```

### Live Log Monitoring
```bash
# Watch logs in real-time during market hours
./run.sh logs

# Or manually:
tail -f logs/execution.log
```

---

## ⚠️ Important Warnings

### Account Protection
- **Account Floor:** Agent pauses trades if equity drops below $450
- **Daily Loss Cap:** Stops trading after -$25 loss per day
- **Hard Stop Loss:** Exits positions at -20% (non-negotiable)
- **Cooldown:** 2-hour pause after 2 consecutive losses

### Before Going Live
1. **Paper trade for 2-4 weeks minimum**
2. **Achieve >50% win rate consistently**
3. **Verify all signal sources working reliably**
4. **Audit entry/exit logic for accuracy**
5. **Get explicit approval before switching mode**

### Risk Management
- Never exceed position sizing rules
- Always use hard stop losses
- Monitor daily loss accumulation
- Review STRATEGY.md before making changes
- Keep logs backed up regularly

---

## 🐛 Troubleshooting

### "SyntaxError in execute_cycle.py"
→ Python version incompatible. Use Python 3.8+
```bash
python3 --version
```

### "ImportError: No module named 'requests'"
→ Optional dependency. Agent works without it.
→ Install if needed: `pip3 install requests`

### ".env not found"
→ Agent auto-creates from .env.template
→ If not, manually copy: `cp .env.template .env`

### "Cron job not running"
→ Verify cron entry: `crontab -l`
→ Check permissions: `ls -la run.sh` (should show x)
→ Check logs: `tail logs/cron.log`

### "Equity not updating"
→ Check STATE.json permissions
→ Verify logs/execution.log for errors
→ Manual test: `python3 execute_cycle.py`

---

## 📈 Success Metrics (First 2-4 Weeks)

### Target Benchmarks
- **Win Rate:** >50% (break-even threshold)
- **Monthly Return:** 10-20% (paper trading)
- **Sharpe Ratio:** >1.5 (risk-adjusted)
- **Max Drawdown:** <10% (portfolio stability)
- **Consistency:** Wins in 3+ out of 4 weeks

### Review Schedule
- **Daily:** Check equity and P&L
- **Weekly:** Analyze win rate and average win/loss
- **Bi-weekly:** Review signal reliability
- **Monthly:** Comprehensive strategy review

### Adjustment Triggers
- Win rate <40% → Audit signal accuracy
- Consecutive losses >3 → Increase cooldown period
- Account below $475 → Reduce position sizing
- Whale wallet performance degrades → Replace with new wallet

---

## 🎯 Next Steps After Setup

1. **Day 1:** Run agent, monitor first 5-10 cycles
2. **Days 2-7:** Collect data, analyze signal quality
3. **Weeks 2-4:** Run full paper trading period, measure performance
4. **Month 2:** If >50% win rate, request live approval from Tyler
5. **Live Switch:** Use `switch_to_live()` function (when approved)

---

## 📞 Support References

- **Strategy Questions:** See STRATEGY.md (entry/exit rules)
- **Configuration Questions:** See CONFIG.md (APIs, limits, parameters)
- **Execution Questions:** See execute_cycle.py (code comments)
- **Troubleshooting:** See README.md (FAQ section)

---

## ✅ Final Verification

Before declaring "ready to deploy," verify:

```bash
cd /Users/tylerxdurden/.openclaw/workspace/agents/raydium-degen

# Check all files exist
ls -la AGENT.md STRATEGY.md CONFIG.md TRADES.md STATE.json execute_cycle.py run.sh

# Check Python syntax
python3 -m py_compile execute_cycle.py

# Check logs directory exists
mkdir -p logs && ls -la logs

# Test execution
./run.sh test

# Test one cycle
./run.sh run

# Verify STATE.json updated
cat STATE.json | jq '.account.last_updated'
```

All green? 🟢 **Agent is ready to deploy!**

---

**Deployment Date:** 2026-03-06  
**Agent Status:** ✅ READY FOR PRODUCTION  
**Mode:** Paper Trading ($500 capital)  
**Next Action:** Configure .env and enable cron job  
