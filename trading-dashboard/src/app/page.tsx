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
  const [agents, setAgents] = useState<AgentStatus[]>([])
  const [loading, setLoading] = useState(true)
  const [authenticated, setAuthenticated] = useState(false)
  const [password, setPassword] = useState('')

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
      const data = await res.json()
      setAgents(data)
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

  if (!authenticated) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <form
          onSubmit={handleLogin}
          className="bg-slate-800 p-8 rounded-lg shadow-lg w-96"
        >
          <h1 className="text-3xl font-bold text-white mb-6">
            Trading Command Center
          </h1>
          <input
            type="password"
            placeholder="Enter dashboard password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 rounded bg-slate-700 text-white placeholder-slate-400 mb-4"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded"
          >
            Login
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Trading Command Center</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {agents.map((agent) => (
            <div
              key={agent.name}
              className="bg-slate-800 rounded-lg p-6 border border-slate-700"
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold">{agent.name}</h2>
                <span
                  className={`px-3 py-1 rounded text-sm ${
                    agent.status === 'OPERATIONAL'
                      ? 'bg-green-900 text-green-200'
                      : 'bg-red-900 text-red-200'
                  }`}
                >
                  {agent.status}
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Equity:</span>
                  <span className="font-mono text-lg">${agent.equity.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">P&L:</span>
                  <span
                    className={`font-mono text-lg ${
                      agent.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}
                  >
                    {agent.pnl >= 0 ? '+' : ''}${agent.pnl.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Open Positions:</span>
                  <span className="font-mono text-lg">{agent.positions}</span>
                </div>
                <div className="flex justify-between text-xs text-slate-500">
                  <span>Last Update:</span>
                  <span>{agent.lastUpdate}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 text-slate-500 text-sm">
          <p>Dashboard auto-refreshes every 5 seconds</p>
        </div>
      </div>
    </div>
  )
}
