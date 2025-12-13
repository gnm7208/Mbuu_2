# api/dealerships.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.dealership import Dealership
from models import get_session
from core.deps import get_current_user, require_admin

class CreateDealershipBody(BaseModel):
    name: str
    location: str
    image_url: str | None = None

router = APIRouter()

@router.get("")
def list_dealerships():
    session = get_session()
    try:
        ds = session.query(Dealership).all()
        out = []
        for d in ds:
            out.append({
                "id": d.id,
                "name": d.name,
                "location": d.location,
                "admin": {"id": d.admin.id, "username": d.admin.username} if d.admin else None,
                "car_count": d.car_count,
                "total_sales": d.total_sales,
                "image_url": getattr(d, "image_url", None)
            })
        return out
    finally:
        session.close()

@router.get("/admin/{admin_id}")
def my_dealerships(admin_id: int, user = Depends(get_current_user)):
    session = get_session()
    try:
        ds = session.query(Dealership).filter(Dealership.admin_id == admin_id).all()
        return [{"id": d.id, "name": d.name, "location": d.location, "image_url": getattr(d, "image_url", None)} for d in ds]
    finally:
        session.close()

@router.post("")
def create_dealership(body: CreateDealershipBody, admin = Depends(require_admin)):
    session = get_session()
    try:
        d = Dealership(name=body.name, location=body.location, admin_id=admin.id)
        # If you add image_url column to Dealership model:
        if hasattr(d, "image_url"):
            d.image_url = body.image_url
        session.add(d)
        session.commit()
        session.refresh(d)
        return {"id": d.id, "name": d.name, "location": d.location, "image_url": getattr(d, "image_url", None)}
    finally:
        session.close()

@router.delete("/{dealership_id}")
def delete_dealership(dealership_id: int, admin = Depends(require_admin)):
    session = get_session()
    try:
        d = session.query(Dealership).filter(Dealership.id == dealership_id).first()
        if not d:
            raise HTTPException(status_code=404, detail="Not found")
        if d.admin_id != admin.id:
            raise HTTPException(status_code=403, detail="You can only delete your own dealerships")
        session.delete(d)
        session.commit()
        return {"success": True}
    finally:
        session.close()
