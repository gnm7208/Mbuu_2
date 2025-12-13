import CarCard from "./CarCard";
export default function CarList({ cars, onPurchase }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 16 }}>
      {cars.map(c => <CarCard key={c.id} car={c} onPurchase={onPurchase} />)}
    </div>
  );
}
