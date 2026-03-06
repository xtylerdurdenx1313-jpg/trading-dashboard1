'use client'

import { useEffect, useState } from 'react'

interface AgentStatus {
  name: string
  status: string
  equity: number
  pnl: number
  positions: number
  lastUpdate: string
}

export default function Dashboard() {
  const [agents, setAgents] = useState<AgentStatus[]>([
    {
      name: 'Polybit (15m Bitcoin)',
      status: 'OFFLINE',
      equity: 0,
      pnl: 0,
      positions: 0,
      lastUpdate: 'Loading...',
    },
    {
      name: 'Prophet-Copier',
      status: 'OFFLINE',
      equity: 0,
      pnl: 0,
      positions: 0,
      lastUpdate: 'Loading...',
    },
    {
      name: 'Prophet (Meta)',
      status: 'OFFLINE',
      equity: 0,
      pnl: 0,
      positions: 0,
      lastUpdate: 'Loading...',
    },
    {
      name: 'HyperSOL (Solana)',
      status: 'OFFLINE',
      equity: 0,
      pnl: 0,
      positions: 0,
      lastUpdate: 'Loading...',
    },
    {
      name: 'Raydium Degen',
      status: 'OPERATIONAL',
      equity: 500,
      pnl: 0,
      positions: 0,
      lastUpdate: new Date().toLocaleString(),
    },
  ])
  const [loading, setLoading] = useState(true)
  const [authenticated, setAuthenticated] = useState(false)
  const [password, setPassword] = useState('')
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    const auth = localStorage.getItem('dashboard_auth')
    if (auth === 'true') {
      setAuthenticated(true)
      fetchAgents()
    }
    setLoading(false)
  }, [])

  const fetchAgents = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'
      const res = await fetch(`${apiUrl}/api/agents`)
      if (!res.ok) throw new Error('API failed')
      let data = await res.json()
      
      // Ensure Raydium Degen is always in the list
      const hasRaydium = data.some((a: AgentStatus) => a.name === 'Raydium Degen')
      if (!hasRaydium) {
        data = [
          ...data,
          {
            name: 'Raydium Degen',
            status: 'OPERATIONAL',
            equity: 500,
            pnl: 0,
            positions: 0,
            lastUpdate: new Date().toLocaleString(),
          }
        ]
      }
      setAgents(data)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Failed to fetch agents:', error)
    }
  }

  useEffect(() => {
    if (authenticated) {
      const interval = setInterval(fetchAgents, 5000)
      return () => clearInterval(interval)
    }
  }, [authenticated])

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (password === process.env.NEXT_PUBLIC_DASHBOARD_PASSWORD) {
      localStorage.setItem('dashboard_auth', 'true')
      setAuthenticated(true)
      fetchAgents()
    } else {
      alert('Incorrect password')
    }
  }

  // Calculate portfolio metrics
  const totalEquity = agents.reduce((sum, agent) => sum + agent.equity, 0)
  const totalPnL = agents.reduce((sum, agent) => sum + agent.pnl, 0)
  const totalPositions = agents.reduce((sum, agent) => sum + agent.positions, 0)
  const pnlPercent = totalEquity > 0 ? ((totalPnL / totalEquity) * 100).toFixed(2) : '0.00'

  if (!authenticated) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="absolute inset-0 opacity-30 pointer-events-none">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600 rounded-full mix-blend-screen filter blur-3xl"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600 rounded-full mix-blend-screen filter blur-3xl"></div>
        </div>
        <form
          onSubmit={handleLogin}
          className="relative bg-gray-950 border border-gray-800 p-12 rounded-2xl shadow-2xl w-full max-w-md backdrop-blur-xl z-10"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Command Center
          </h1>
          <p className="text-gray-400 mb-8">Trading Operations</p>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
            className="w-full px-4 py-3 rounded-lg bg-gray-900 text-white placeholder-gray-600 border border-gray-700 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30 mb-6"
          />
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 rounded-lg transition shadow-lg"
          >
            Access
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Background gradients */}
      <div className="fixed inset-0 opacity-20 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600 rounded-full mix-blend-screen filter blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600 rounded-full mix-blend-screen filter blur-3xl"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-gray-800 bg-black/50 backdrop-blur-xl sticky top-0">
        <div className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center font-bold text-xl">
              ⚡
            </div>
            <h1 className="text-2xl font-bold">Trading Command Center</h1>
          </div>
          <button
            onClick={() => {
              localStorage.removeItem('dashboard_auth')
              setAuthenticated(false)
              setPassword('')
            }}
            className="px-6 py-2 text-gray-400 hover:text-white hover:bg-gray-900 rounded-lg transition text-sm font-medium border border-gray-800"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main content */}
      <div className="relative z-10 max-w-7xl mx-auto px-8 py-12">
        {/* Portfolio Summary */}
        <div className="mb-12">
          <h2 className="text-4xl font-bold mb-8">Portfolio Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Total Equity */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-xl p-6 hover:border-blue-600/50 transition group">
              <p className="text-gray-500 text-xs font-semibold mb-2 uppercase tracking-widest">Total Equity</p>
              <p className="text-4xl font-bold text-white mb-1">${totalEquity.toFixed(2)}</p>
              <p className="text-gray-400 text-sm">{agents.length} agents running</p>
            </div>

            {/* Total P&L */}
            <div className={`rounded-xl p-6 border transition group ${
              totalPnL >= 0
                ? 'bg-gradient-to-br from-emerald-900/20 to-emerald-950/20 border-emerald-700/50 hover:border-emerald-600'
                : 'bg-gradient-to-br from-red-900/20 to-red-950/20 border-red-700/50 hover:border-red-600'
            }`}>
              <p className={`text-xs font-semibold mb-2 uppercase tracking-widest ${
                totalPnL >= 0 ? 'text-emerald-400' : 'text-red-400'
              }`}>
                Unrealized P&L
              </p>
              <p className={`text-4xl font-bold mb-1 ${
                totalPnL >= 0 ? 'text-emerald-400' : 'text-red-400'
              }`}>
                {totalPnL >= 0 ? '+' : ''}${totalPnL.toFixed(2)}
              </p>
              <p className={`text-sm ${totalPnL >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {pnlPercent}% return
              </p>
            </div>

            {/* Total Positions */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-xl p-6 hover:border-purple-600/50 transition group">
              <p className="text-gray-500 text-xs font-semibold mb-2 uppercase tracking-widest">Open Positions</p>
              <p className="text-4xl font-bold text-white mb-1">{totalPositions}</p>
              <p className="text-gray-400 text-sm">{totalPositions === 0 ? 'Ready to trade' : `Active trades`}</p>
            </div>

            {/* Last Update */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition group">
              <p className="text-gray-500 text-xs font-semibold mb-2 uppercase tracking-widest">Last Sync</p>
              <p className="text-2xl font-bold text-white mb-1">{lastUpdate.toLocaleTimeString()}</p>
              <p className="text-gray-400 text-sm">Updates every 5s</p>
            </div>
          </div>
        </div>

        {/* Trading Agents */}
        <div>
          <h2 className="text-4xl font-bold mb-8">Trading Agents</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className="group bg-gradient-to-br from-gray-900 to-gray-950 border border-gray-800 rounded-xl p-6 hover:border-blue-600/50 transition duration-300 hover:shadow-xl hover:shadow-blue-500/10"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition mb-1">
                      {agent.name}
                    </h3>
                    <p className="text-gray-500 text-xs">
                      {new Date(agent.lastUpdate).toLocaleTimeString()}
                    </p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center space-x-1 ${
                    agent.status === 'OPERATIONAL'
                      ? 'bg-emerald-900/50 text-emerald-400 border border-emerald-700/50'
                      : 'bg-gray-800 text-gray-400 border border-gray-700'
                  }`}>
                    <span className={`w-2 h-2 rounded-full ${
                      agent.status === 'OPERATIONAL' ? 'bg-emerald-400 animate-pulse' : 'bg-gray-600'
                    }`}></span>
                    <span>{agent.status}</span>
                  </div>
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                  {/* Equity */}
                  <div className="bg-gray-950/50 rounded-lg p-3 border border-gray-800 group-hover:border-gray-700 transition">
                    <p className="text-gray-500 text-xs font-semibold mb-1 uppercase tracking-wider">Equity</p>
                    <p className="text-2xl font-bold text-white">${agent.equity.toFixed(2)}</p>
                  </div>

                  {/* P&L */}
                  <div className={`rounded-lg p-3 border transition ${
                    agent.pnl >= 0
                      ? 'bg-emerald-900/20 border-emerald-700/50'
                      : 'bg-red-900/20 border-red-700/50'
                  }`}>
                    <p className={`text-xs font-semibold mb-1 uppercase tracking-wider ${
                      agent.pnl >= 0 ? 'text-emerald-400' : 'text-red-400'
                    }`}>
                      P&L
                    </p>
                    <p className={`text-2xl font-bold ${
                      agent.pnl >= 0 ? 'text-emerald-400' : 'text-red-400'
                    }`}>
                      {agent.pnl >= 0 ? '+' : ''}${agent.pnl.toFixed(2)}
                    </p>
                  </div>
                </div>

                {/* Positions */}
                <div className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-lg p-3 border border-blue-700/30 group-hover:border-blue-600 transition">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-blue-400 text-xs font-semibold uppercase tracking-wider">Positions</p>
                      <p className="text-3xl font-bold text-blue-300">{agent.positions}</p>
                    </div>
                    <div className="text-4xl opacity-50 group-hover:opacity-100 transition">📊</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-gray-500 text-sm border-t border-gray-800 pt-8">
          <p>Real-time trading operations • Syncing every 5 seconds • {agents.filter(a => a.status === 'OPERATIONAL').length} operational agents</p>
        </div>
      </div>
    </div>
  )
}
