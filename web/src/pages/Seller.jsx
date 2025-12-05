import React, { useEffect, useState } from 'react'
import { fetchDealerships } from '../utils/api'

export default function Seller() {
  const [biz, setBiz] = useState([])

  useEffect(() => {
    fetchDealerships()
      .then(setBiz)
      .catch(console.error)
  }, [])

  return (
    <div>
      <h3 className="text-lg font-medium">Your Dealerships</h3>
      <ul className="mt-4 space-y-3">
        {biz.map(d => (
          <li key={d.id} className="p-3 border rounded bg-white dark:bg-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold">{d.name}</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">{d.location}</div>
              </div>
              <div className="text-sm text-slate-500">Cars: {d.car_count || 0}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
