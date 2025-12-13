# api/uploads.py
import os, uuid
from fastapi import APIRouter, UploadFile, File, Depends
from core.deps import get_current_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT = os.path.join(os.path.dirname(BASE_DIR), "uploads")

def save_file(subdir: str, file: UploadFile):
    folder = os.path.join(UPLOAD_ROOT, subdir)
    os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(folder, name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return f"/static/{subdir}/{name}", path

router = APIRouter()

@router.post("/profile")
def upload_profile(file: UploadFile = File(...), user = Depends(get_current_user)):
    url, _ = save_file("profile", file)
    return {"url": f"http://localhost:8000{url}"}

@router.post("/dealership")
def upload_dealership(file: UploadFile = File(...), user = Depends(get_current_user)):
    if not user.is_admin: 
        raise Exception("Admin required")
    url, _ = save_file("dealership", file)
    return {"url": f"http://localhost:8000{url}"}

@router.post("/car")
def upload_car(file: UploadFile = File(...), user = Depends(get_current_user)):
    if not user.is_admin:
        raise Exception("Admin required")
    url, _ = save_file("car", file)
    return {"url": f"http://localhost:8000{url}"}
