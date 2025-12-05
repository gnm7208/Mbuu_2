import React, { useEffect } from 'react'
import logo from '../assets/logo.svg'

export default function Splash({ onDone }) {
  useEffect(() => {
    // For development, shorten the splash to 3s. Production can be 20s.
    const t = setTimeout(onDone, 3000)
    return () => clearTimeout(t)
  }, [onDone])

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <img src={logo} alt="Mbuu" className="mx-auto w-48 h-48" />
        <h1 className="mt-4 text-4xl font-bold">Mbuu</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">Find cars, manage dealerships</p>
      </div>
    </div>
  )
}
