# api/cars.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models.car import Car
from models.dealership import Dealership
from models import get_session
from core.deps import require_admin

class CreateCarBody(BaseModel):
    brand: str
    model: str
    year: int
    price: float
    color: str
    dealership_id: int
    image_url: str | None = None

router = APIRouter()

def serialize_car(c: Car):
    return {
        "id": c.id,
        "brand": c.brand,
        "model": c.model,
        "year": c.year,
        "price": c.price,
        "color": c.color,
        "is_sold": c.is_sold,
        "dealership": {"id": c.dealership.id, "name": c.dealership.name} if c.dealership else None,
        "image_url": getattr(c, "image_url", None),
    }

@router.get("")
def list_all_cars():
    cars = Car.get_all()
    return [serialize_car(c) for c in cars]

@router.get("/available")
def list_available_cars():
    cars = Car.get_available()
    return [serialize_car(c) for c in cars]

@router.get("/search")
def search_cars(brand: str):
    cars = Car.find_by_brand(brand)
    return [serialize_car(c) for c in cars]

@router.post("")
def add_car(body: CreateCarBody, admin = Depends(require_admin)):
    session = get_session()
    try:
        # Verify dealership belongs to admin
        d = session.query(Dealership).filter(Dealership.id == body.dealership_id).first()
        if not d or d.admin_id != admin.id:
            raise ValueError("You must own the dealership to add cars")

        car = Car(brand=body.brand, model=body.model, year=body.year, price=body.price, color=body.color, dealership_id=d.id)
        if hasattr(car, "image_url"):  # add this field to model if desired
            car.image_url = body.image_url
        session.add(car)
        session.commit()
        session.refresh(car)
        # eager relationship
        _ = car.dealership.name
        return serialize_car(car)
    finally:
        session.close()
