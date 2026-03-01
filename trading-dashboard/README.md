# Trading Command Center

A real-time monitoring dashboard for your trading agents (Polymarket, Hyperliquid, etc.).

## Features

- **Live Agent Monitoring** — View equity, P&L, positions, and status for all agents
- **Private Access** — Password-protected dashboard
- **Real-time Updates** — Auto-refresh every 5 seconds
- **Multi-Agent Support** — Scales with your trading fleet

## Setup

1. Install dependencies:
```bash
npm install
```

2. Update `.env.local` with your dashboard password:
```
NEXT_PUBLIC_DASHBOARD_PASSWORD=YourPasswordHere
```

3. Run locally:
```bash
npm run dev
```

Open http://localhost:3000 and log in.

## Deployment to Vercel

1. Push this repo to GitHub
2. Connect to Vercel via [vercel.com](https://vercel.com)
3. Vercel will auto-detect Next.js
4. Add environment variable `NEXT_PUBLIC_DASHBOARD_PASSWORD` in Vercel settings
5. Deploy

## Data Sources

The dashboard reads from your local agent state files:
- `/agents/polymarket-trader/STATE.json`
- `/agents/hyperliquid-solana/STATE.json` (when available)

## Security

- Dashboard password protected
- Credentials NOT stored in browser
- API routes only expose safe metrics (no API keys or secrets)
