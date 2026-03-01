const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const AGENTS_DIR = path.join(process.env.HOME, '.openclaw/workspace/agents');
const PORT = process.env.PORT || 3001;

const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  if (pathname === '/api/agents') {
    try {
      const agents = [];

      // Polymarket Trader
      try {
        const polyPath = path.join(AGENTS_DIR, 'polymarket-trader/STATE.json');
        const polyData = JSON.parse(fs.readFileSync(polyPath, 'utf-8'));
        agents.push({
          name: 'Polymarket Trader',
          status: 'OPERATIONAL',
          equity: polyData.account?.equity || 0,
          pnl: polyData.account?.pnl || 0,
          positions: polyData.positions?.length || 0,
          lastUpdate: new Date(polyData.last_updated || Date.now()).toLocaleString(),
        });
      } catch (error) {
        agents.push({
          name: 'Polymarket Trader',
          status: 'OFFLINE',
          equity: 0,
          pnl: 0,
          positions: 0,
          lastUpdate: 'N/A',
        });
      }

      // Hyperliquid Solana (when available)
      try {
        const hyperPath = path.join(AGENTS_DIR, 'hyperliquid-solana/STATE.json');
        const hyperData = JSON.parse(fs.readFileSync(hyperPath, 'utf-8'));
        agents.push({
          name: 'Hyperliquid Solana',
          status: 'OPERATIONAL',
          equity: hyperData.account?.equity || 0,
          pnl: hyperData.account?.pnl || 0,
          positions: hyperData.positions?.length || 0,
          lastUpdate: new Date(hyperData.last_updated || Date.now()).toLocaleString(),
        });
      } catch (error) {
        // Hyperliquid not set up yet
      }

      res.writeHead(200);
      res.end(JSON.stringify(agents));
    } catch (error) {
      console.error('Error:', error);
      res.writeHead(500);
      res.end(JSON.stringify({ error: 'Failed to fetch agents' }));
    }
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, () => {
  console.log(`🚀 Trading API Server running on http://localhost:${PORT}`);
  console.log(`📊 GET http://localhost:${PORT}/api/agents`);
});
