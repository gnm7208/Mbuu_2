import React from 'react'
import useTheme from '../hooks/useTheme'

export default function Header({ user, onLogout }) {
  const [theme, setTheme] = useTheme()

  return (
    <header className="flex items-center justify-between p-4 bg-white dark:bg-slate-800 border-b">
      <div className="flex items-center gap-3">
        <div className="font-bold">Mbuu</div>
        <div className="text-sm text-slate-500 dark:text-slate-300">{user || 'Guest'}</div>
      </div>
      <div className="flex items-center gap-3">
        <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} className="px-3 py-1 border rounded">
          {theme === 'dark' ? 'Light' : 'Dark'}
        </button>
        {onLogout && (
          <button onClick={onLogout} className="px-3 py-1 bg-red-500 text-white rounded">Logout</button>
        )}
      </div>
    </header>
  )
}
