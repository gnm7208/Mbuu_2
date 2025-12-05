import React, { useState } from 'react'
import Splash from './pages/Splash'
import Home from './pages/Home'
import Header from './components/Header'
import useTheme from './hooks/useTheme'

export default function App() {
  const [showSplash, setShowSplash] = useState(true)
  const [theme] = useTheme()

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100">
      {showSplash ? (
        <Splash onDone={() => setShowSplash(false)} />
      ) : (
        <div className="flex flex-col min-h-screen">
          <Header />
          <main className="flex-1">
            <Home />
          </main>
        </div>
      )}
    </div>
  )
}
