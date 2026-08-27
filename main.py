import re
import json
import os
import hashlib
import math
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Form, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="CropConnect - Digital Agri Marketplace & Smart Logistics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# JSON FILE DATABASE (persists across restarts)
# ==========================================
USERS_FILE = "users.json"
LISTINGS_FILE = "listings.json"
MESSAGES_FILE = "messages.json"
ORDERS_FILE = "orders.json"
TRIPS_FILE = "trips.json"

def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def normalize_phone(phone: str) -> str:
    """Normalize phone strings by stripping formatting characters."""
    if not phone:
        return ""
    p = re.sub(r'[^\d+]', '', str(phone).strip())
    return p

def phones_match(p1: str, p2: str) -> bool:
    """Check if two phone numbers match, handling +91 prefix and plain formats."""
    n1 = normalize_phone(p1)
    n2 = normalize_phone(p2)
    if not n1 or not n2:
        return False
    if n1 == n2:
        return True
    d1 = re.sub(r'\D', '', n1)
    d2 = re.sub(r'\D', '', n2)
    if len(d1) >= 10 and len(d2) >= 10:
        return d1[-10:] == d2[-10:]
    return False

def load_users() -> dict:
    """Read users from disk. Seed with demo accounts if missing or empty."""
    default_pass = hash_password("password123")
    seed = {
        "+919876543210": {
            "name": "Ramesh Kumar (Farmer)",
            "phone": "+919876543210",
            "zip_code": "500001",
            "role": "FARMER",
            "password": default_pass
        },
        "+919876543220": {
            "name": "Telangana Kisan FPO (Aggregator)",
            "phone": "+919876543220",
            "zip_code": "500001",
            "role": "FPO",
            "password": default_pass
        },
        "+919876543211": {
            "name": "Suresh Wholesale & Retail Hub",
            "phone": "+919876543211",
            "zip_code": "500001",
            "role": "BULK_BUYER",
            "password": default_pass
        },
        "+919876543230": {
            "name": "Priya Sharma (Consumer)",
            "phone": "+919876543230",
            "zip_code": "500001",
            "role": "CONSUMER",
            "password": default_pass
        },
        "+1234567890": {
            "name": "Farmer John",
            "phone": "+1234567890",
            "zip_code": "90210",
            "role": "FARMER",
            "password": default_pass
        }
    }
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
        return seed
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure essential demo users exist
            updated = False
            for k, v in seed.items():
                if k not in data and not any(phones_match(k, existing_k) for existing_k in data):
                    data[k] = v
                    updated = True
            if updated:
                with open(USERS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out, indent=2)
            return data
    except Exception:
        return seed

def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

USERS_DB = load_users()


def load_listings() -> list:
    """Read listings from disk. Create rich seed data if missing."""
    seed = [
        {
            "id": 1,
            "farmer_name": "Ramesh Kumar (Farmer)",
            "farmer_phone": "+919876543210",
            "seller_type": "FARMER",
            "crop_name": "TOMATO",
            "quantity_kg": 450.0,
            "price_per_kg": 28.0,
            "mandi_price_per_kg": 18.0,
            "retail_market_price_per_kg": 42.0,
            "min_order_kg": 5.0,
            "bulk_price_per_kg": 25.0,
            "zip_code": "500001",
            "location_name": "Shamshabad Peri-urban Cluster",
            "lat": 17.2500,
            "lon": 78.4200,
            "quality_grade": "Grade A - Premium Fresh",
            "harvest_date": "2026-08-26",
            "shelf_life_days": 6,
            "source": "WEB",
            "status": "ACTIVE"
        },
        {
            "id": 2,
            "farmer_name": "Telangana Kisan FPO (Aggregator)",
            "farmer_phone": "+919876543220",
            "seller_type": "FPO",
            "crop_name": "RED ONION",
            "quantity_kg": 1200.0,
            "price_per_kg": 24.0,
            "mandi_price_per_kg": 16.0,
            "retail_market_price_per_kg": 38.0,
            "min_order_kg": 20.0,
            "bulk_price_per_kg": 21.0,
            "zip_code": "500001",
            "location_name": "Warangal FPO Collective Hub",
            "lat": 17.4000,
            "lon": 78.5000,
            "quality_grade": "Organic Certified",
            "harvest_date": "2026-08-25",
            "shelf_life_days": 25,
            "source": "WEB",
            "status": "ACTIVE"
        },
        {
            "id": 3,
            "farmer_name": "Ramesh Kumar (Farmer)",
            "farmer_phone": "+919876543210",
            "seller_type": "FARMER",
            "crop_name": "CHILLI",
            "quantity_kg": 180.0,
            "price_per_kg": 60.0,
            "mandi_price_per_kg": 42.0,
            "retail_market_price_per_kg": 85.0,
            "min_order_kg": 2.0,
            "bulk_price_per_kg": 54.0,
            "zip_code": "500001",
            "location_name": "Medchal Green Belt",
            "lat": 17.5200,
            "lon": 78.4800,
            "quality_grade": "Guntur Grade A Extra Spicy",
            "harvest_date": "2026-08-27",
            "shelf_life_days": 14,
            "source": "SMS",
            "status": "ACTIVE"
        },
        {
            "id": 4,
            "farmer_name": "Telangana Kisan FPO (Aggregator)",
            "farmer_phone": "+919876543220",
            "seller_type": "FPO",
            "crop_name": "POTATO",
            "quantity_kg": 850.0,
            "price_per_kg": 22.0,
            "mandi_price_per_kg": 14.0,
            "retail_market_price_per_kg": 34.0,
            "min_order_kg": 10.0,
            "bulk_price_per_kg": 19.5,
            "zip_code": "500001",
            "location_name": "Zaheerabad Agro Cluster",
            "lat": 17.6800,
            "lon": 77.6100,
            "quality_grade": "Standard Fresh Cleaned",
            "harvest_date": "2026-08-24",
            "shelf_life_days": 30,
            "source": "WEB",
            "status": "ACTIVE"
        },
        {
            "id": 5,
            "farmer_name": "Ramesh Kumar (Farmer)",
            "farmer_phone": "+919876543210",
            "seller_type": "FARMER",
            "crop_name": "BANANA",
            "quantity_kg": 320.0,
            "price_per_kg": 35.0,
            "mandi_price_per_kg": 22.0,
            "retail_market_price_per_kg": 55.0,
            "min_order_kg": 5.0,
            "bulk_price_per_kg": 30.0,
            "zip_code": "500001",
            "location_name": "Shamshabad Orchards",
            "lat": 17.2600,
            "lon": 78.4300,
            "quality_grade": "Robusta Naturally Ripened",
            "harvest_date": "2026-08-27",
            "shelf_life_days": 5,
            "source": "WEB",
            "status": "ACTIVE"
        }
    ]
    if not os.path.exists(LISTINGS_FILE):
        with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
        return seed
    try:
        with open(LISTINGS_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            if not items:
                with open(LISTINGS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(seed, f_out, indent=2)
                return seed
            # Upgrade existing records if missing new fields
            modified = False
            for it in items:
                if "seller_type" not in it:
                    it["seller_type"] = "FPO" if "FPO" in str(it.get("farmer_name", "")).upper() else "FARMER"
                    modified = True
                if "mandi_price_per_kg" not in it:
                    it["mandi_price_per_kg"] = round(float(it.get("price_per_kg", 20)) * 0.68, 1)
                    modified = True
                if "retail_market_price_per_kg" not in it:
                    it["retail_market_price_per_kg"] = round(float(it.get("price_per_kg", 20)) * 1.45, 1)
                    modified = True
                if "min_order_kg" not in it:
                    it["min_order_kg"] = 5.0
                    modified = True
                if "status" not in it:
                    it["status"] = "ACTIVE" if it.get("quantity_kg", 0) > 0 else "SOLD_OUT"
                    modified = True
            if modified:
                with open(LISTINGS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(items, f_out, indent=2)
            return items
    except Exception:
        return seed

def save_listings(items: list) -> None:
    with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

LISTINGS_DB = load_listings()


def load_messages() -> list:
    if not os.path.exists(MESSAGES_FILE):
        return []
    try:
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_messages(items: list) -> None:
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

MESSAGES_DB = load_messages()


def load_orders() -> list:
    """Read orders from disk. Create seed data if missing."""
    seed = [
        {
            "id": 1,
            "listing_id": 1,
            "crop_name": "TOMATO",
            "farmer_phone": "+919876543210",
            "farmer_name": "Ramesh Kumar (Farmer)",
            "buyer_phone": "+919876543211",
            "buyer_name": "Suresh Wholesale & Retail Hub",
            "buyer_role": "BULK_BUYER",
            "quantity_kg": 150.0,
            "price_per_kg": 25.0,
            "total_price": 3750.0,
            "status": "ACCEPTED",
            "delivery_address": "Wholesale Mart, Begumpet, Secunderabad",
            "delivery_zip": "500003",
            "delivery_lat": 17.4435,
            "delivery_lon": 78.4738,
            "notes": "Bulk morning delivery for supermarkets",
            "created_at": "2026-08-25T08:30:00.000000+00:00",
            "updated_at": "2026-08-25T09:00:00.000000+00:00"
        },
        {
            "id": 2,
            "listing_id": 2,
            "crop_name": "RED ONION",
            "farmer_phone": "+919876543220",
            "farmer_name": "Telangana Kisan FPO (Aggregator)",
            "buyer_phone": "+919876543230",
            "buyer_name": "Priya Sharma (Consumer)",
            "buyer_role": "CONSUMER",
            "quantity_kg": 25.0,
            "price_per_kg": 24.0,
            "total_price": 600.0,
            "status": "ACCEPTED",
            "delivery_address": "Apt 402, Green Valley Apartments, Banjara Hills",
            "delivery_zip": "500034",
            "delivery_lat": 17.4156,
            "delivery_lon": 78.4350,
            "notes": "Residential consumer fresh produce",
            "created_at": "2026-08-26T10:15:00.000000+00:00",
            "updated_at": "2026-08-26T11:00:00.000000+00:00"
        },
        {
            "id": 3,
            "listing_id": 1,
            "crop_name": "TOMATO",
            "farmer_phone": "+919876543210",
            "farmer_name": "Ramesh Kumar (Farmer)",
            "buyer_phone": "+919876543230",
            "buyer_name": "Priya Sharma (Consumer)",
            "buyer_role": "CONSUMER",
            "quantity_kg": 15.0,
            "price_per_kg": 28.0,
            "total_price": 420.0,
            "status": "PENDING",
            "delivery_address": "Apt 402, Green Valley Apartments, Banjara Hills",
            "delivery_zip": "500034",
            "delivery_lat": 17.4156,
            "delivery_lon": 78.4350,
            "notes": "Direct to home delivery",
            "created_at": "2026-08-27T07:20:00.000000+00:00",
            "updated_at": "2026-08-27T07:20:00.000000+00:00"
        }
    ]
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
        return seed
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
            if not items:
                with open(ORDERS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(seed, f_out, indent=2)
                return seed
            # Upgrade existing orders with delivery coordinates if missing
            modified = False
            for o in items:
                if "delivery_lat" not in o or not o["delivery_lat"]:
                    o["delivery_lat"] = 17.4200
                    o["delivery_lon"] = 78.4500
                    o["delivery_address"] = o.get("notes") or "Direct Customer Address"
                    modified = True
                if "buyer_role" not in o:
                    o["buyer_role"] = "CONSUMER" if o.get("quantity_kg", 0) < 50 else "BULK_BUYER"
                    modified = True
            if modified:
                with open(ORDERS_FILE, "w", encoding="utf-8") as f_out:
                    json.dump(items, f_out, indent=2)
            return items
    except Exception:
        return seed

def save_orders(items: list) -> None:
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

ORDERS_DB = load_orders()


def load_trips() -> list:
    """Read saved logistics trips from disk."""
    if not os.path.exists(TRIPS_FILE):
        return []
    try:
        with open(TRIPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_trips(items: list) -> None:
    with open(TRIPS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

TRIPS_DB = load_trips()


# ==========================================
# AUTH & ROLE HELPERS
# ==========================================

SELLER_ROLES = {"FARMER", "FPO"}
BUYER_ROLES = {"BUYER", "BULK_BUYER", "CONSUMER"}

def is_seller(role: str) -> bool:
    return str(role).strip().upper() in SELLER_ROLES

def is_buyer(role: str) -> bool:
    return str(role).strip().upper() in BUYER_ROLES

def find_user_by_phone(phone: str) -> Optional[dict]:
    """Look up user in USERS_DB with lenient phone matching."""
    if not phone:
        return None
    if phone in USERS_DB:
        return USERS_DB[phone]
    for k, v in USERS_DB.items():
        if phones_match(k, phone):
            return v
    return None

def require_user(phone: str) -> dict:
    user = find_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=403, detail="Unknown phone number. Please log in.")
    return user

def require_seller(phone: str) -> dict:
    user = require_user(phone)
    if not is_seller(user.get("role", "")):
        raise HTTPException(status_code=403, detail="This action is reserved for Farmers and FPOs only.")
    return user

def require_buyer(phone: str) -> dict:
    user = require_user(phone)
    if not is_buyer(user.get("role", "")):
        raise HTTPException(status_code=403, detail="This action is reserved for Consumers and Bulk Buyers only.")
    return user


# ==========================================
# PYDANTIC SCHEMAS
# ==========================================

class RegisterSchema(BaseModel):
    name: str
    phone: str
    zip_code: str
    role: str  # FARMER, FPO, BULK_BUYER, CONSUMER
    password: str

class LoginSchema(BaseModel):
    phone: str
    password: str
    role: str

class CreateOrderSchema(BaseModel):
    listing_id: int
    buyer_phone: str
    quantity_kg: float
    delivery_address: Optional[str] = "Customer Address"
    delivery_lat: Optional[float] = 17.4000
    delivery_lon: Optional[float] = 78.4800
    notes: Optional[str] = None

class CreateListingSchema(BaseModel):
    farmer_phone: str
    crop_name: str
    quantity_kg: float
    price_per_kg: float
    min_order_kg: Optional[float] = 5.0
    bulk_price_per_kg: Optional[float] = None
    zip_code: str
    location_name: Optional[str] = "Farm Gate"
    quality_grade: Optional[str] = "Grade A - Fresh"
    shelf_life_days: Optional[int] = 7

class UpdateListingSchema(BaseModel):
    farmer_phone: str
    crop_name: Optional[str] = None
    quantity_kg: Optional[float] = None
    price_per_kg: Optional[float] = None
    min_order_kg: Optional[float] = None
    bulk_price_per_kg: Optional[float] = None
    zip_code: Optional[str] = None
    quality_grade: Optional[str] = None
    shelf_life_days: Optional[int] = None

class SendMessageSchema(BaseModel):
    from_phone: str
    to_phone: str
    body: str

class RouteStopSchema(BaseModel):
    name: str
    lat: float
    lon: float
    quantity_kg: float = 0.0
    order_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class RoutePlanSchema(BaseModel):
    origin_name: str = "Farm Hub / Central Warehouse"
    origin_lat: float = 17.3850
    origin_lon: float = 78.4867
    stops: List[RouteStopSchema]
    vehicle_capacity_kg: float = 1000.0

class CreateTripSchema(BaseModel):
    farmer_phone: str
    origin_name: str
    origin_lat: float
    origin_lon: float
    vehicle_type: str
    vehicle_number: Optional[str] = "AP-28-TR-4402"
    driver_name: Optional[str] = "Driver Assigned"
    driver_phone: Optional[str] = "+919800112233"
    stops: List[RouteStopSchema]
    order_ids: List[int]
    total_distance_km: float
    total_load_kg: float
    estimated_travel_minutes: int
    fuel_cost_est: float
    co2_saved_kg: float


# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.post("/api/register")
def register_user(data: RegisterSchema):
    phone_norm = normalize_phone(data.phone)
    if find_user_by_phone(phone_norm):
        raise HTTPException(status_code=400, detail="Phone number already registered. Please log in.")

    role_clean = data.role.strip().upper()
    if role_clean not in SELLER_ROLES and role_clean not in BUYER_ROLES:
        role_clean = "FARMER" if "FARM" in role_clean else "BUYER"

    USERS_DB[phone_norm] = {
        "name": data.name.strip(),
        "phone": phone_norm,
        "zip_code": data.zip_code.strip(),
        "role": role_clean,
        "password": hash_password(data.password),
    }
    save_users(USERS_DB)
    safe_user = {k: v for k, v in USERS_DB[phone_norm].items() if k != "password"}
    return {"message": "Account created successfully!", "user": safe_user}


@app.post("/api/login")
def login_user(data: LoginSchema):
    user = find_user_by_phone(data.phone)
    if not user or user["password"] != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid phone number or password.")

    req_role = data.role.strip().upper()
    user_role = user.get("role", "").upper()

    if req_role != user_role:
        if (is_seller(req_role) and is_seller(user_role)) or (is_buyer(req_role) and is_buyer(user_role)):
            pass
        else:
            raise HTTPException(
                status_code=401,
                detail=f"Account role is {user_role}. Please select {user_role} to sign in."
            )

    safe_user = {k: v for k, v in user.items() if k != "password"}
    return {"message": "Login successful", "user": safe_user}


@app.get("/api/listings")
def get_listings(
    crop: Optional[str] = None,
    zip_code: Optional[str] = None,
    seller_type: Optional[str] = None,
    buyer_type: Optional[str] = None
):
    """Return active crop listings with fair pricing benchmarks and filter support."""
    results = [l for l in LISTINGS_DB if float(l.get("quantity_kg", 0)) > 0]
    
    if crop and crop.strip():
        q = crop.strip().lower()
        results = [l for l in results if q in str(l.get("crop_name", "")).lower()]
        
    if zip_code and zip_code.strip():
        z = zip_code.strip()
        results = [l for l in results if str(l.get("zip_code", "")) == z]
        
    if seller_type and seller_type.strip():
        st = seller_type.strip().upper()
        results = [l for l in results if str(l.get("seller_type", "")).upper() == st]

    return results


@app.post("/api/listings")
def create_listing(data: CreateListingSchema):
    seller = require_seller(data.farmer_phone)
    new_id = max([l["id"] for l in LISTINGS_DB], default=0) + 1
    
    price = float(data.price_per_kg)
    mandi_price = round(price * 0.70, 1)
    retail_price = round(price * 1.40, 1)
    bulk_price = float(data.bulk_price_per_kg) if data.bulk_price_per_kg else round(price * 0.90, 1)

    new_listing = {
        "id": new_id,
        "farmer_name": seller["name"],
        "farmer_phone": seller["phone"],
        "seller_type": seller.get("role", "FARMER"),
        "crop_name": data.crop_name.upper().strip(),
        "quantity_kg": float(data.quantity_kg),
        "price_per_kg": price,
        "mandi_price_per_kg": mandi_price,
        "retail_market_price_per_kg": retail_price,
        "min_order_kg": float(data.min_order_kg or 5.0),
        "bulk_price_per_kg": bulk_price,
        "zip_code": data.zip_code.strip(),
        "location_name": data.location_name or "Farm Gate",
        "lat": 17.3850,
        "lon": 78.4867,
        "quality_grade": data.quality_grade or "Grade A - Fresh",
        "harvest_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "shelf_life_days": int(data.shelf_life_days or 7),
        "source": "WEB",
        "status": "ACTIVE"
    }
    LISTINGS_DB.insert(0, new_listing)
    save_listings(LISTINGS_DB)
    return {"message": "Listing created successfully.", "listing": new_listing}


@app.put("/api/listings/{listing_id}")
def update_listing(listing_id: int, data: UpdateListingSchema):
    seller = require_seller(data.farmer_phone)
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    if not phones_match(listing["farmer_phone"], seller["phone"]):
        raise HTTPException(status_code=403, detail="You can only edit your own listings.")

    if data.crop_name:
        listing["crop_name"] = data.crop_name.upper().strip()
    if data.quantity_kg is not None:
        listing["quantity_kg"] = float(data.quantity_kg)
        listing["status"] = "ACTIVE" if listing["quantity_kg"] > 0 else "SOLD_OUT"
    if data.price_per_kg is not None:
        price = float(data.price_per_kg)
        listing["price_per_kg"] = price
        listing["mandi_price_per_kg"] = round(price * 0.70, 1)
        listing["retail_market_price_per_kg"] = round(price * 1.40, 1)
    if data.min_order_kg is not None:
        listing["min_order_kg"] = float(data.min_order_kg)
    if data.bulk_price_per_kg is not None:
        listing["bulk_price_per_kg"] = float(data.bulk_price_per_kg)
    if data.zip_code:
        listing["zip_code"] = data.zip_code.strip()
    if data.quality_grade:
        listing["quality_grade"] = data.quality_grade
    if data.shelf_life_days is not None:
        listing["shelf_life_days"] = int(data.shelf_life_days)

    save_listings(LISTINGS_DB)
    return {"message": "Listing updated successfully.", "listing": listing}


@app.delete("/api/listings/{listing_id}")
def delete_listing(listing_id: int, farmer_phone: str):
    seller = require_seller(farmer_phone)
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    if not phones_match(listing["farmer_phone"], seller["phone"]):
        raise HTTPException(status_code=403, detail="You can only delete your own listings.")

    LISTINGS_DB.remove(listing)
    save_listings(LISTINGS_DB)
    return {"message": "Listing deleted successfully."}


# ----- Orders & Direct Transactions Endpoints -----

@app.post("/api/order")
def place_order(data: CreateOrderSchema):
    buyer = require_buyer(data.buyer_phone)
    listing = next((l for l in LISTINGS_DB if l["id"] == data.listing_id), None)
    if not listing or float(listing.get("quantity_kg", 0)) <= 0:
        raise HTTPException(status_code=404, detail="Crop listing is no longer available or is sold out.")

    qty = float(data.quantity_kg)
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Requested quantity must be greater than 0.")

    min_qty = float(listing.get("min_order_kg", 1.0))
    if qty < min_qty:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum order quantity for this crop is {min_qty} KG."
        )

    if qty > float(listing["quantity_kg"]):
        raise HTTPException(
            status_code=400,
            detail=f"Requested quantity ({qty} KG) exceeds available stock ({listing['quantity_kg']} KG)."
        )

    price_per_kg = float(listing.get("price_per_kg", 20.0))
    if qty >= 50 and listing.get("bulk_price_per_kg"):
        price_per_kg = float(listing["bulk_price_per_kg"])

    total_price = round(qty * price_per_kg, 2)
    new_order_id = max([o["id"] for o in ORDERS_DB], default=0) + 1
    now_iso = datetime.now(timezone.utc).isoformat()

    new_order = {
        "id": new_order_id,
        "listing_id": listing["id"],
        "crop_name": listing["crop_name"],
        "farmer_phone": listing["farmer_phone"],
        "farmer_name": listing["farmer_name"],
        "buyer_phone": buyer["phone"],
        "buyer_name": buyer["name"],
        "buyer_role": buyer.get("role", "CONSUMER"),
        "quantity_kg": qty,
        "price_per_kg": price_per_kg,
        "total_price": total_price,
        "status": "PENDING",
        "delivery_address": (data.delivery_address or "Customer Address").strip(),
        "delivery_zip": listing.get("zip_code", "500001"),
        "delivery_lat": float(data.delivery_lat or 17.4000),
        "delivery_lon": float(data.delivery_lon or 78.4800),
        "notes": (data.notes or "").strip(),
        "created_at": now_iso,
        "updated_at": now_iso
    }
    ORDERS_DB.insert(0, new_order)
    save_orders(ORDERS_DB)

    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    role_title = "Bulk Buyer" if buyer.get("role") == "BULK_BUYER" else "Consumer"
    auto_msg = {
        "id": msg_id,
        "listing_id": listing["id"],
        "crop_name": listing["crop_name"],
        "from_phone": buyer["phone"],
        "from_name": buyer["name"],
        "to_phone": listing["farmer_phone"],
        "to_name": listing["farmer_name"],
        "body": f"ðŸ“¦ New Order #{new_order_id} ({role_title}): Requested {qty} KG of {listing['crop_name']} for â‚¹{total_price} (â‚¹{price_per_kg}/kg). Delivery: {new_order['delivery_address']}" + (f" | Note: {data.notes}" if data.notes else ""),
        "ts": now_iso
    }
    MESSAGES_DB.append(auto_msg)
    save_messages(MESSAGES_DB)

    return {
        "status": "SUCCESS",
        "message": f"Order #{new_order_id} for {qty} KG of {listing['crop_name']} submitted successfully!",
        "order": new_order
    }


@app.get("/api/farmer/orders")
def get_farmer_orders(farmer_phone: str):
    seller = require_seller(farmer_phone)
    return [o for o in ORDERS_DB if phones_match(o.get("farmer_phone", ""), seller["phone"])]


@app.get("/api/buyer/orders")
def get_buyer_orders(buyer_phone: str):
    buyer = require_buyer(buyer_phone)
    return [o for o in ORDERS_DB if phones_match(o.get("buyer_phone", ""), buyer["phone"])]


@app.post("/api/orders/{order_id}/accept")
def accept_order(order_id: int, farmer_phone: str):
    seller = require_seller(farmer_phone)
    order = next((o for o in ORDERS_DB if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if not phones_match(order["farmer_phone"], seller["phone"]):
        raise HTTPException(status_code=403, detail="You can only manage orders for your own crops.")
    if order["status"] != "PENDING":
        raise HTTPException(status_code=400, detail=f"Order is already {order['status'].lower()}.")

    listing = next((l for l in LISTINGS_DB if l["id"] == order["listing_id"]), None)
    remaining_kg = 0.0

    if listing:
        avail = float(listing.get("quantity_kg", 0))
        req = float(order.get("quantity_kg", 0))
        if avail < req:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot accept order: Available stock ({avail} KG) is less than requested quantity ({req} KG)."
            )
        
        listing["quantity_kg"] = round(avail - req, 1)
        remaining_kg = listing["quantity_kg"]
        if listing["quantity_kg"] <= 0:
            listing["status"] = "SOLD_OUT"
        
        save_listings(LISTINGS_DB)

    now_iso = datetime.now(timezone.utc).isoformat()
    order["status"] = "ACCEPTED"
    order["updated_at"] = now_iso
    save_orders(ORDERS_DB)

    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    accept_msg = {
        "id": msg_id,
        "listing_id": order["listing_id"],
        "crop_name": order["crop_name"],
        "from_phone": seller["phone"],
        "from_name": order["farmer_name"],
        "to_phone": order["buyer_phone"],
        "to_name": order["buyer_name"],
        "body": f"âœ… Order Accepted! Your order for {order['quantity_kg']} KG of {order['crop_name']} (â‚¹{order['total_price']}) has been confirmed and scheduled for logistics dispatch.",
        "ts": now_iso
    }
    MESSAGES_DB.append(accept_msg)
    save_messages(MESSAGES_DB)

    return {
        "message": "Order accepted! Inventory deducted and queued for logistics dispatch.",
        "order": order,
        "remaining_kg": remaining_kg
    }


@app.post("/api/orders/{order_id}/reject")
def reject_order(order_id: int, farmer_phone: str):
    seller = require_seller(farmer_phone)
    order = next((o for o in ORDERS_DB if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if not phones_match(order["farmer_phone"], seller["phone"]):
        raise HTTPException(status_code=403, detail="You can only manage orders for your own crops.")
    if order["status"] != "PENDING":
        raise HTTPException(status_code=400, detail=f"Order is already {order['status'].lower()}.")

    now_iso = datetime.now(timezone.utc).isoformat()
    order["status"] = "REJECTED"
    order["updated_at"] = now_iso
    save_orders(ORDERS_DB)

    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    reject_msg = {
        "id": msg_id,
        "listing_id": order["listing_id"],
        "crop_name": order["crop_name"],
        "from_phone": seller["phone"],
        "from_name": order["farmer_name"],
        "to_phone": order["buyer_phone"],
        "to_name": order["buyer_name"],
        "body": f"âŒ Order Declined: The request for {order['quantity_kg']} KG of {order['crop_name']} could not be accepted at this time.",
        "ts": now_iso
    }
    MESSAGES_DB.append(reject_msg)
    save_messages(MESSAGES_DB)

    return {"message": "Order declined.", "order": order}


@app.post("/api/orders/{order_id}/cancel")
def cancel_order(order_id: int, buyer_phone: str):
    buyer = require_buyer(buyer_phone)
    order = next((o for o in ORDERS_DB if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if not phones_match(order["buyer_phone"], buyer["phone"]):
        raise HTTPException(status_code=403, detail="You can only cancel your own orders.")
    if order["status"] not in ["PENDING", "ACCEPTED"]:
        raise HTTPException(status_code=400, detail=f"Order cannot be cancelled in '{order['status']}' state.")

    if order["status"] == "ACCEPTED":
        listing = next((l for l in LISTINGS_DB if l["id"] == order["listing_id"]), None)
        if listing:
            listing["quantity_kg"] = round(float(listing.get("quantity_kg", 0)) + float(order["quantity_kg"]), 1)
            listing["status"] = "ACTIVE"
            save_listings(LISTINGS_DB)

    now_iso = datetime.now(timezone.utc).isoformat()
    order["status"] = "CANCELLED"
    order["updated_at"] = now_iso
    save_orders(ORDERS_DB)

    return {"message": "Order cancelled successfully.", "order": order}


# ----- Direct In-App Chat Endpoints -----

@app.get("/api/listings/{listing_id}/messages")
def list_messages(listing_id: int, phone: str, partner_phone: Optional[str] = None):
    caller = require_user(phone)
    user_p = caller["phone"]
    
    if is_seller(caller.get("role", "")):
        if partner_phone:
            return [
                m for m in MESSAGES_DB
                if m.get("listing_id") == listing_id and (
                    (phones_match(m.get("from_phone", ""), user_p) and phones_match(m.get("to_phone", ""), partner_phone)) or
                    (phones_match(m.get("from_phone", ""), partner_phone) and phones_match(m.get("to_phone", ""), user_p))
                )
            ]
        else:
            return [
                m for m in MESSAGES_DB
                if m.get("listing_id") == listing_id and (
                    phones_match(m.get("from_phone", ""), user_p) or phones_match(m.get("to_phone", ""), user_p)
                )
            ]
    else:
        listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
        farmer_p = partner_phone or (listing["farmer_phone"] if listing else None)
        
        return [
            m for m in MESSAGES_DB
            if m.get("listing_id") == listing_id and (
                (phones_match(m.get("from_phone", ""), user_p) and (not farmer_p or phones_match(m.get("to_phone", ""), farmer_p))) or
                (phones_match(m.get("to_phone", ""), user_p) and (not farmer_p or phones_match(m.get("from_phone", ""), farmer_p)))
            )
        ]


@app.get("/api/listings/{listing_id}/conversations")
def list_conversations(listing_id: int, farmer_phone: str):
    seller = require_seller(farmer_phone)
    user_p = seller["phone"]
    
    listing_msgs = [
        m for m in MESSAGES_DB
        if m.get("listing_id") == listing_id and (
            phones_match(m.get("from_phone", ""), user_p) or phones_match(m.get("to_phone", ""), user_p)
        )
    ]
    
    buyers_map = {}
    for m in listing_msgs:
        buyer_p = m["from_phone"] if not phones_match(m["from_phone"], user_p) else m["to_phone"]
        buyer_user = find_user_by_phone(buyer_p) or {}
        buyer_n = buyer_user.get("name", m.get("from_name" if phones_match(m["from_phone"], buyer_p) else "to_name", buyer_p))
        if buyer_p not in buyers_map:
            buyers_map[buyer_p] = {
                "buyer_phone": buyer_p,
                "buyer_name": buyer_n,
                "last_message": m.get("body", ""),
                "last_ts": m.get("ts", ""),
                "msg_count": 1
            }
        else:
            buyers_map[buyer_p]["last_message"] = m.get("body", "")
            buyers_map[buyer_p]["last_ts"] = m.get("ts", "")
            buyers_map[buyer_p]["msg_count"] += 1
            
    return list(buyers_map.values())


@app.get("/api/farmer/inbox_counts")
def get_inbox_counts(farmer_phone: str):
    seller = require_seller(farmer_phone)
    user_p = seller["phone"]
    counts = {}
    for m in MESSAGES_DB:
        if phones_match(m.get("to_phone", ""), user_p) or phones_match(m.get("from_phone", ""), user_p):
            lid = m.get("listing_id", 0)
            buyer_p = m["from_phone"] if not phones_match(m["from_phone"], user_p) else m["to_phone"]
            if lid not in counts:
                counts[lid] = set()
            counts[lid].add(buyer_p)
    return {str(lid): len(buyers) for lid, buyers in counts.items()}


@app.post("/api/listings/{listing_id}/messages")
def send_message(listing_id: int, data: SendMessageSchema):
    sender = require_user(data.from_phone)
    recipient = find_user_by_phone(data.to_phone) or {}
    
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    crop_name = listing["crop_name"] if listing else "CROP"
    
    new_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    msg = {
        "id": new_id,
        "listing_id": listing_id,
        "crop_name": crop_name,
        "from_phone": sender["phone"],
        "from_name": sender.get("name", data.from_phone),
        "to_phone": data.to_phone,
        "to_name": recipient.get("name", data.to_phone),
        "body": data.body.strip(),
        "ts": datetime.now(timezone.utc).isoformat()
    }
    MESSAGES_DB.append(msg)
    save_messages(MESSAGES_DB)
    return {"message": "Message sent.", "msg": msg}


# ==========================================
# AI DEMAND FORECASTING & MARKET INTELLIGENCE
# ==========================================

CROP_BENCHMARKS = {
    "TOMATO": {"base_daily_kg": 45.0, "shelf_life": 6, "mandi_ref": 18.0, "retail_ref": 42.0, "elasticity": 1.25, "season_factor": 1.15},
    "RED ONION": {"base_daily_kg": 65.0, "shelf_life": 25, "mandi_ref": 16.0, "retail_ref": 38.0, "elasticity": 0.85, "season_factor": 1.05},
    "ONION": {"base_daily_kg": 65.0, "shelf_life": 25, "mandi_ref": 16.0, "retail_ref": 38.0, "elasticity": 0.85, "season_factor": 1.05},
    "POTATO": {"base_daily_kg": 80.0, "shelf_life": 30, "mandi_ref": 14.0, "retail_ref": 34.0, "elasticity": 0.70, "season_factor": 1.00},
    "CHILLI": {"base_daily_kg": 25.0, "shelf_life": 14, "mandi_ref": 42.0, "retail_ref": 85.0, "elasticity": 1.10, "season_factor": 1.20},
    "BANANA": {"base_daily_kg": 40.0, "shelf_life": 5, "mandi_ref": 22.0, "retail_ref": 55.0, "elasticity": 1.15, "season_factor": 1.10},
    "MANGO": {"base_daily_kg": 50.0, "shelf_life": 7, "mandi_ref": 45.0, "retail_ref": 110.0, "elasticity": 1.40, "season_factor": 1.35},
    "CARROT": {"base_daily_kg": 30.0, "shelf_life": 12, "mandi_ref": 20.0, "retail_ref": 50.0, "elasticity": 0.95, "season_factor": 1.05},
    "RICE": {"base_daily_kg": 120.0, "shelf_life": 180, "mandi_ref": 32.0, "retail_ref": 62.0, "elasticity": 0.60, "season_factor": 1.00},
    "WHEAT": {"base_daily_kg": 100.0, "shelf_life": 180, "mandi_ref": 26.0, "retail_ref": 48.0, "elasticity": 0.65, "season_factor": 1.00},
}

def _accepted_demand_by_day(crop_name: str) -> dict:
    crop = crop_name.strip().lower()
    daily = {}
    for order in ORDERS_DB:
        if str(order.get("crop_name", "")).strip().lower() != crop:
            continue
        if str(order.get("status", "")).upper() in ["REJECTED", "CANCELLED"]:
            continue
        ts = order.get("created_at")
        if not ts:
            continue
        try:
            day = datetime.fromisoformat(ts.replace("Z", "+00:00")).date().isoformat()
            daily[day] = daily.get(day, 0.0) + float(order.get("quantity_kg", 0))
        except Exception:
            continue
    return daily


@app.get("/api/ai/demand-forecast")
def demand_forecast(crop: str, days: int = 7):
    """
    AI Multi-Factor Demand Forecasting Engine:
    Combines recency-weighted linear trend regression, crop seasonal elasticity,
    historical order volume, current marketplace supply gap, and price advisory.
    """
    if not crop or not crop.strip():
        raise HTTPException(status_code=400, detail="Crop name is required.")
    days = max(1, min(int(days), 30))
    crop_clean = crop.strip().upper()
    benchmark = CROP_BENCHMARKS.get(crop_clean, {
        "base_daily_kg": 35.0,
        "shelf_life": 7,
        "mandi_ref": 20.0,
        "retail_ref": 45.0,
        "elasticity": 1.0,
        "season_factor": 1.0
    })

    history = _accepted_demand_by_day(crop_clean)
    today = datetime.now(timezone.utc).date()

    observed = []
    if history:
        first_day = min(datetime.fromisoformat(d).date() for d in history)
        start = max(first_day, today - timedelta(days=59))
        cursor = start
        while cursor <= today:
            observed.append(float(history.get(cursor.isoformat(), 0.0)))
            cursor += timedelta(days=1)

    current_supply = sum(
        float(l.get("quantity_kg", 0))
        for l in LISTINGS_DB
        if str(l.get("crop_name", "")).strip().lower() == crop_clean.lower()
    )

    if observed and len(observed) >= 2:
        n = len(observed)
        xs = list(range(n))
        weights = [1.0 + (i / max(1, n - 1)) * 2.0 for i in range(n)]
        w_sum = sum(weights)
        x_bar = sum(x * w for x, w in zip(xs, weights)) / w_sum
        y_bar = sum(y * w for y, w in zip(observed, weights)) / w_sum
        denom = sum(w * (x - x_bar) ** 2 for x, w in zip(xs, weights))
        slope = (
            sum(w * (x - x_bar) * (y - y_bar) for x, y, w in zip(xs, observed, weights)) / denom
            if denom else 0.0
        )
        intercept = y_bar - slope * x_bar
        raw_daily = max(0.0, intercept + slope * (n - 1 + 1))
        forecast_daily = (raw_daily * 0.75) + (benchmark["base_daily_kg"] * benchmark["season_factor"] * 0.25)
        avg_daily = sum(observed) / n
        trend = "rising" if slope > max(0.05, avg_daily * 0.03) else ("falling" if slope < -max(0.05, avg_daily * 0.03) else "stable")
        confidence = min(95.0, 60.0 + n * 1.5 + min(20, sum(1 for x in observed if x > 0) * 3))
        method = "Recency-Weighted Linear Trend + Seasonal Prior"
    else:
        forecast_daily = benchmark["base_daily_kg"] * benchmark["season_factor"]
        trend = "stable"
        confidence = 68.0
        method = "Agri-Market Benchmark & Seasonal Prior"

    total_forecast = round(forecast_daily * days, 1)
    recommended_stock = round(total_forecast * 1.15, 1)
    supply_gap = round(recommended_stock - current_supply, 1)

    fair_farmer_price = round(benchmark["mandi_ref"] * 1.45, 1)
    fair_consumer_price = round(benchmark["retail_ref"] * 0.75, 1)

    daily_projection = []
    for i in range(1, days + 1):
        day_date = today + timedelta(days=i)
        noise = math.sin(i * 0.8) * (forecast_daily * 0.08)
        proj_val = max(1.0, round(forecast_daily + noise, 1))
        daily_projection.append({
            "day": day_date.strftime("%a %d %b"),
            "demand_kg": proj_val
        })

    if supply_gap > 0:
        recommendation = f"High Demand Detected. Supply deficit of {supply_gap} KG expected. Farmers/FPOs should mobilize harvest to capture premium pricing."
    elif supply_gap < -100:
        recommendation = f"Market is well-supplied (surplus of {abs(supply_gap)} KG). Recommend offering batch bulk discounts to institutional buyers to avoid spoilage."
    else:
        recommendation = f"Market is balanced. Target harvesting {recommended_stock} KG over the next {days} days at recommended fair rate â‚¹{fair_farmer_price}/kg."

    return {
        "crop": crop_clean,
        "forecast_days": days,
        "forecast_daily_kg": round(forecast_daily, 1),
        "forecast_total_kg": total_forecast,
        "current_supply_kg": round(current_supply, 1),
        "recommended_stock_kg": recommended_stock,
        "supply_gap_kg": supply_gap,
        "trend": trend,
        "confidence_percent": round(confidence, 1),
        "method": method,
        "history_days": len(observed),
        "fair_farmer_price_inr": fair_farmer_price,
        "fair_consumer_price_inr": fair_consumer_price,
        "mandi_benchmark_inr": benchmark["mandi_ref"],
        "retail_benchmark_inr": benchmark["retail_ref"],
        "shelf_life_days": benchmark["shelf_life"],
        "spoilage_risk": "HIGH" if benchmark["shelf_life"] <= 6 else ("MEDIUM" if benchmark["shelf_life"] <= 14 else "LOW"),
        "recommendation": recommendation,
        "daily_projection": daily_projection
    }


# ==========================================
# SMART LOGISTICS & 2-OPT ROUTE OPTIMIZATION
# ==========================================

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Geodesic distance in kilometers adjusted for road circuity factor (~1.25)."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    crow_dist = 2 * r * math.asin(math.sqrt(a))
    return crow_dist * 1.25


def _two_opt_tsp(origin: dict, stops: list) -> list:
    """2-Opt local search improvement on top of nearest-neighbour ordering."""
    if len(stops) <= 2:
        return stops

    unvisited = list(stops)
    ordered = []
    curr_lat, curr_lon = origin["lat"], origin["lon"]

    while unvisited:
        next_s = min(unvisited, key=lambda s: _haversine_km(curr_lat, curr_lon, s["lat"], s["lon"]))
        ordered.append(next_s)
        curr_lat, curr_lon = next_s["lat"], next_s["lon"]
        unvisited.remove(next_s)

    def total_path_dist(route):
        d = _haversine_km(origin["lat"], origin["lon"], route[0]["lat"], route[0]["lon"])
        for i in range(len(route) - 1):
            d += _haversine_km(route[i]["lat"], route[i]["lon"], route[i+1]["lat"], route[i+1]["lon"])
        return d

    best_route = ordered
    best_dist = total_path_dist(best_route)
    improved = True

    while improved:
        improved = False
        for i in range(len(best_route) - 1):
            for j in range(i + 1, len(best_route)):
                new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]
                new_dist = total_path_dist(new_route)
                if new_dist < best_dist - 0.01:
                    best_route = new_route
                    best_dist = new_dist
                    improved = True
                    break
            if improved:
                break

    return best_route


@app.post("/api/logistics/optimize")
def optimize_logistics(data: RoutePlanSchema):
    """
    Logistics Route Optimizer using Nearest-Neighbour + 2-Opt Heuristic.
    Computes optimal sequence, road distance, ETA, vehicle recommendation,
    fuel cost estimate, and CO2 reduction compared to individual trips.
    """
    if not data.stops:
        raise HTTPException(status_code=400, detail="Add at least one delivery stop.")
    if data.vehicle_capacity_kg <= 0:
        raise HTTPException(status_code=400, detail="Vehicle capacity must be greater than zero.")

    total_load = sum(max(0.0, float(s.quantity_kg)) for s in data.stops)
    if total_load > data.vehicle_capacity_kg:
        raise HTTPException(
            status_code=400,
            detail=f"Total delivery load ({total_load:.1f} KG) exceeds vehicle capacity ({data.vehicle_capacity_kg:.1f} KG)."
        )

    stops_dicts = [s.model_dump() for s in data.stops]
    origin_dict = {"name": data.origin_name, "lat": data.origin_lat, "lon": data.origin_lon}

    optimized_stops = _two_opt_tsp(origin_dict, stops_dicts)

    route = []
    curr_lat, curr_lon = data.origin_lat, data.origin_lon
    total_km = 0.0

    unoptimized_km = sum(_haversine_km(data.origin_lat, data.origin_lon, s["lat"], s["lon"]) * 2 for s in stops_dicts)

    for idx, stop in enumerate(optimized_stops, 1):
        leg_km = _haversine_km(curr_lat, curr_lon, stop["lat"], stop["lon"])
        total_km += leg_km
        route.append({
            "sequence": idx,
            "name": stop["name"],
            "lat": stop["lat"],
            "lon": stop["lon"],
            "quantity_kg": round(float(stop.get("quantity_kg", 0)), 1),
            "order_id": stop.get("order_id"),
            "address": stop.get("address") or f"Stop {idx} Delivery Point",
            "phone": stop.get("phone") or "",
            "distance_from_previous_km": round(leg_km, 2)
        })
        curr_lat, curr_lon = stop["lat"], stop["lon"]

    eta_hours = total_km / 32.0 if total_km else 0
    utilization = (total_load / data.vehicle_capacity_kg) * 100

    if total_load <= 80:
        vehicle = "Electric Cargo 3-Wheeler / 2-Wheeler Fleet"
        fuel_rate_per_km = 3.5
    elif total_load <= 400:
        vehicle = "Mini Truck / Light Pickup (e.g. Tata Ace / Mahindra Bolero)"
        fuel_rate_per_km = 7.5
    elif total_load <= 1200:
        vehicle = "Medium Commercial Vehicle (e.g. Ashok Leyland Dost / Eicher Pro)"
        fuel_rate_per_km = 12.0
    else:
        vehicle = "Heavy Goods Carrier / Temperature-Controlled Reefer"
        fuel_rate_per_km = 18.0

    fuel_cost_est = round(total_km * fuel_rate_per_km, 2)
    unoptimized_fuel_cost = round(unoptimized_km * fuel_rate_per_km, 2)
    cost_savings_inr = max(0.0, round(unoptimized_fuel_cost - fuel_cost_est, 2))
    
    km_saved = max(0.0, unoptimized_km - total_km)
    co2_saved_kg = round(km_saved * 0.17, 2)

    return {
        "origin": origin_dict,
        "route": route,
        "total_distance_km": round(total_km, 2),
        "unoptimized_distance_km": round(unoptimized_km, 2),
        "distance_saved_km": round(km_saved, 2),
        "estimated_travel_hours": round(eta_hours, 2),
        "estimated_travel_minutes": round(eta_hours * 60),
        "total_load_kg": round(total_load, 1),
        "vehicle_capacity_kg": round(data.vehicle_capacity_kg, 1),
        "load_utilization_percent": round(utilization, 1),
        "recommended_vehicle": vehicle,
        "estimated_fuel_cost_inr": fuel_cost_est,
        "cost_savings_inr": cost_savings_inr,
        "co2_saved_kg": co2_saved_kg,
        "optimization_method": "2-Opt Trajectory Distance Optimization",
        "traffic_note": "Travel time uses road circuity factors (1.25x) and average semi-urban logistics speeds."
    }


@app.post("/api/logistics/dispatch")
def dispatch_trip(data: CreateTripSchema):
    """Save an active delivery trip and advance all included orders to DISPATCHED status."""
    seller = require_seller(data.farmer_phone)
    new_trip_id = max([t["id"] for t in TRIPS_DB], default=0) + 1
    now_iso = datetime.now(timezone.utc).isoformat()

    new_trip = {
        "id": new_trip_id,
        "farmer_phone": seller["phone"],
        "farmer_name": seller["name"],
        "origin_name": data.origin_name,
        "origin_lat": data.origin_lat,
        "origin_lon": data.origin_lon,
        "vehicle_type": data.vehicle_type,
        "vehicle_number": data.vehicle_number or "TS-09-UB-8821",
        "driver_name": data.driver_name or "Logistics Driver",
        "driver_phone": data.driver_phone or "+919876540000",
        "stops": [s.model_dump() for s in data.stops],
        "order_ids": data.order_ids,
        "total_distance_km": data.total_distance_km,
        "total_load_kg": data.total_load_kg,
        "estimated_travel_minutes": data.estimated_travel_minutes,
        "fuel_cost_est": data.fuel_cost_est,
        "co2_saved_kg": data.co2_saved_kg,
        "status": "DISPATCHED",
        "created_at": now_iso,
        "updated_at": now_iso
    }
    TRIPS_DB.insert(0, new_trip)
    save_trips(TRIPS_DB)

    for o in ORDERS_DB:
        if o["id"] in data.order_ids:
            o["status"] = "DISPATCHED"
            o["updated_at"] = now_iso
            msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
            MESSAGES_DB.append({
                "id": msg_id,
                "listing_id": o.get("listing_id", 0),
                "crop_name": o.get("crop_name", "CROP"),
                "from_phone": seller["phone"],
                "from_name": seller["name"],
                "to_phone": o["buyer_phone"],
                "to_name": o["buyer_name"],
                "body": f"ðŸšš Order #{o['id']} Dispatched! Vehicle: {new_trip['vehicle_type']} ({new_trip['vehicle_number']}). Driver: {new_trip['driver_name']} ({new_trip['driver_phone']}). Est. Arrival: ~{data.estimated_travel_minutes} mins.",
                "ts": now_iso
            })
    save_orders(ORDERS_DB)
    save_messages(MESSAGES_DB)

    return {"message": f"Logistics Trip #{new_trip_id} dispatched successfully!", "trip": new_trip}


@app.get("/api/logistics/trips")
def get_trips(phone: str):
    user = require_user(phone)
    user_p = user["phone"]
    if is_seller(user.get("role", "")):
        return [t for t in TRIPS_DB if phones_match(t.get("farmer_phone", ""), user_p)]
    else:
        buyer_order_ids = {o["id"] for o in ORDERS_DB if phones_match(o.get("buyer_phone", ""), user_p)}
        return [t for t in TRIPS_DB if any(oid in buyer_order_ids for oid in t.get("order_ids", []))]


@app.post("/api/logistics/trips/{trip_id}/deliver")
def mark_trip_delivered(trip_id: int, phone: str):
    seller = require_seller(phone)
    trip = next((t for t in TRIPS_DB if t["id"] == trip_id), None)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")
    if not phones_match(trip["farmer_phone"], seller["phone"]):
        raise HTTPException(status_code=403, detail="You can only manage your own logistics trips.")

    now_iso = datetime.now(timezone.utc).isoformat()
    trip["status"] = "DELIVERED"
    trip["updated_at"] = now_iso
    save_trips(TRIPS_DB)

    for o in ORDERS_DB:
        if o["id"] in trip.get("order_ids", []):
            o["status"] = "DELIVERED"
            o["updated_at"] = now_iso
            msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
            MESSAGES_DB.append({
                "id": msg_id,
                "listing_id": o.get("listing_id", 0),
                "crop_name": o.get("crop_name", "CROP"),
                "from_phone": seller["phone"],
                "from_name": seller["name"],
                "to_phone": o["buyer_phone"],
                "to_name": o["buyer_name"],
                "body": f"ðŸŽ‰ Order #{o['id']} Delivered! Thank you for purchasing directly from farmers on CropConnect.",
                "ts": now_iso
            })
    save_orders(ORDERS_DB)
    save_messages(MESSAGES_DB)

    return {"message": f"Trip #{trip_id} and all attached orders marked as DELIVERED.", "trip": trip}


# ==========================================
# SUPPLY CHAIN VALUE & FAIR PRICE ANALYTICS
# ==========================================

@app.get("/api/analytics/value-distribution")
def get_value_distribution(crop: str = "TOMATO"):
    """
    Supply Chain Inefficiencies & Value Distribution Breakdown:
    Compares Traditional Mandi multi-tier chain against CropConnect Direct Marketplace.
    """
    crop_clean = crop.strip().upper()
    benchmark = CROP_BENCHMARKS.get(crop_clean, {
        "mandi_ref": 20.0,
        "retail_ref": 45.0
    })

    farmer_mandi_price = benchmark["mandi_ref"]
    consumer_retail_price = benchmark["retail_ref"]

    cropconnect_farmer_price = round(farmer_mandi_price * 1.50, 1)
    cropconnect_logistics_cost = round(farmer_mandi_price * 0.20, 1)
    cropconnect_consumer_price = round(cropconnect_farmer_price + cropconnect_logistics_cost, 1)

    farmer_benefit_percent = round(((cropconnect_farmer_price - farmer_mandi_price) / farmer_mandi_price) * 100, 1)
    consumer_saving_percent = round(((consumer_retail_price - cropconnect_consumer_price) / consumer_retail_price) * 100, 1)
    waste_reduction_percent = 82.0

    return {
        "crop": crop_clean,
        "traditional_chain": {
            "farmer_earns_inr": farmer_mandi_price,
            "village_middleman_inr": round(farmer_mandi_price * 0.25, 1),
            "mandi_commission_inr": round(farmer_mandi_price * 0.35, 1),
            "wholesaler_margin_inr": round(farmer_mandi_price * 0.30, 1),
            "retailer_margin_inr": round(farmer_mandi_price * 0.35, 1),
            "consumer_pays_inr": consumer_retail_price,
            "post_harvest_waste_percent": 25.0
        },
        "cropconnect_direct_chain": {
            "farmer_earns_inr": cropconnect_farmer_price,
            "direct_logistics_inr": cropconnect_logistics_cost,
            "middleman_cut_inr": 0.0,
            "consumer_pays_inr": cropconnect_consumer_price,
            "post_harvest_waste_percent": 4.5
        },
        "benefits": {
            "farmer_income_increase_percent": farmer_benefit_percent,
            "consumer_price_savings_percent": consumer_saving_percent,
            "supply_chain_waste_reduction_percent": waste_reduction_percent,
            "intermediary_tiers_eliminated": 3
        }
    }


# ==========================================
# TWILIO SMS INBOUND WEBHOOK ENDPOINT
# ==========================================

@app.post("/sms/webhook")
async def twilio_sms_webhook(From: str = Form(...), Body: str = Form(...)):
    """
    Robust SMS Webhook supporting:
    - SELL <CROP> <QTY>KG <PRICE>/KG [ZIP]
    - PRICE <CROP> (Get fair market price & forecast)
    - ORDERS (Check pending orders via SMS)
    """
    farmer = find_user_by_phone(From)

    if not farmer:
        reply = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: Your phone is not registered. Please register as a Farmer or FPO on the CropConnect portal first.</Message></Response>"
        return Response(content=reply, media_type="text/xml")

    body_clean = Body.strip()
    
    # 1. Price Inquiry via SMS: "PRICE TOMATO"
    if body_clean.upper().startswith("PRICE"):
        parts = body_clean.split()
        crop_query = parts[1].upper() if len(parts) > 1 else "TOMATO"
        bench = CROP_BENCHMARKS.get(crop_query, {"mandi_ref": 20.0, "retail_ref": 45.0})
        rec_price = round(bench["mandi_ref"] * 1.45, 1)
        reply = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect AI Price Advisor: Recommended selling price for {crop_query} is Rs {rec_price}/KG (Mandi: Rs {bench['mandi_ref']}, Retail: Rs {bench['retail_ref']}). Text 'SELL {crop_query} 50KG {int(rec_price)}/KG' to list.</Message></Response>"
        return Response(content=reply, media_type="text/xml")

    # 2. Check Orders via SMS: "ORDERS"
    if body_clean.upper() == "ORDERS":
        pending = [o for o in ORDERS_DB if phones_match(o.get("farmer_phone", ""), farmer["phone"]) and o.get("status") == "PENDING"]
        if not pending:
            reply = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: You have 0 pending orders right now.</Message></Response>"
        else:
            summary = ", ".join([f"#{o['id']}: {o['quantity_kg']}kg {o['crop_name']}" for o in pending[:3]])
            reply = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: You have {len(pending)} pending orders ({summary}). Log in to accept and dispatch via Route Optimizer.</Message></Response>"
        return Response(content=reply, media_type="text/xml")

    # 3. Sell Command via SMS: SELL TOMATO 50KG 30/KG [500001]
    pattern = r'^SELL\s+([A-Za-z\s]+?)\s+(\d+(?:\.\d+)?)\s*KG\s+(\d+(?:\.\d+)?)(?:/KG)?(?:\s+(\d{5,6}))?$'
    match = re.match(pattern, body_clean, re.IGNORECASE)

    if match:
        crop, qty, price, zip_c = match.groups()
        crop_clean = crop.strip().upper()
        qty_val = float(qty)
        price_val = float(price)
        zip_val = zip_c or farmer.get("zip_code", "500001")

        new_id = max([l["id"] for l in LISTINGS_DB], default=0) + 1
        new_listing = {
            "id": new_id,
            "farmer_name": farmer["name"],
            "farmer_phone": farmer["phone"],
            "seller_type": farmer.get("role", "FARMER"),
            "crop_name": crop_clean,
            "quantity_kg": qty_val,
            "price_per_kg": price_val,
            "mandi_price_per_kg": round(price_val * 0.70, 1),
            "retail_market_price_per_kg": round(price_val * 1.40, 1),
            "min_order_kg": 5.0,
            "bulk_price_per_kg": round(price_val * 0.90, 1),
            "zip_code": str(zip_val),
            "location_name": f"Farm SMS ({zip_val})",
            "lat": 17.3850,
            "lon": 78.4867,
            "quality_grade": "Grade A Fresh",
            "harvest_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "shelf_life_days": 7,
            "source": "SMS",
            "status": "ACTIVE"
        }
        LISTINGS_DB.insert(0, new_listing)
        save_listings(LISTINGS_DB)
        reply = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: Successfully listed {qty_val}KG of {crop_clean} at Rs {price_val}/KG. Visible to consumers and bulk buyers.</Message></Response>"
    else:
        reply = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: Invalid format. Use: SELL CROP QTYKG PRICE/KG (e.g. SELL TOMATO 50KG 28/KG) or text PRICE TOMATO for fair market rates.</Message></Response>"

    return Response(content=reply, media_type="text/xml")


# ==========================================
# MULTILINGUAL SPA FRONTEND (HTML + JS)
# ==========================================

from frontend import FRONTEND_HTML

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return FRONTEND_HTML

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

