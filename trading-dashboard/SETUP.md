# Trading Dashboard Setup Guide

## Architecture

```
Your Mac (Local)
├── API Server (Node.js on :3001)
│   └── Reads: agents/*/STATE.json
└── Ngrok Tunnel (exposes API publicly)
    └── https://your-url.ngrok.io

Vercel (Cloud)
└── Dashboard (Next.js)
    └── Calls API via tunnel
```

---

## Step 1: Start Local API Server

```bash
cd ~/.openclaw/workspace/trading-dashboard
node server.js
```

You should see:
```
🚀 Trading API Server running on http://localhost:3001
📊 GET http://localhost:3001/api/agents
```

Test it works:
```bash
curl http://localhost:3001/api/agents
```

---

## Step 2: Install & Run Ngrok

### Option A: Brew (macOS)
```bash
brew install ngrok
ngrok authtoken YOUR_AUTH_TOKEN
```

Get your auth token: https://dashboard.ngrok.com/auth

### Option B: Direct Download
Download from: https://ngrok.com/download

---

## Step 3: Expose API with Ngrok

While API server is running:

```bash
ngrok http 3001
```

You'll see:
```
Forwarding   https://abc123def456.ngrok.io -> http://localhost:3001
```

**Copy that URL** — you'll need it for Vercel.

---

## Step 4: Deploy Dashboard to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier is fine)

### Steps

1. **Initialize git repo:**
   ```bash
   cd ~/.openclaw/workspace/trading-dashboard
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/trading-dashboard.git
   git branch -M main
   git push -u origin main
   ```

3. **Connect to Vercel:**
   - Go to https://vercel.com/new
   - Import your GitHub repo
   - Vercel will auto-detect Next.js

4. **Add Environment Variables:**
   In Vercel dashboard, go to Settings → Environment Variables and add:

   ```
   NEXT_PUBLIC_DASHBOARD_PASSWORD = TylerTrading2026!
   NEXT_PUBLIC_API_URL = https://abc123def456.ngrok.io
   ```

   (Replace with your actual Ngrok URL)

5. **Deploy!**
   Click "Deploy" — Vercel handles the rest.

---

## Keeping It Running

You need TWO processes always running:

**Process 1: API Server (keep terminal open)**
```bash
cd ~/.openclaw/workspace/trading-dashboard
node server.js
```

**Process 2: Ngrok Tunnel (separate terminal)**
```bash
ngrok http 3001
```

### Option: Run as Background Services

**Using tmux:**
```bash
# Terminal 1
tmux new-session -d -s api "cd ~/.openclaw/workspace/trading-dashboard && node server.js"

# Terminal 2
tmux new-session -d -s ngrok "ngrok http 3001"

# Later, to check:
tmux ls
tmux attach -t api  # or -t ngrok
```

**Using launchd (auto-start on Mac boot):**
Create `~/Library/LaunchAgents/com.trading.api.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.trading.api</string>
    <key>Program</key>
    <string>/usr/local/bin/node</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/tylerxdurden/.openclaw/workspace/trading-dashboard/server.js</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then:
```bash
launchctl load ~/Library/LaunchAgents/com.trading.api.plist
```

---

## Testing

1. **Local:** http://localhost:3000 (password: TylerTrading2026!)
2. **Remote:** https://your-vercel-app.vercel.app (same password)

Both should show your agents' live data, refreshing every 5 seconds.

---

## Troubleshooting

**"API connection refused"**
- Make sure `node server.js` is running
- Check Ngrok URL is correct in Vercel env vars

**"Dashboard shows OFFLINE"**
- API server might not have access to agent files
- Check permissions: `ls -la ~/.openclaw/workspace/agents/`

**Ngrok URL keeps changing**
- Free tier resets on restart
- Get a paid Ngrok account ($5/mo) to lock in a static URL

---

## Security Notes

- API is public (via Ngrok), but dashboard password-protects the UI
- API only exposes public metrics (no credentials)
- Don't commit `.env.local` to git (already in `.gitignore`)

---

Next: Get those API keys and fire up Hyperliquid! 🚀
