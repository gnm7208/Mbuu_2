import { useEffect, useState } from 'react'

export default function useTheme() {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('mbuu-theme') || 'light'
    } catch (e) {
      return 'light'
    }
  })

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    try { localStorage.setItem('mbuu-theme', theme) } catch (e) {}
  }, [theme])

  return [theme, setTheme]
}
