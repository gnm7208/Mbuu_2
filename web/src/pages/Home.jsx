import React, { useState } from 'react'
import Buyer from './Buyer'
import Seller from './Seller'
import Header from '../components/Header'
import TabAuth from '../components/TabAuth'

export default function Home() {
  const [user, setUser] = useState(null)
  const [roleInfo, setRoleInfo] = useState(null)

  async function handleLogin(e) {
    e.preventDefault()
    const form = new FormData(e.target)
    const username = form.get('username')
    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
      })
      const data = await res.json()
      setUser(data.username || username)
      setRoleInfo(data.role || 'guest')
    } catch (err) {
      console.error(err)
      setRoleInfo('guest')
    }
  }

  if (!user) {
    return (
      <div className="p-6 max-w-md mx-auto">
        <h2 className="text-2xl font-semibold mb-4">Welcome to Mbuu</h2>
        <TabAuth onAuth={(data) => { setUser(data.username || data.entered); setRoleInfo(data.role || 'guest'); }} />
      </div>
    )
  }

  return (
    <div>
      <Header user={user} onLogout={() => { setUser(null); setRoleInfo(null); }} />
      <div className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Hello, {user}</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">Role: {roleInfo}</p>
          </div>
        </div>
        <div className="mt-6">
          {roleInfo === 'admin' ? <Seller /> : <Buyer />}
        </div>
      </div>
    </div>
  )
}
