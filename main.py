# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, users, dealerships, cars, sales, uploads
from fastapi.staticfiles import StaticFiles
import os

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "uploads")), name="static")

app = FastAPI(title="Mbuu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(dealerships.router, prefix="/dealerships", tags=["dealerships"])
app.include_router(cars.router, prefix="/cars", tags=["cars"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(uploads.router, prefix="/upload", tags=["uploads"])
