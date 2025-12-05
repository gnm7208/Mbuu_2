import React, { useEffect, useState } from 'react'

export default function Buyer() {
  const [cars, setCars] = useState([])

  useEffect(() => {
    fetch('/api/cars')
      .then(r => r.json())
      .then(setCars)
      .catch(console.error)
  }, [])

  return (
    <div>
      <h3 className="text-lg font-medium">Available Cars</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        {cars.map(c => (
          <div key={c.id} className="p-4 border rounded bg-white dark:bg-slate-800">
            <img src={c.image_url} alt={c.model} className="w-full h-40 object-cover rounded" />
            <h4 className="mt-2 font-semibold">{c.brand} {c.model} ({c.year})</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">Price: ${c.price}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
