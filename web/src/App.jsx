import React, { useState } from 'react'
import Splash from './pages/Splash'
import Home from './pages/Home'
import useTheme from './hooks/useTheme'

export default function App() {
  const [showSplash, setShowSplash] = useState(true)
  const [theme] = useTheme()

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100">
      {showSplash ? (
        <Splash onDone={() => setShowSplash(false)} />
      ) : (
        <Home />
      )}
    </div>
  )
}
