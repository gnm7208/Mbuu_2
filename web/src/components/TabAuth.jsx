import React, { useState } from 'react'
import { postAuth } from '../utils/api'

export default function TabAuth({ onAuth }) {
  const [mode, setMode] = useState('login')
  const [error, setError] = useState(null)

  async function handleLogin(e) {
    e.preventDefault()
    const form = new FormData(e.target)
    const username = form.get('username')
    try {
      const data = await postAuth(username)
      if (data && data.role) {
        onAuth(data)
      } else {
        onAuth({ entered: username, role: 'guest' })
      }
    } catch (err) {
      setError(String(err))
    }
  }

  async function handleRegister(e) {
    e.preventDefault()
    const f = new FormData(e.target)
    const username = f.get('username')
    const email = f.get('email')
    const password = f.get('password')

    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      })
      const data = await res.json()
      if (res.ok) {
        onAuth(data)
      } else {
        setError(data.error || 'Registration failed')
      }
    } catch (err) {
      setError(String(err))
    }
  }

  return (
    <div className="border rounded p-4 bg-white dark:bg-slate-800">
      <div className="flex gap-2 mb-4">
        <button onClick={() => setMode('login')} className={`px-3 py-1 ${mode==='login'?'bg-blue-600 text-white rounded':''}`}>Login</button>
        <button onClick={() => setMode('register')} className={`px-3 py-1 ${mode==='register'?'bg-blue-600 text-white rounded':''}`}>Register</button>
      </div>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      {mode === 'login' ? (
        <form onSubmit={handleLogin} className="space-y-3">
          <input name="username" placeholder="Enter username" className="w-full p-2 border rounded" />
          <div className="flex justify-end">
            <button className="px-4 py-2 bg-blue-600 text-white rounded">Continue</button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleRegister} className="space-y-3">
          <input name="username" placeholder="Choose username" className="w-full p-2 border rounded" />
          <input name="email" placeholder="Email" className="w-full p-2 border rounded" />
          <input name="password" type="password" placeholder="Password" className="w-full p-2 border rounded" />
          <div className="flex justify-end">
            <button className="px-4 py-2 bg-green-600 text-white rounded">Register</button>
          </div>
        </form>
      )}
    </div>
  )
}
