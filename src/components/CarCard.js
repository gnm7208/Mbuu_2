export default function CarCard({ car, onPurchase }) {
  return (
    <div className="card">
      {car.image_url && <img src={car.image_url} alt={`${car.brand} ${car.model}`} style={{ width: "100%", borderRadius: 12 }} />}
      <h3>{car.year} {car.brand} {car.model}</h3>
      <p>{car.color} • ${car.price}</p>
      <small>Dealership: {car.dealership?.name}</small>
      {!car.is_sold && onPurchase && <button className="btn btn-primary" onClick={() => onPurchase(car)}>Purchase</button>}
    </div>
  );
}
