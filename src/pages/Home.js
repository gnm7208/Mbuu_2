import { useEffect, useState, useContext } from "react";
import { api } from "../services/api";
import CarList from "../components/CarList";
import { AuthContext } from "../context/AuthContext";

export default function Home() {
  const [cars, setCars] = useState([]);
  const [brand, setBrand] = useState("");
  const { user, token } = useContext(AuthContext);

  useEffect(() => { api("/cars/available").then(setCars); }, []);

  const search = async () => {
    const res = await api(`/cars/search?brand=${encodeURIComponent(brand)}`);
    setCars(res);
  };

  const purchase = async (car) => {
    if (!user || user.is_admin) return alert("Login as a customer to purchase.");
    await api("/sales", { method: "POST", token, body: { user_id: user.id, car_id: car.id, dealership_id: car.dealership.id, sale_price: car.price } });
    alert("Purchase successful!");
    const updated = await api("/cars/available");
    setCars(updated);
  };

  return (
    <div>
      <div className="card" style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input placeholder="Search brand (e.g., Toyota)" value={brand} onChange={e => setBrand(e.target.value)} />
        <button className="btn" onClick={search}>Search</button>
      </div>
      <CarList cars={cars} onPurchase={purchase} />
    </div>
  );
}
