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
    const agentsDir = join(process.cwd(), '..', 'agents')

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

    // Polybit
    try {
      const polybitState = await fs.readFile(
        join(agentsDir, 'polybit/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(polybitState)
      agents.push({
        name: 'Polybit',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'Polybit',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    // Prophet Copier
    try {
      const prophetCopierState = await fs.readFile(
        join(agentsDir, 'prophet-copier/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(prophetCopierState)
      agents.push({
        name: 'Prophet Copier',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'Prophet Copier',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    // Polymarket Meta
    try {
      const polymarketMetaState = await fs.readFile(
        join(agentsDir, 'polymarket-meta/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(polymarketMetaState)
      agents.push({
        name: 'Polymarket Meta',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'Polymarket Meta',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    // Hyperliquid Solana (HyperSOL)
    try {
      const hyperliquidState = await fs.readFile(
        join(agentsDir, 'hyperliquid-solana/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(hyperliquidState)
      agents.push({
        name: 'HyperSOL',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'HyperSOL',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    // Raydium Degen
    try {
      const raydiumState = await fs.readFile(
        join(agentsDir, 'raydium-degen/STATE.json'),
        'utf-8'
      )
      const data: State = JSON.parse(raydiumState)
      agents.push({
        name: 'Raydium Degen',
        status: 'OPERATIONAL',
        equity: data.account?.equity || 0,
        pnl: data.account?.pnl || 0,
        positions: data.positions?.length || 0,
        lastUpdate: new Date(data.last_updated || Date.now()).toLocaleString(),
      })
    } catch (error) {
      agents.push({
        name: 'Raydium Degen',
        status: 'OFFLINE',
        equity: 0,
        pnl: 0,
        positions: 0,
        lastUpdate: 'N/A',
      })
    }

    return Response.json(agents)
  } catch (error) {
    console.error('API Error:', error)
    return Response.json({ error: 'Failed to fetch agents' }, { status: 500 })
  }
}
