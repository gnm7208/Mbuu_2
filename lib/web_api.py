#!/usr/bin/env python3
"""
Simple Flask API for Mbuu frontend integration.

Run this with: `pipenv run python lib/web_api.py`

Provides lightweight JSON endpoints for users, dealerships, cars and simple auth.
"""
import os
import sys
from flask import Flask, jsonify, request

# Ensure `lib` directory is on path so `models` package resolves
sys.path.insert(0, os.path.dirname(__file__))

from models.user import User
from models.dealership import Dealership
from models.car import Car
from models.sale import Sale

try:
    from flask_cors import CORS
except Exception:
    CORS = lambda app: app

app = Flask(__name__)
CORS(app)

# Simple image mapping for car brands (hotlinks)
BRAND_IMAGES = {
    "Toyota": "https://source.unsplash.com/featured/?toyota-car",
    "Honda": "https://source.unsplash.com/featured/?honda-car",
    "BMW": "https://source.unsplash.com/featured/?bmw-car",
    "Mercedes": "https://source.unsplash.com/featured/?mercedes-car",
    "Audi": "https://source.unsplash.com/featured/?audi-car",
    "Ford": "https://source.unsplash.com/featured/?ford-truck",
    "Chevrolet": "https://source.unsplash.com/featured/?chevrolet-car",
    "Nissan": "https://source.unsplash.com/featured/?nissan-car",
}

def car_to_dict(car):
    return {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "price": float(car.price),
        "color": car.color,
        "is_sold": bool(car.is_sold),
        "dealership_id": car.dealership_id,
        "dealership_name": getattr(car.dealership, 'name', None),
        "image_url": BRAND_IMAGES.get(car.brand, "https://source.unsplash.com/featured/?car")
    }

@app.route('/api/users', methods=['GET'])
def api_users():
    users = User.get_all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email, "is_admin": bool(u.is_admin)} for u in users])

@app.route('/api/dealerships', methods=['GET'])
def api_dealerships():
    items = Dealership.get_all()
    result = []
    for d in items:
        result.append({
            "id": d.id,
            "name": d.name,
            "location": d.location,
            "admin_id": d.admin_id,
            "admin_username": getattr(d.admin, 'username', None),
            "car_count": d.car_count,
            "total_sales": d.total_sales,
        })
    return jsonify(result)

@app.route('/api/cars', methods=['GET'])
def api_cars():
    # Filtering: brand, year, available
    brand = request.args.get('brand')
    year = request.args.get('year')
    available = request.args.get('available')

    cars = Car.get_all()
    if brand:
        cars = [c for c in cars if brand.lower() in c.brand.lower()]
    if year:
        try:
            y = int(year)
            cars = [c for c in cars if c.year == y]
        except ValueError:
            pass
    if available is not None:
        if available.lower() in ('1', 'true', 'yes'):
            cars = [c for c in cars if not c.is_sold]
        elif available.lower() in ('0', 'false', 'no'):
            cars = [c for c in cars if c.is_sold]

    return jsonify([car_to_dict(c) for c in cars])

@app.route('/api/auth', methods=['POST'])
def api_auth():
    data = request.get_json() or {}
    username = data.get('username')
    if not username:
        return jsonify({"error": "username required"}), 400

    user = User.find_by_username(username)
    if not user:
        return jsonify({"role": "guest"})

    role = 'admin' if user.is_admin else 'customer'
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": role})

@app.route('/api/sales', methods=['GET'])
def api_sales():
    sales = Sale.get_all()
    result = []
    for s in sales:
        result.append({
            "id": s.id,
            "customer_id": s.customer_id,
            "customer_username": getattr(s.customer, 'username', None),
            "car_id": s.car_id,
            "car_model": getattr(s.car, 'model', None),
            "dealership_id": s.dealership_id,
            "sale_price": float(s.sale_price),
            "sale_date": s.sale_date.isoformat() if s.sale_date else None,
        })
    return jsonify(result)


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    if User.find_by_username(username):
        return jsonify({"error": "username already exists"}), 400

    # naive registration (no hashing) — this project uses plain text passwords for simplicity
    try:
        user = User.create(username=username, email=email, password=password, is_admin=bool(is_admin))
        return jsonify({"id": user.id, "username": user.username, "email": user.email, "is_admin": bool(user.is_admin)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/dealerships', methods=['POST'])
def api_create_dealership():
    data = request.get_json() or {}
    name = data.get('name')
    location = data.get('location')
    admin_id = data.get('admin_id')

    if not name or not location or not admin_id:
        return jsonify({"error": "name, location and admin_id are required"}), 400

    admin = User.find_by_id(admin_id)
    if not admin:
        return jsonify({"error": "admin user not found"}), 404
    if not admin.is_admin:
        return jsonify({"error": "user is not an admin"}), 403

    try:
        d = Dealership.create(name=name, location=location, admin_id=admin_id)
        return jsonify({"id": d.id, "name": d.name, "location": d.location, "admin_id": d.admin_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cars', methods=['POST'])
def api_create_car():
    data = request.get_json() or {}
    brand = data.get('brand')
    model_name = data.get('model')
    year = data.get('year')
    price = data.get('price')
    color = data.get('color')
    dealership_id = data.get('dealership_id')

    if not all([brand, model_name, year, price, color, dealership_id]):
        return jsonify({"error": "brand, model, year, price, color, dealership_id are required"}), 400

    # basic conversions
    try:
        year = int(year)
        price = float(price)
    except ValueError:
        return jsonify({"error": "invalid year or price format"}), 400

    d = Dealership.find_by_id(dealership_id)
    if not d:
        return jsonify({"error": "dealership not found"}), 404

    try:
        car = Car.create(brand=brand, model=model_name, year=year, price=price, color=color, dealership_id=dealership_id)
        return jsonify(car_to_dict(car))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cars/<int:car_id>/sell', methods=['POST'])
def api_sell_car(car_id):
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    sale_price = data.get('sale_price')

    if not customer_id or not sale_price:
        return jsonify({"error": "customer_id and sale_price are required"}), 400

    try:
        sale_price = float(sale_price)
    except ValueError:
        return jsonify({"error": "invalid sale_price"}), 400

    car = Car.find_by_id(car_id)
    if not car:
        return jsonify({"error": "car not found"}), 404
    if car.is_sold:
        return jsonify({"error": "car already sold"}), 400

    customer = User.find_by_id(customer_id)
    if not customer:
        return jsonify({"error": "customer not found"}), 404

    try:
        sale = Sale.create(customer_id=customer_id, car_id=car_id, dealership_id=car.dealership_id, sale_price=sale_price)
        car.mark_sold()
        return jsonify({"sale_id": sale.id, "car_id": car_id, "sale_price": float(sale.sale_price)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
