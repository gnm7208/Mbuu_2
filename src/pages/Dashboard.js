import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { api } from "../services/api";
import UploadImage from "../components/UploadImage";

export default function Dashboard() {
  const { user, token } = useContext(AuthContext);
  const [dealerships, setDealerships] = useState([]);
  const [formD, setFormD] = useState({ name: "", location: "", image_url: "" });
  const [formC, setFormC] = useState({ brand: "", model: "", year: 2024, price: 10000, color: "", dealership_id: 0, image_url: "" });

  useEffect(() => {
    if (user?.is_admin) api(`/dealerships/admin/${user.id}`, { token }).then(setDealerships);
  }, [user, token]);

  const createDealership = async (e) => {
    e.preventDefault();
    const d = await api("/dealerships", { method: "POST", token, body: formD });
    setDealerships(prev => [d, ...prev]);
    setFormD({ name: "", location: "", image_url: "" });
  };

  const addCar = async (e) => {
    e.preventDefault();
    const c = await api("/cars", { method: "POST", token, body: formC });
    alert(`Added ${c.year} ${c.brand} ${c.model}`);
    setFormC({ brand: "", model: "", year: 2024, price: 10000, color: "", dealership_id: 0, image_url: "" });
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>

      <div className="card">
        <h3>My Dealerships</h3>
        <ul>{dealerships.map(d => <li key={d.id}>{d.name} — {d.location}</li>)}</ul>
      </div>

      <form onSubmit={createDealership} className="card" style={{ marginTop: 16 }}>
        <h3>Create Dealership</h3>
        <input placeholder="Name" value={formD.name} onChange={e => setFormD({ ...formD, name: e.target.value })} />
        <input placeholder="Location" value={formD.location} onChange={e => setFormD({ ...formD, location: e.target.value })} />
        <UploadImage endpoint="/upload/dealership" onUploaded={url => setFormD({ ...formD, image_url: url })} />
        <button className="btn btn-primary" type="submit">Create</button>
      </form>

      <form onSubmit={addCar} className="card" style={{ marginTop: 16 }}>
        <h3>Add Car</h3>
        <select value={formC.dealership_id} onChange={e => setFormC({ ...formC, dealership_id: Number(e.target.value) })}>
          <option value={0}>Select dealership</option>
          {dealerships.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <input placeholder="Brand" value={formC.brand} onChange={e => setFormC({ ...formC, brand: e.target.value })} />
        <input placeholder="Model" value={formC.model} onChange={e => setFormC({ ...formC, model: e.target.value })} />
        <input type="number" placeholder="Year" value={formC.year} onChange={e => setFormC({ ...formC, year: Number(e.target.value) })} />
        <input type="number" placeholder="Price" value={formC.price} onChange={e => setFormC({ ...formC, price: Number(e.target.value) })} />
        <input placeholder="Color" value={formC.color} onChange={e => setFormC({ ...formC, color: e.target.value })} />
        <UploadImage endpoint="/upload/car" onUploaded={url => setFormC({ ...formC, image_url: url })} />
        <button className="btn btn-primary" type="submit">Add Car</button>
      </form>
    </div>
  );
}
