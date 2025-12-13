import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { api } from "../services/api";

export default function MyPurchases() {
  const { user, token } = useContext(AuthContext);
  const [sales, setSales] = useState([]);

  useEffect(() => {
    if (user) api(`/sales/user/${user.id}`, { token }).then(setSales);
  }, [user, token]);

  const total = sales.reduce((sum, s) => sum + s.sale_price, 0);

  return (
    <div>
      <h2>{user?.username}'s purchases</h2>
      <ul>
        {sales.map(s => (
          <li key={s.id}>
            {s.car.year} {s.car.brand} {s.car.model} — ${s.sale_price} — {new Date(s.sale_date).toLocaleDateString()}
          </li>
        ))}
      </ul>
      <p>Total spent: ${total.toFixed(2)}</p>
    </div>
  );
}
