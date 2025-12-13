# api/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import create_access_token, verify_password, hash_password
from models.user import User
from models import get_session

class LoginBody(BaseModel):
    username: str
    password: str

class RegisterBody(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False

router = APIRouter()

@router.post("/login")
def login(body: LoginBody):
    session = get_session()
    try:
        user = session.query(User).filter(User.username == body.username).first()
        if not user or not verify_password(body.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.id})
        return {"id": user.id, "username": user.username, "is_admin": user.is_admin, "token": token}
    finally:
        session.close()

@router.post("/register")
def register(body: RegisterBody):
    session = get_session()
    try:
        if session.query(User).filter((User.username == body.username) | (User.email == body.email)).first():
            raise HTTPException(status_code=400, detail="Username or email already exists")

        user = User(username=body.username, email=body.email, password=hash_password(body.password), is_admin=body.is_admin)
        session.add(user)
        session.commit()
        session.refresh(user)
        token = create_access_token({"sub": user.id})
        return {"id": user.id, "username": user.username, "is_admin": user.is_admin, "token": token}
    finally:
        session.close()
