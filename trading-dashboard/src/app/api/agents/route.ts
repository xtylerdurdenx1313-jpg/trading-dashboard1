import { promises as fs } from 'fs'
import { join } from 'path'

interface State {
  account?: {
    balance?: number
    equity?: number
    pnl?: number
  }
  positions?: Array<{ status: string }>
  last_updated?: string
}

export async function GET() {
  try {
    const agentsDir = join(
      process.env.HOME || '/root',
      '.openclaw/workspace/agents'
    )

    const agents = []

    // Polymarket Trader
    try {
      const polymarketState = await fs.readFile(
        join(agentsDir, 'polymarket-trader/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(polymarketState)
      agents.push({
        name: 'Polymarket Trader',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'Polymarket Trader',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    // Hyperliquid Solana (when available)
    try {
      const hyperliquidState = await fs.readFile(
        join(agentsDir, 'hyperliquid-solana/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(hyperliquidState)
      agents.push({
        name: 'Hyperliquid Solana',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      // Hyperliquid not set up yet
    }

    return Response.json(agents)
  } catch (error) {
    console.error('API Error:', error)
    return Response.json({ error: 'Failed to fetch agents' }, { status: 500 })
  }
}
