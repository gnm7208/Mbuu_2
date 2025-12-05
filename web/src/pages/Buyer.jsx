import React, { useEffect, useState } from 'react'
import { fetchCars } from '../utils/api'

export default function Buyer() {
  const [cars, setCars] = useState([])
  const [filters, setFilters] = useState({ brand: '', year: '', available: '1' })

  async function load() {
    try {
      const params = {}
      if (filters.brand) params.brand = filters.brand
      if (filters.year) params.year = filters.year
      if (filters.available !== undefined) params.available = filters.available
      const list = await fetchCars(params)
      setCars(list)
    } catch (e) { console.error(e) }
  }

  useEffect(() => { load() }, [])

  return (
    <div>
      <h3 className="text-lg font-medium">Available Cars</h3>
      <div className="mt-3 p-3 bg-white dark:bg-slate-800 border rounded">
        <div className="flex gap-2">
          <input value={filters.brand} onChange={e=>setFilters({...filters, brand: e.target.value})} placeholder="Brand" className="p-2 border rounded" />
          <input value={filters.year} onChange={e=>setFilters({...filters, year: e.target.value})} placeholder="Year" className="p-2 border rounded w-24" />
          <select value={filters.available} onChange={e=>setFilters({...filters, available: e.target.value})} className="p-2 border rounded w-40">
            <option value="1">Available only</option>
            <option value="0">Sold only</option>
            <option value="">All</option>
          </select>
          <button onClick={load} className="px-3 py-1 bg-blue-600 text-white rounded">Filter</button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        {cars.map(c => (
          <div key={c.id} className="p-4 border rounded bg-white dark:bg-slate-800">
            <img src={c.image_url} alt={c.model} className="w-full h-40 object-cover rounded" />
            <h4 className="mt-2 font-semibold">{c.brand} {c.model} ({c.year})</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">Price: ${c.price}</p>
            <p className="text-sm text-slate-500">Dealership: {c.dealership_name}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
