import React, { useEffect, useState } from 'react'
import { fetchDealerships, createDealership, createCar } from '../utils/api'

export default function Seller() {
  const [biz, setBiz] = useState([])
  const [newDeal, setNewDeal] = useState({ name: '', location: '', admin_id: '' })
  const [adding, setAdding] = useState(null) // dealership id where adding car

  async function load() {
    try {
      const list = await fetchDealerships()
      setBiz(list)
    } catch (e) { console.error(e) }
  }

  useEffect(() => { load() }, [])

  async function handleCreateDeal(e) {
    e.preventDefault()
    try {
      const res = await createDealership(newDeal)
      if (res.error) throw new Error(res.error)
      setNewDeal({ name: '', location: '', admin_id: '' })
      await load()
    } catch (err) { console.error(err) }
  }

  async function handleAddCar(e, dealershipId) {
    e.preventDefault()
    const fd = new FormData(e.target)
    const payload = {
      brand: fd.get('brand'),
      model: fd.get('model'),
      year: fd.get('year'),
      price: fd.get('price'),
      color: fd.get('color'),
      dealership_id: dealershipId
    }
    try {
      const res = await createCar(payload)
      if (res.error) throw new Error(res.error)
      setAdding(null)
      await load()
    } catch (err) { console.error(err) }
  }

  return (
    <div>
      <h3 className="text-lg font-medium">Your Dealerships</h3>
      <div className="mt-4 p-3 border rounded bg-white dark:bg-slate-800">
        <form onSubmit={handleCreateDeal} className="grid grid-cols-1 gap-2">
          <input value={newDeal.name} onChange={e=>setNewDeal({...newDeal, name: e.target.value})} name="name" placeholder="Dealership name" className="p-2 border rounded" />
          <input value={newDeal.location} onChange={e=>setNewDeal({...newDeal, location: e.target.value})} name="location" placeholder="Location" className="p-2 border rounded" />
          <input value={newDeal.admin_id} onChange={e=>setNewDeal({...newDeal, admin_id: e.target.value})} name="admin_id" placeholder="Admin user id" className="p-2 border rounded" />
          <div className="flex justify-end">
            <button className="px-3 py-1 bg-green-600 text-white rounded">Create Dealership</button>
          </div>
        </form>
      </div>

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

            <div className="mt-3">
              {adding === d.id ? (
                <form onSubmit={(e)=>handleAddCar(e, d.id)} className="grid grid-cols-1 gap-2">
                  <input name="brand" placeholder="Brand" className="p-2 border rounded" />
                  <input name="model" placeholder="Model" className="p-2 border rounded" />
                  <input name="year" placeholder="Year" className="p-2 border rounded" />
                  <input name="price" placeholder="Price" className="p-2 border rounded" />
                  <input name="color" placeholder="Color" className="p-2 border rounded" />
                  <div className="flex gap-2 justify-end">
                    <button type="button" onClick={()=>setAdding(null)} className="px-3 py-1 border rounded">Cancel</button>
                    <button className="px-3 py-1 bg-blue-600 text-white rounded">Add Car</button>
                  </div>
                </form>
              ) : (
                <div className="flex justify-end mt-3">
                  <button onClick={()=>setAdding(d.id)} className="px-3 py-1 bg-indigo-600 text-white rounded">Add Car</button>
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
