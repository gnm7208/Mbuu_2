# api/sales.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.sale import Sale
from models.car import Car
from models import get_session
from core.deps import get_current_user

class CreateSaleBody(BaseModel):
    user_id: int
    car_id: int
    dealership_id: int
    sale_price: float

router = APIRouter()

@router.get("/user/{user_id}")
def get_my_sales(user_id: int, user = Depends(get_current_user)):
    if user.id != user_id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    session = get_session()
    try:
        sales = Sale.find_by_customer(user_id)
        out = []
        for s in sales:
            out.append({
                "id": s.id,
                "sale_price": s.sale_price,
                "sale_date": s.sale_date.isoformat(),
                "car": {
                    "id": s.car.id, "brand": s.car.brand, "model": s.car.model, "year": s.car.year
                },
                "dealership": {"id": s.dealership.id, "name": s.dealership.name}
            })
        return out
    finally:
        session.close()

@router.post("")
def purchase(body: CreateSaleBody, user = Depends(get_current_user)):
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Admins cannot purchase cars")
    if user.id != body.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    session = get_session()
    try:
        car = Car.find_by_id(body.car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        if car.is_sold:
            raise HTTPException(status_code=400, detail="Car already sold")

        sale = Sale.create(user.id, car.id, body.dealership_id, body.sale_price)
        car.mark_sold()
        return {"id": sale.id, "sale_price": sale.sale_price, "sale_date": sale.sale_date.isoformat()}
    finally:
        session.close()
