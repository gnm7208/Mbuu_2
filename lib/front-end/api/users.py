# api/users.py
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from models import get_session
from core.deps import require_admin

router = APIRouter()

@router.get("")
def get_users(admin = Depends(require_admin)):
    session = get_session()
    try:
        users = session.query(User).all()
        return [{"id": u.id, "username": u.username, "email": u.email, "is_admin": u.is_admin} for u in users]
    finally:
        session.close()

@router.delete("/{user_id}")
def delete_user(user_id: int, admin = Depends(require_admin)):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"success": True}
    finally:
        session.close()
