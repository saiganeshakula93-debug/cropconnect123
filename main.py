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
        "body": f"📦 New Order #{new_order_id} ({role_title}): Requested {qty} KG of {listing['crop_name']} for ₹{total_price} (₹{price_per_kg}/kg). Delivery: {new_order['delivery_address']}" + (f" | Note: {data.notes}" if data.notes else ""),
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
        "body": f"✅ Order Accepted! Your order for {order['quantity_kg']} KG of {order['crop_name']} (₹{order['total_price']}) has been confirmed and scheduled for logistics dispatch.",
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
        "body": f"❌ Order Declined: The request for {order['quantity_kg']} KG of {order['crop_name']} could not be accepted at this time.",
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
        recommendation = f"Market is balanced. Target harvesting {recommended_stock} KG over the next {days} days at recommended fair rate ₹{fair_farmer_price}/kg."

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
                "body": f"🚚 Order #{o['id']} Dispatched! Vehicle: {new_trip['vehicle_type']} ({new_trip['vehicle_number']}). Driver: {new_trip['driver_name']} ({new_trip['driver_phone']}). Est. Arrival: ~{data.estimated_travel_minutes} mins.",
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
                "body": f"🎉 Order #{o['id']} Delivered! Thank you for purchasing directly from farmers on CropConnect.",
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

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return FRONTEND_HTML

FRONTEND_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CropConnect - Direct Agri Marketplace & Smart Logistics</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    :root {
      --primary-green: #1b5e20;
      --accent-green: #2e7d32;
      --light-green: #e8f5e9;
      --accent-gold: #f59e0b;
    }
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; background-color: #f8fafc; }
    .navbar-brand { font-weight: 800; color: var(--primary-green) !important; letter-spacing: -0.5px; }
    .hero-banner { background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 60%, #43a047 100%); color: #fff; padding: 3rem 0 2.5rem; }
    .card-listing { border: none; border-radius: 14px; transition: transform 0.2s, box-shadow 0.2s; }
    .card-listing:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,0,0,0.08); }
    .lang-flag { width: 22px; height: 22px; border-radius: 50%; display:inline-block; vertical-align:middle; margin-right:4px; font-size:10px; line-height:22px; text-align:center; color:#fff; font-weight:700; }
    .lang-en{background:#3b82f6;} .lang-hi{background:#f59e0b;} .lang-te{background:#ef4444;} .lang-ta{background:#10b981;}
    .chat-bubble { max-width: 82%; word-break: break-word; }
    .chat-msg-self { background-color: var(--accent-green); color: #fff; border-bottom-right-radius: 2px; }
    .chat-msg-other { background-color: #ffffff; color: #212529; border: 1px solid #e2e8f0; border-bottom-left-radius: 2px; }
    .chat-box { height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
    .smart-card { border: 0; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,.04); }
    .metric-box { border-radius: 12px; background: #ffffff; border: 1px solid #e2e8f0; padding: 1rem; }
    .route-stop-item { border-left: 4px solid var(--accent-green); background: #ffffff; border-radius: 8px; }
    .ai-pill { background: rgba(46, 125, 50, 0.12); color: var(--primary-green); font-weight: 600; }
    .nav-tabs .nav-link { color: #475569; font-weight: 600; border: none; border-bottom: 3px solid transparent; padding: 0.75rem 1.25rem; }
    .nav-tabs .nav-link.active { color: var(--primary-green); border-bottom-color: var(--primary-green); background: transparent; }
    .price-tag { font-size: 1.35rem; font-weight: 800; color: #0f172a; }
    .badge-fpo { background-color: #7c3aed; color: #fff; }
    .badge-farmer { background-color: #059669; color: #fff; }
    .badge-consumer { background-color: #0284c7; color: #fff; }
    .badge-bulk { background-color: #d97706; color: #fff; }
  </style>
</head>
<body>

  <!-- Top Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm sticky-top">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#" onclick="switchTab('marketplace'); return false;">
        <i class="bi bi-flower1 text-success fs-2 me-2"></i>
        <span>CropConnect</span>
      </a>
      
      <div class="d-flex align-items-center gap-2">
        <!-- Language dropdown -->
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center" type="button" data-bs-toggle="dropdown">
            <i class="bi bi-translate me-1"></i> <span id="langLabel">English</span>
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow">
            <li><a class="dropdown-item" href="#" onclick="setLang('en');return false;"><span class="lang-flag lang-en">EN</span>English</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('hi');return false;"><span class="lang-flag lang-hi">हि</span>हिन्दी (Hindi)</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('te');return false;"><span class="lang-flag lang-te">తె</span>తెలుగు (Telugu)</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('ta');return false;"><span class="lang-flag lang-ta">த</span>தமிழ் (Tamil)</a></li>
          </ul>
        </div>

        <div id="navAuthBtns" class="d-flex gap-2">
          <button class="btn btn-outline-success btn-sm fw-semibold" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')" data-i18n="login">Log In</button>
          <button class="btn btn-success btn-sm fw-semibold" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('register')" data-i18n="register">Register</button>
        </div>

        <div id="navUserArea" class="d-none align-items-center gap-2">
          <span class="badge" id="navUserBadge"></span>
          <span class="fw-bold text-dark small" id="navUserName"></span>
          <button class="btn btn-outline-danger btn-sm py-1 px-2" onclick="logout()" title="Logout"><i class="bi bi-box-arrow-right"></i></button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Hero Header -->
  <section class="hero-banner">
    <div class="container text-center">
      <span class="badge rounded-pill ai-pill bg-white text-success px-3 py-1 mb-2">
        <i class="bi bi-stars me-1"></i> <span data-i18n="tagline_badge">Direct Digital Agri Marketplace + Smart AI Logistics</span>
      </span>
      <h1 class="fw-bold mb-2" data-i18n="hero_title">Empowering Farmers & Buyers Directly</h1>
      <p class="lead mb-3 text-white-50 small" data-i18n="hero_subtitle">Fair prices for farmers (+45%), lower prices for consumers (-25%), zero middleman waste, and AI route optimization.</p>
      
      <!-- SMS Banner Hint -->
      <div class="d-inline-flex align-items-center bg-dark bg-opacity-25 border border-white border-opacity-25 rounded-pill px-3 py-1 text-white small">
        <i class="bi bi-phone-vibrate me-2 text-warning"></i>
        <span><span data-i18n="sms_hint">Farmers list via SMS:</span> <code class="text-warning fw-bold">SELL TOMATO 50KG 28/KG</code></span>
      </div>
    </div>
  </section>

  <!-- Navigation Tabs Bar -->
  <div class="bg-white border-bottom shadow-sm">
    <div class="container">
      <ul class="nav nav-tabs border-bottom-0" id="mainAppTabs">
        <li class="nav-item">
          <button class="nav-link active" onclick="switchTab('marketplace')" id="tab-marketplace">
            <i class="bi bi-shop me-1 text-success"></i> <span data-i18n="nav_marketplace">Marketplace</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('orders')" id="tab-orders">
            <i class="bi bi-box-seam me-1 text-primary"></i> <span data-i18n="nav_orders">Orders & Requests</span>
            <span class="badge bg-danger rounded-pill ms-1 d-none" id="tabOrdersBadge">0</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('ai')" id="tab-ai">
            <i class="bi bi-graph-up-arrow me-1 text-warning"></i> <span data-i18n="nav_ai">AI Demand Forecast</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('logistics')" id="tab-logistics">
            <i class="bi bi-truck me-1 text-info"></i> <span data-i18n="nav_logistics">Smart Logistics & Route</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('analytics')" id="tab-analytics">
            <i class="bi bi-pie-chart-fill me-1 text-purple"></i> <span data-i18n="nav_value">Fair Price & Value Chain</span>
          </button>
        </li>
      </ul>
    </div>
  </div>

  <main class="container my-4">

    <!-- TAB 1: DIGITAL MARKETPLACE -->
    <div id="view-marketplace" class="tab-pane-view">
      <!-- Search & Filters -->
      <div class="card smart-card bg-white p-3 mb-4">
        <div class="row g-2 align-items-center">
          <div class="col-md-4">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0"><i class="bi bi-search text-muted"></i></span>
              <input type="text" id="searchInput" class="form-control border-start-0" oninput="fetchListings()" placeholder="Search crop (e.g. Tomato, Red Onion)..." data-i18n-attr="placeholder" data-i18n="search_placeholder">
            </div>
          </div>
          <div class="col-md-3">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0"><i class="bi bi-geo-alt text-muted"></i></span>
              <input type="text" id="zipInput" class="form-control border-start-0" oninput="fetchListings()" placeholder="Pincode (e.g. 500001)..." data-i18n-attr="placeholder" data-i18n="zip_placeholder">
            </div>
          </div>
          <div class="col-md-3">
            <select id="sellerTypeFilter" class="form-select" onchange="fetchListings()">
              <option value="" data-i18n="filter_all_sellers">All Sellers (Farmers & FPOs)</option>
              <option value="FARMER" data-i18n="filter_farmers_only">Individual Farmers Only</option>
              <option value="FPO" data-i18n="filter_fpos_only">FPO Collectives Only</option>
            </select>
          </div>
          <div class="col-md-2 d-flex gap-2">
            <button class="btn btn-success w-100 fw-semibold" onclick="fetchListings()" data-i18n="filter_btn">Search</button>
            <button class="btn btn-outline-success d-none" id="farmerAddListingBtn" onclick="openCreateListingModal()" title="Add Crop Listing">
              <i class="bi bi-plus-lg"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Seller Quick Inventory Bar (Visible when Farmer/FPO logged in) -->
      <div id="sellerDashboardBox" class="card smart-card border-success border-opacity-25 bg-light p-3 mb-4 d-none">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h5 class="fw-bold text-success mb-1"><i class="bi bi-speedometer2 me-2"></i><span data-i18n="seller_portal">Seller Hub</span></h5>
            <p class="text-muted small mb-0" data-i18n="seller_portal_desc">Manage your harvest inventory, orders, and 1-click logistics route dispatch.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-success btn-sm fw-semibold" onclick="openCreateListingModal()">
              <i class="bi bi-plus-circle me-1"></i> <span data-i18n="add_listing">+ Add Listing</span>
            </button>
            <button class="btn btn-outline-primary btn-sm fw-semibold" onclick="switchTab('logistics')">
              <i class="bi bi-truck me-1"></i> <span data-i18n="route_dispatch">Logistics Dispatch</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Listings Grid -->
      <div class="row g-4" id="listingsContainer"></div>
      <div id="noListings" class="text-center text-muted d-none my-5 py-5">
        <i class="bi bi-basket3 fs-1 text-muted d-block mb-2"></i>
        <span data-i18n="no_listings">No active crop listings found matching your search.</span>
      </div>
    </div>

    <!-- TAB 2: ORDERS & BATCH REQUESTS -->
    <div id="view-orders" class="tab-pane-view d-none">
      <div class="card smart-card bg-white p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1"><i class="bi bi-box-seam me-2 text-success"></i><span id="ordersTitleText" data-i18n="orders_title">Orders & Batch Requests</span></h4>
            <p class="text-muted small mb-0" data-i18n="orders_desc">Real-time status tracking from purchase request to verified farm-to-door delivery.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-success btn-sm" onclick="fetchOrdersData()">
              <i class="bi bi-arrow-clockwise me-1"></i> <span data-i18n="refresh">Refresh</span>
            </button>
            <button class="btn btn-primary btn-sm d-none" id="orderAutoDispatchBtn" onclick="autoLoadOrdersToLogistics()">
              <i class="bi bi-truck me-1"></i> <span data-i18n="plan_route_from_orders">Plan Delivery Route</span>
            </button>
          </div>
        </div>

        <div id="ordersTableContainer">
          <div class="text-center py-5 text-muted">
            <span class="spinner-border spinner-border-sm me-2"></span><span data-i18n="loading">Loading orders...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: AI DEMAND FORECASTING -->
    <div id="view-ai" class="tab-pane-view d-none">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="card smart-card bg-white p-4 h-100">
            <h5 class="fw-bold text-success mb-3"><i class="bi bi-magic me-2"></i><span data-i18n="ai_forecast_config">Forecast Query</span></h5>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary" data-i18n="crop_name">Select / Enter Crop</label>
              <select id="forecastCropSelect" class="form-select mb-2" onchange="syncForecastCropInput(this.value)">
                <option value="TOMATO">TOMATO (Tomato)</option>
                <option value="RED ONION">RED ONION (Red Onion)</option>
                <option value="POTATO">POTATO (Potato)</option>
                <option value="CHILLI">CHILLI (Green / Red Chilli)</option>
                <option value="BANANA">BANANA (Banana)</option>
                <option value="MANGO">MANGO (Mango)</option>
                <option value="CARROT">CARROT (Carrot)</option>
                <option value="RICE">RICE (Paddy / Rice)</option>
                <option value="WHEAT">WHEAT (Wheat)</option>
              </select>
              <input type="text" id="forecastCropInput" class="form-control" placeholder="Or type custom crop..." value="TOMATO">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary" data-i18n="forecast_horizon">Forecast Horizon</label>
              <select id="forecastDaysSelect" class="form-select">
                <option value="7">Next 7 Days</option>
                <option value="14">Next 14 Days</option>
                <option value="30">Next 30 Days</option>
              </select>
            </div>
            <button class="btn btn-success w-100 py-2 fw-semibold" onclick="runAIDemandForecast()">
              <i class="bi bi-cpu-fill me-1"></i> <span data-i18n="run_forecast_btn">Generate AI Forecast</span>
            </button>
            
            <hr class="my-4">
            <div class="small text-muted">
              <h6 class="fw-bold text-dark small mb-1"><i class="bi bi-info-circle me-1 text-primary"></i>How the AI Engine Works:</h6>
              <ul class="ps-3 mb-0" style="font-size:0.82rem;">
                <li>Recency-weighted regression on real marketplace order transactions.</li>
                <li>Crop-specific perishability & seasonal elasticity weighting.</li>
                <li>Dynamic equilibrium pricing model balancing farmer profit vs buyer affordability.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card smart-card bg-white p-4 h-100" id="forecastResultsCard">
            <div class="text-center py-5 text-muted">
              <i class="bi bi-bar-chart-line fs-1 text-muted d-block mb-2"></i>
              <p data-i18n="ai_forecast_prompt">Select a crop and click 'Generate AI Forecast' to view demand projections & price advice.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: SMART LOGISTICS & ROUTE OPTIMIZATION -->
    <div id="view-logistics" class="tab-pane-view d-none">
      <div class="card smart-card bg-white p-4 mb-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1"><i class="bi bi-truck me-2 text-success"></i><span data-i18n="logistics_title">Smart Logistics & Route Optimizer</span></h4>
            <p class="text-muted small mb-0" data-i18n="logistics_desc">2-Opt trajectory optimization reduces road miles, fuel costs, and spoilage during multi-drop harvest delivery.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-success btn-sm" onclick="autoLoadOrdersToLogistics()">
              <i class="bi bi-magic me-1"></i> <span data-i18n="auto_import_orders">Auto-Import Accepted Orders</span>
            </button>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-lg-5">
            <div class="p-3 bg-light rounded-3">
              <h6 class="fw-bold text-dark mb-3"><i class="bi bi-geo-alt-fill text-danger me-1"></i>Hub Origin & Vehicle Capacity</h6>
              <div class="row g-2 mb-3">
                <div class="col-12">
                  <label class="form-label small fw-semibold text-secondary">Origin Hub Name</label>
                  <input id="originName" class="form-control form-control-sm" value="Shamshabad Agri Hub / Central Warehouse">
                </div>
                <div class="col-6">
                  <label class="form-label small fw-semibold text-secondary">Origin Lat</label>
                  <input id="originLat" type="number" step="any" class="form-control form-control-sm" value="17.2500">
                </div>
                <div class="col-6">
                  <label class="form-label small fw-semibold text-secondary">Origin Lon</label>
                  <input id="originLon" type="number" step="any" class="form-control form-control-sm" value="78.4200">
                </div>
                <div class="col-12">
                  <label class="form-label small fw-semibold text-secondary">Vehicle Capacity (KG)</label>
                  <input id="vehicleCapacity" type="number" class="form-control form-control-sm" value="800">
                </div>
              </div>

              <h6 class="fw-bold text-dark mb-2"><i class="bi bi-signpost-split text-success me-1"></i>Delivery Waypoint Stops</h6>
              <p class="text-muted" style="font-size:0.78rem;">Format per line: <code>Buyer Name, Lat, Lon, KG, [Address]</code></p>
              <textarea id="routeStops" class="form-control font-monospace mb-3" rows="6" placeholder="Wholesale Mart Begumpet, 17.4435, 78.4738, 150, Secunderabad&#10;Green Valley Apt Banjara Hills, 17.4156, 78.4350, 25, Road 12&#10;Kukatpally Supermarket, 17.4933, 78.3995, 200, Main Road&#10;Madhapur Organic Store, 17.4483, 78.3915, 80, Hitec City"></textarea>

              <button class="btn btn-success w-100 fw-semibold" onclick="runRouteOptimizer()">
                <i class="bi bi-signpost-2-fill me-1"></i> <span data-i18n="optimize_route_btn">Optimize Delivery Route</span>
              </button>
            </div>
          </div>

          <div class="col-lg-7">
            <div id="routeResultsBox" class="p-3 bg-light rounded-3 h-100">
              <div class="text-center py-5 text-muted">
                <i class="bi bi-map fs-1 text-muted d-block mb-2"></i>
                <span data-i18n="route_prompt">Add waypoint stops and click 'Optimize Delivery Route' to generate the most efficient drop sequence.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Dispatched Trips History -->
        <div class="mt-5">
          <h5 class="fw-bold text-dark mb-3"><i class="bi bi-clock-history me-2 text-primary"></i><span data-i18n="active_trips_title">Active Logistics Trips</span></h5>
          <div id="tripsListContainer">
            <p class="text-muted small">Loading active trips...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: FAIR PRICING & VALUE CHAIN TRANSPARENCY -->
    <div id="view-analytics" class="tab-pane-view d-none">
      <div class="card smart-card bg-white p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1"><i class="bi bi-pie-chart-fill me-2 text-success"></i><span data-i18n="fair_price_title">Fair Pricing & Middleman Elimination Breakdown</span></h4>
            <p class="text-muted small mb-0" data-i18n="fair_price_desc">See exactly how direct farm linkage boosts farmer realization and cuts consumer prices.</p>
          </div>
          <div class="d-flex gap-2 align-items-center">
            <label class="small fw-semibold text-secondary mb-0">Crop:</label>
            <select id="valueCropSelect" class="form-select form-select-sm" onchange="fetchValueDistribution(this.value)">
              <option value="TOMATO">TOMATO</option>
              <option value="RED ONION">RED ONION</option>
              <option value="POTATO">POTATO</option>
              <option value="CHILLI">CHILLI</option>
              <option value="BANANA">BANANA</option>
              <option value="MANGO">MANGO</option>
            </select>
          </div>
        </div>

        <div id="valueDistributionContent">
          <div class="text-center py-5 text-muted">
            <span class="spinner-border spinner-border-sm me-2"></span>Loading value distribution model...
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- ============ MODALS ============ -->

  <!-- Auth Modal -->
  <div class="modal fade" id="authModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow-lg rounded-4">
        <div class="modal-header border-bottom-0 pb-0">
          <ul class="nav nav-tabs border-bottom-0" id="authTabs">
            <li class="nav-item">
              <button class="nav-link active fw-bold" id="login-tab" data-bs-toggle="tab" data-bs-target="#login-pane" data-i18n="login">Log In</button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-bold" id="register-tab" data-bs-toggle="tab" data-bs-target="#register-pane" data-i18n="register">Register</button>
            </li>
          </ul>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-4">
          <div class="tab-content">
            <!-- LOGIN FORM -->
            <div class="tab-pane fade show active" id="login-pane">
              <form onsubmit="handleLogin(event)">
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="role_label">Account Role</label>
                  <select class="form-select" id="loginRole">
                    <option value="FARMER">🧑‍🌾 Farmer (Individual)</option>
                    <option value="FPO">🚜 FPO (Farmer Producer Org / Collective)</option>
                    <option value="BULK_BUYER">🏢 Bulk / Wholesale Buyer (Supermarkets, Hotels)</option>
                    <option value="CONSUMER">🛒 Direct Consumer (Retail / Household)</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="loginPhone" required placeholder="+919876543210 or 9876543210">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="loginPassword" required placeholder="Password">
                </div>
                <button type="submit" class="btn btn-success w-100 py-2 fw-semibold" data-i18n="sign_in">Sign In</button>
                <div class="alert alert-light border small mt-3 mb-0">
                  <strong>Demo Accounts:</strong><br>
                  Farmer: <code>+919876543210</code> / <code>password123</code><br>
                  FPO: <code>+919876543220</code> / <code>password123</code><br>
                  Bulk Buyer: <code>+919876543211</code> / <code>password123</code><br>
                  Consumer: <code>+919876543230</code> / <code>password123</code>
                </div>
              </form>
            </div>
            <!-- REGISTER FORM -->
            <div class="tab-pane fade" id="register-pane">
              <form onsubmit="handleRegister(event)">
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="role_label">Account Role</label>
                  <select class="form-select" id="regRole">
                    <option value="FARMER">🧑‍🌾 Farmer (Individual Smallholder)</option>
                    <option value="FPO">🚜 FPO (Farmer Producer Organization)</option>
                    <option value="BULK_BUYER">🏢 Bulk / Institutional Buyer</option>
                    <option value="CONSUMER">🛒 Direct Household Consumer</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="name_placeholder">Full / Business Name</label>
                  <input type="text" class="form-control" id="regName" required placeholder="e.g. Ramesh Kumar or Telangana Kisan FPO">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="regPhone" required placeholder="e.g. +919876543210">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="zip_code">Pin Code / Zip</label>
                  <input type="text" class="form-control" id="regZip" required placeholder="e.g. 500001">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="regPassword" required placeholder="Create password">
                </div>
                <button type="submit" class="btn btn-success w-100 py-2 fw-semibold" data-i18n="create_account">Create Account</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add / Edit Listing Modal -->
  <div class="modal fade" id="listingModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow-lg rounded-4">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title fw-bold" id="listingModalTitle" data-i18n="new_listing_title">Add Crop Listing</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSaveListing(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="listingId">
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="crop_name">Crop Name</label>
              <input type="text" class="form-control" id="listingCrop" required placeholder="e.g. TOMATO, RED ONION, POTATO">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="quantity_kg">Available Quantity (KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingQty" required placeholder="e.g. 250">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Price per KG (₹)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingPrice" required placeholder="e.g. 28">
              </div>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold">Min Order Qty (KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingMinQty" value="5" placeholder="5">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Bulk Discount Rate (₹/KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingBulkPrice" placeholder="Optional">
              </div>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="zip_code">Pin Code</label>
                <input type="text" class="form-control" id="listingZip" required placeholder="e.g. 500001">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Shelf Life (Days)</label>
                <input type="number" class="form-control" id="listingShelfLife" value="7" placeholder="7">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold">Quality Grade / Description</label>
              <input type="text" class="form-control" id="listingGrade" value="Grade A - Freshly Harvested" placeholder="e.g. Organic Grade A">
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" data-i18n="cancel">Cancel</button>
            <button type="submit" class="btn btn-success fw-semibold" data-i18n="save">Save Listing</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Place Order Modal -->
  <div class="modal fade" id="orderModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow-lg rounded-4">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title fw-bold" id="orderModalTitle" data-i18n="request_order_title">Order Fresh Crop Batch</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSubmitOrder(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="orderListingId">
            <input type="hidden" id="orderPricePerKg">
            <input type="hidden" id="orderBulkPricePerKg">

            <div class="alert alert-light border mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="fw-bold text-success fs-5" id="orderCropName">TOMATO</span>
                <span class="badge bg-success-subtle text-success fs-6" id="orderPriceBadge">₹28/kg</span>
              </div>
              <small class="text-muted d-block">
                <span data-i18n="seller">Seller</span>: <strong id="orderFarmerName">Ramesh Kumar</strong> (<span id="orderFarmerPhone"></span>)
              </small>
              <small class="text-muted d-block">
                <span data-i18n="available_stock">Available Stock</span>: <strong id="orderAvailableQty" class="text-dark">450</strong> KG
              </small>
              <small class="text-muted d-block">
                <span>Minimum Order</span>: <strong id="orderMinQty" class="text-primary">5</strong> KG
              </small>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="request_qty">Quantity to Buy (KG)</label>
              <input type="number" step="any" min="1" class="form-control form-control-lg fw-bold" id="orderQuantityInput" oninput="updateOrderTotal()" required>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="delivery_address">Delivery Address / Destination</label>
              <input type="text" class="form-control" id="orderDeliveryAddress" required placeholder="e.g. Plot 14, Banjara Hills, Hyderabad">
            </div>

            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold">Delivery Lat</label>
                <input type="number" step="any" class="form-control form-control-sm" id="orderDeliveryLat" value="17.4156">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Delivery Lon</label>
                <input type="number" step="any" class="form-control form-control-sm" id="orderDeliveryLon" value="78.4350">
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="order_notes">Delivery Instructions / Notes (Optional)</label>
              <textarea class="form-control" id="orderNotesInput" rows="2" placeholder="e.g. Morning delivery preferred before 10 AM"></textarea>
            </div>

            <div class="p-3 bg-light rounded-3 border d-flex justify-content-between align-items-center">
              <div>
                <small class="text-muted d-block">Total Estimated Price:</small>
                <span class="fs-4 fw-bold text-success" id="orderTotalPriceEst">₹0</span>
              </div>
              <div class="text-end">
                <span class="badge bg-success-subtle text-success border" id="orderSavingsBadge">Direct Farm Savings</span>
              </div>
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" data-i18n="cancel">Cancel</button>
            <button type="submit" class="btn btn-success fw-semibold" data-i18n="submit_order_btn">Confirm & Place Order</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Chat Modal -->
  <div class="modal fade" id="chatModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content border-0 shadow-lg rounded-4">
        <div class="modal-header bg-success text-white">
          <div>
            <h5 class="modal-title fw-bold mb-0"><i class="bi bi-chat-dots-fill me-2"></i><span id="chatCropTitle">Crop Chat</span></h5>
            <small class="text-white-50" id="chatPartnerTitle"></small>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        
        <!-- Farmer Buyer Selection Tabs Bar -->
        <div id="farmerBuyerBar" class="d-none bg-light p-2 border-bottom">
          <small class="text-muted d-block mb-1 fw-semibold" data-i18n="select_buyer">Buyer Inquiries:</small>
          <div class="d-flex gap-1 flex-wrap" id="farmerBuyerPills"></div>
        </div>

        <div class="modal-body p-3 bg-light">
          <div class="chat-box" id="chatMessagesList">
            <p class="text-muted small text-center my-auto" data-i18n="loading">Loading messages...</p>
          </div>
        </div>
        <div class="modal-footer p-2 bg-white">
          <form class="input-group" onsubmit="handleSendMessage(event)" id="chatForm">
            <input type="text" class="form-control" id="chatInputText" required placeholder="Type a message..." data-i18n-attr="placeholder" data-i18n="type_message">
            <button class="btn btn-success" type="submit" id="chatSendBtn">
              <i class="bi bi-send-fill me-1"></i> <span data-i18n="send">Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // ============ Multilingual i18n Dictionaries ============
    const I18N = {
      en: {
        app_name: "CropConnect",
        hero_title: "Empowering Farmers & Buyers Directly",
        hero_subtitle: "Fair prices for farmers (+45%), lower prices for consumers (-25%), zero middleman waste, and AI route optimization.",
        tagline_badge: "Direct Digital Agri Marketplace + Smart AI Logistics",
        sms_hint: "Farmers list via SMS:",
        login: "Log In", register: "Register", logout: "Logout",
        nav_marketplace: "Marketplace", nav_orders: "Orders & Requests",
        nav_ai: "AI Demand Forecast", nav_logistics: "Smart Logistics & Route",
        nav_value: "Fair Price & Value Chain",
        search_placeholder: "Search crop (e.g. Tomato, Red Onion)...",
        zip_placeholder: "Pincode (e.g. 500001)...",
        filter_all_sellers: "All Sellers (Farmers & FPOs)",
        filter_farmers_only: "Individual Farmers Only",
        filter_fpos_only: "FPO Collectives Only",
        filter_btn: "Search", add_listing: "+ Add Listing",
        seller_portal: "Seller Hub",
        seller_portal_desc: "Manage your harvest inventory, orders, and 1-click logistics route dispatch.",
        route_dispatch: "Logistics Dispatch",
        no_listings: "No active crop listings found matching your search.",
        kg_left: "KG Left", min_order: "Min Order",
        market_benchmark: "Retail Supermarket:",
        farmer_gain: "Farmer earns +45% more",
        consumer_save: "Save 25% vs Retail",
        chat_seller: "Chat with Seller", order_now: "Order Batch / Retail",
        orders_title: "Orders & Batch Requests",
        orders_desc: "Real-time status tracking from purchase request to verified farm-to-door delivery.",
        refresh: "Refresh", plan_route_from_orders: "Plan Delivery Route",
        crop_name: "Crop Name", seller: "Seller", quantity_kg: "Quantity (KG)",
        total_price: "Total Price", status: "Status", actions: "Actions",
        status_pending: "Pending", status_accepted: "Accepted",
        status_rejected: "Declined", status_dispatched: "Dispatched",
        status_delivered: "Delivered", status_cancelled: "Cancelled",
        accept: "Accept", decline: "Decline", chat: "Chat", cancel_order: "Cancel",
        new_listing_title: "Add Crop Listing", edit_listing_title: "Edit Crop Listing",
        save: "Save Listing", cancel: "Cancel",
        request_order_title: "Order Fresh Crop Batch",
        request_qty: "Quantity to Buy (KG)", delivery_address: "Delivery Address / Destination",
        order_notes: "Delivery Instructions / Notes", submit_order_btn: "Confirm & Place Order",
        available_stock: "Available Stock",
        ai_forecast_config: "Forecast Query", forecast_horizon: "Forecast Horizon",
        run_forecast_btn: "Generate AI Forecast", ai_forecast_prompt: "Select a crop and click 'Generate AI Forecast' to view demand projections & price advice.",
        logistics_title: "Smart Logistics & Route Optimizer",
        logistics_desc: "2-Opt trajectory optimization reduces road miles, fuel costs, and spoilage during multi-drop harvest delivery.",
        auto_import_orders: "Auto-Import Accepted Orders",
        optimize_route_btn: "Optimize Delivery Route",
        route_prompt: "Add waypoint stops and click 'Optimize Delivery Route' to generate the most efficient drop sequence.",
        active_trips_title: "Active Logistics Trips",
        fair_price_title: "Fair Pricing & Middleman Elimination Breakdown",
        fair_price_desc: "See exactly how direct farm linkage boosts farmer realization and cuts consumer prices.",
        type_message: "Type a message...", send: "Send",
        select_buyer: "Buyer Inquiries:", loading: "Loading...",
        you: "You"
      },
      hi: {
        app_name: "क्रॉपकनेक्ट",
        hero_title: "किसानों और उपभोक्ताओं का सीधा डिजिटल बाज़ार",
        hero_subtitle: "किसानों को अधिक लाभ (+45%), उपभोक्ताओं को कम दाम (-25%), शून्य बिचौलिया और AI रूट लॉजिस्टिक्स।",
        tagline_badge: "सीधा डिजिटल बाज़ार + स्मार्ट AI लॉजिस्टिक्स",
        sms_hint: "किसान SMS भेजें:",
        login: "लॉग इन", register: "पंजीकरण", logout: "लॉग आउट",
        nav_marketplace: "बाज़ार (Marketplace)", nav_orders: "ऑर्डर व अनुरोध",
        nav_ai: "AI मांग पूर्वानुमान", nav_logistics: "स्मार्ट लॉजिस्टिक्स व रूट",
        nav_value: "उचित मूल्य व बचत विश्लेषण",
        search_placeholder: "फसल खोजें (जैसे टमाटर, प्याज)...",
        zip_placeholder: "पिन कोड (जैसे 500001)...",
        filter_all_sellers: "सभी विक्रेता (किसान व FPO)",
        filter_farmers_only: "केवल व्यक्तिगत किसान",
        filter_fpos_only: "केवल FPO समूह",
        filter_btn: "खोजें", add_listing: "+ फसल जोड़ें",
        seller_portal: "विक्रेता केंद्र (Seller Hub)",
        seller_portal_desc: "अपनी फसल सूची, ऑर्डर और 1-क्लिक लॉजिस्टिक्स डिलीवरी प्रबंधित करें।",
        route_dispatch: "लॉजिस्टिक्स डिस्पैच",
        no_listings: "कोई सक्रिय फसल सूची नहीं मिली।",
        kg_left: "किलो शेष", min_order: "न्यूनतम ऑर्डर",
        market_benchmark: "खुदरा बाज़ार दर:",
        farmer_gain: "किसान को +45% अधिक लाभ",
        consumer_save: "खुदरा से 25% बचत",
        chat_seller: "विक्रेता से चैट करें", order_now: "ऑर्डर करें",
        orders_title: "ऑर्डर और बैच अनुरोध",
        orders_desc: "खेत से उपभोक्ता तक सीधी डिलीवरी ट्रैकिंग।",
        refresh: "ताज़ा करें", plan_route_from_orders: "डिलीवरी रूट बनाएं",
        crop_name: "फसल का नाम", seller: "विक्रेता", quantity_kg: "मात्रा (किलो)",
        total_price: "कुल मूल्य", status: "स्थिति", actions: "कार्रवाई",
        status_pending: "लंबित", status_accepted: "स्वीकृत",
        status_rejected: "अस्वीकृत", status_dispatched: "रवाना (Dispatched)",
        status_delivered: "वितरित (Delivered)", status_cancelled: "रद्द",
        accept: "स्वीकार करें", decline: "अस्वीकार", chat: "चैट", cancel_order: "रद्द करें",
        new_listing_title: "नई फसल सूची जोड़ें", edit_listing_title: "फसल सूची संपादित करें",
        save: "सहेजें", cancel: "रद्द करें",
        request_order_title: "ताज़ी फसल का ऑर्डर दें",
        request_qty: "खरीदने की मात्रा (किलो)", delivery_address: "डिलीवरी का पता",
        order_notes: "डिलीवरी निर्देश / टिप्पणी", submit_order_btn: "ऑर्डर की पुष्टि करें",
        available_stock: "उपलब्ध स्टॉक",
        ai_forecast_config: "पूर्वानुमान खोज", forecast_horizon: "पूर्वानुमान अवधि",
        run_forecast_btn: "AI पूर्वानुमान चलाएं", ai_forecast_prompt: "मांग और मूल्य सलाह देखने के लिए फसल चुनें।",
        logistics_title: "स्मार्ट लॉजिस्टिक्स व रूट ऑप्टिमाइज़र",
        logistics_desc: "2-Opt रूटिंग दूरी, ईंधन लागत और फसल के खराब होने को कम करती है।",
        auto_import_orders: "स्वीकृत ऑर्डर स्वतः जोड़ें",
        optimize_route_btn: "रूट ऑप्टिमाइज़ करें",
        route_prompt: "रूट तैयार करने के लिए स्टॉप जोड़ें।",
        active_trips_title: "सक्रिय लॉजिस्टिक्स ट्रिप",
        fair_price_title: "उचित मूल्य व बिचौलिया उन्मूलन",
        fair_price_desc: "देखें कि सीधे बाज़ार से किसानों और उपभोक्ताओं को कितना लाभ होता है।",
        type_message: "संदेश लिखें...", send: "भेजें",
        select_buyer: "खरीदार पूछताछ:", loading: "लोड हो रहा है...",
        you: "आप"
      },
      te: {
        app_name: "క్రాప్‌కనెక్ట్",
        hero_title: "రైతులు మరియు కొనుగోలుదారుల ప్రత్యక్ష వేదిక",
        hero_subtitle: "రైతులకు అధిక లాభం (+45%), కొనుగోలుదారులకు తక్కువ ధర (-25%), దళారులు లేని నేరుగా సరఫరా & AI రవాణా.",
        tagline_badge: "ప్రత్యక్ష డిజిటల్ మార్కెట్ + స్మార్ట్ AI లాజిస్టిక్స్",
        sms_hint: "రైతులు SMS పంపండి:",
        login: "లాగిన్", register: "నమోదు", logout: "లాగౌట్",
        nav_marketplace: "మార్కెట్ (Marketplace)", nav_orders: "ఆర్డర్లు & అభ్యర్థనలు",
        nav_ai: "AI డిమాండ్ అంచనా", nav_logistics: "స్మార్ట్ లాజిస్టిక్స్ & రూట్",
        nav_value: "ధర & విలువ విశ్లేషణ",
        search_placeholder: "పంటను శోధించండి (ఉదా: టమోటా)...",
        zip_placeholder: "పిన్ కోడ్ (ఉదా: 500001)...",
        filter_all_sellers: "అందరూ అమ్మకందారులు (రైతులు & FPOలు)",
        filter_farmers_only: "రైతులు మాత్రమే",
        filter_fpos_only: "FPO సంఘాలు మాత్రమే",
        filter_btn: "శోధించు", add_listing: "+ పంటను జోడించండి",
        seller_portal: "విక్రేత కేంద్రం (Seller Hub)",
        seller_portal_desc: "మీ పంట నిల్వలు, ఆర్డర్లు మరియు డెలివరీ రూట్‌ను నిర్వహించండి.",
        route_dispatch: "రవాణా పంపు",
        no_listings: "పంట జాబితాలు ఏవీ దొరకలేదు.",
        kg_left: "కేజీ మిగిలి ఉంది", min_order: "కనిష్ట ఆర్డర్",
        market_benchmark: "మార్కెట్ ధర:",
        farmer_gain: "రైతుకు +45% అధిక ఆదాయం",
        consumer_save: "రిటైల్ కంటే 25% ఆదా",
        chat_seller: "రైతుతో చాట్ చేయండి", order_now: "ఆర్డర్ చేయండి",
        orders_title: "ఆర్డర్లు & అభ్యర్థనలు",
        orders_desc: "పొలం నుండి నేరుగా డెలివరీ స్థితిని ట్రాక్ చేయండి.",
        refresh: "రిఫ్రెష్", plan_route_from_orders: "డెలివరీ రూట్ ప్లాన్ చేయండి",
        crop_name: "పంట పేరు", seller: "విక్రేత", quantity_kg: "పరిమాణం (కేజీ)",
        total_price: "మొత్తం ధర", status: "స్థితి", actions: "చర్యలు",
        status_pending: "పెండింగ్", status_accepted: "అంగీకరించబడింది",
        status_rejected: "తిరస్కరించబడింది", status_dispatched: "రవాణాలో ఉంది",
        status_delivered: "చేరింది (Delivered)", status_cancelled: "రద్దు చేయబడింది",
        accept: "అంగీకరించు", decline: "తిరస్కరించు", chat: "చాట్", cancel_order: "రద్దు చేయి",
        new_listing_title: "కొత్త పంటను చేర్చండి", edit_listing_title: "పంట జాబితా సవరణ",
        save: "భద్రపరచు", cancel: "రద్దు చేయి",
        request_order_title: "తాజా పంటను ఆర్డర్ చేయండి",
        request_qty: "కొనుగోలు పరిమాణం (కేజీ)", delivery_address: "డెలివరీ చిరునామా",
        order_notes: "డెలివరీ సూచనలు", submit_order_btn: "ఆర్డర్ నిర్ధారించండి",
        available_stock: "అందుబాటులో ఉన్న నిల్వ",
        ai_forecast_config: "డిమాండ్ అంచనా", forecast_horizon: "అంచనా కాలం",
        run_forecast_btn: "AI అంచనా వేయండి", ai_forecast_prompt: "పంటను ఎంచుకుని అంచనా వేయండి.",
        logistics_title: "స్మార్ట్ లాజిస్టిక్స్ & రూట్ ఆప్టిమైజర్",
        logistics_desc: "2-Opt రూటింగ్ ద్వారా రవాణా దూరం మరియు ఖర్చు ఆదా అవుతాయి.",
        auto_import_orders: "ఆర్డర్లను నేరుగా తీసుకోండి",
        optimize_route_btn: "రూట్ ఆప్టిమైజ్ చేయండి",
        route_prompt: "రూట్ కోసం డెలివరీ స్థలాలను చేర్చండి.",
        active_trips_title: "ప్రస్తుత రవాణా ట్రిప్పులు",
        fair_price_title: "సరసమైన ధర & దళారుల తొలగింపు",
        fair_price_desc: "రైతులు మరియు వినియోగదారులకు పొందే లాభాన్ని చూడండి.",
        type_message: "సందేశం రాయండి...", send: "పంపు",
        select_buyer: "కొనుగోలుదారుల సందేశాలు:", loading: "లోడ్ అవుతోంది...",
        you: "మీరు"
      },
      ta: {
        app_name: "கிராப்கனெக்ட்",
        hero_title: "விவசாயிகள் மற்றும் வாங்குபவர்களுக்கான நேரடி சந்தை",
        hero_subtitle: "விவசாயிகளுக்கு அதிக லாபம் (+45%), நுகர்வோருக்கு குறைந்த விலை (-25%), இடைத்தரகர் இல்லாத AI விநியோகம்.",
        tagline_badge: "நேரடி டிஜிட்டல் சந்தை + ஸ்மார்ட் AI விநியோகம்",
        sms_hint: "விவசாயிகள் SMS அனுப்பவும்:",
        login: "உள்நுழைவு", register: "பதிவு", logout: "வெளியேறு",
        nav_marketplace: "சந்தை (Marketplace)", nav_orders: "ஆர்டர்கள்",
        nav_ai: "AI தேவை கணிப்பு", nav_logistics: "ஸ்மார்ட் விநியோக பாதை",
        nav_value: "நியாய விலை & சேமிப்பு",
        search_placeholder: "பயிர்களைத் தேடுங்கள்...",
        zip_placeholder: "அஞ்சல் குறியீடு...",
        filter_all_sellers: "அனைத்து விற்பனையாளர்கள்",
        filter_farmers_only: "விவசாயிகள் மட்டும்",
        filter_fpos_only: "FPO குழுக்கள் மட்டும்",
        filter_btn: "தேடு", add_listing: "+ பயிர் சேர்",
        seller_portal: "விற்பனையாளர் தளம்",
        seller_portal_desc: "உங்கள் பயிர் பட்டியல்கள் மற்றும் விநியோகங்களை நிர்வகியுங்கள்.",
        route_dispatch: "விநியோகத்தை அனுப்பு",
        no_listings: "பயிர் பட்டியல்கள் எதுவும் இல்லை.",
        kg_left: "கிலோ உள்ளது", min_order: "குறைந்தபட்ச ஆர்டர்",
        market_benchmark: "சில்லறை விலை:",
        farmer_gain: "விவசாயிக்கு +45% கூடுதல் லாபம்",
        consumer_save: "25% வரை சேமிப்பு",
        chat_seller: "விற்பனையாளருடன் பேசு", order_now: "ஆர்டர் செய்",
        orders_title: "ஆர்டர்கள் & கோரிக்கைகள்",
        orders_desc: "பண்ணையிலிருந்து நேரடி விநியோக நிலை.",
        refresh: "புதுப்பி", plan_route_from_orders: "பாதை திட்டமிடு",
        crop_name: "பயிர் பெயர்", seller: "விற்பவர்", quantity_kg: "அளவு (கிலோ)",
        total_price: "மொத்த விலை", status: "நிலை", actions: "செயல்கள்",
        status_pending: "நிலுவையில்", status_accepted: "ஏற்றுக்கொள்ளப்பட்டது",
        status_rejected: "நிராகரிக்கப்பட்டது", status_dispatched: "அனுப்பப்பட்டது",
        status_delivered: "வழங்கப்பட்டது", status_cancelled: "ரத்து செய்யப்பட்டது",
        accept: "ஏற்றுக்கொள்", decline: "நிராகரி", chat: "உரையாடு", cancel_order: "ரத்து செய்",
        new_listing_title: "புதிய பயிர் சேர்", edit_listing_title: "பயிரைத் திருத்து",
        save: "சேமி", cancel: "ரத்து",
        request_order_title: "பயிரை ஆர்டர் செய்",
        request_qty: "வாங்க வேண்டிய அளவு (கிலோ)", delivery_address: "விநியோக முகவரி",
        order_notes: "விநியோக வழிமுறைகள்", submit_order_btn: "ஆர்டரை உறுதிசெய்",
        available_stock: "இருப்பு அளவு",
        ai_forecast_config: "தேவை கணிப்பு", forecast_horizon: "கணிப்பு காலம்",
        run_forecast_btn: "AI கணிப்பை இயக்கு", ai_forecast_prompt: "தேவையை கணிக்க பயிரைத் தேர்ந்தெடுக்கவும்.",
        logistics_title: "ஸ்மார்ட் விநியோக பாதை அமைப்பு",
        logistics_desc: "2-Opt மூலம் விநியோக தூரம் மற்றும் செலவு குறைகிறது.",
        auto_import_orders: "ஆர்டர்களை தானாக சேர்",
        optimize_route_btn: "பாதையை மேம்படுத்து",
        route_prompt: "விநியோக வழியை உருவாக்க இடங்களைச் சேர்க்கவும்.",
        active_trips_title: "செயலில் உள்ள விநியோகங்கள்",
        fair_price_title: "நியாய விலை & இடைத்தரகர் நீக்கம்",
        fair_price_desc: "நேரடி சந்தையால் கிடைக்கும் கூடுதல் நன்மைகளைக் காண்க.",
        type_message: "செய்தியை உள்ளிடவும்...", send: "அனுப்பு",
        select_buyer: "வாங்குபவர் உரையாடல்கள்:", loading: "ஏற்றுகிறது...",
        you: "நீங்கள்"
      }
    };

    let currentLang = localStorage.getItem("cc_lang") || "en";
    let currentUser = JSON.parse(localStorage.getItem("cc_user") || "null");
    let currentActiveTab = "marketplace";

    // Chat state
    let activeChatListing = null;
    let activeChatPartnerPhone = null;
    let activeChatPartnerName = null;
    let chatPollTimer = null;
    let syncPollTimer = null;

    // Cache
    window._lastListings = [];
    window._lastOrders = [];

    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem("cc_lang", lang);
      document.documentElement.lang = lang;
      applyTranslations();
    }

    function t(key) {
      return (I18N[currentLang] && I18N[currentLang][key]) || (I18N.en && I18N.en[key]) || key;
    }

    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
        ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }

    function applyTranslations() {
      const labels = { en: "English", hi: "हिन्दी", te: "తెలుగు", ta: "தமிழ்" };
      document.getElementById("langLabel").textContent = labels[currentLang] || "English";

      document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const attr = el.getAttribute("data-i18n-attr");
        const value = t(key);
        if (attr) el.setAttribute(attr, value);
        else el.textContent = value;
      });

      renderBuyerListings(window._lastListings || []);
      if (window._lastOrders && window._lastOrders.length) {
        renderOrdersTable(window._lastOrders);
      }
    }

    function switchTab(tabId) {
      currentActiveTab = tabId;
      document.querySelectorAll(".tab-pane-view").forEach(el => el.classList.add("d-none"));
      document.querySelectorAll("#mainAppTabs .nav-link").forEach(el => el.classList.remove("active"));

      const viewEl = document.getElementById(`view-${tabId}`);
      const tabEl = document.getElementById(`tab-${tabId}`);
      if (viewEl) viewEl.classList.remove("d-none");
      if (tabEl) tabEl.classList.add("active");

      if (tabId === "marketplace") fetchListings();
      if (tabId === "orders") fetchOrdersData();
      if (tabId === "ai") runAIDemandForecast();
      if (tabId === "logistics") fetchTripsData();
      if (tabId === "analytics") fetchValueDistribution(document.getElementById("valueCropSelect").value);
    }

    function updateNavUserState() {
      const authBtns = document.getElementById("navAuthBtns");
      const userArea = document.getElementById("navUserArea");
      const sellerBox = document.getElementById("sellerDashboardBox");
      const addBtn = document.getElementById("farmerAddListingBtn");
      const autoDispatchBtn = document.getElementById("orderAutoDispatchBtn");

      if (!currentUser) {
        authBtns.classList.remove("d-none");
        authBtns.classList.add("d-flex");
        userArea.classList.add("d-none");
        userArea.classList.remove("d-flex");
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
        return;
      }

      authBtns.classList.add("d-none");
      authBtns.classList.remove("d-flex");
      userArea.classList.remove("d-none");
      userArea.classList.add("d-flex");

      document.getElementById("navUserName").textContent = currentUser.name;
      const badgeEl = document.getElementById("navUserBadge");
      
      const role = (currentUser.role || "").toUpperCase();
      if (role === "FARMER") {
        badgeEl.textContent = "🧑‍🌾 Farmer";
        badgeEl.className = "badge badge-farmer px-2 py-1";
        sellerBox.classList.remove("d-none");
        addBtn.classList.remove("d-none");
        autoDispatchBtn.classList.remove("d-none");
      } else if (role === "FPO") {
        badgeEl.textContent = "🚜 FPO Collective";
        badgeEl.className = "badge badge-fpo px-2 py-1";
        sellerBox.classList.remove("d-none");
        addBtn.classList.remove("d-none");
        autoDispatchBtn.classList.remove("d-none");
      } else if (role === "BULK_BUYER") {
        badgeEl.textContent = "🏢 Bulk Buyer";
        badgeEl.className = "badge badge-bulk px-2 py-1";
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
      } else {
        badgeEl.textContent = "🛒 Consumer";
        badgeEl.className = "badge badge-consumer px-2 py-1";
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
      }
    }

    function logout() {
      currentUser = null;
      localStorage.removeItem("cc_user");
      stopChatPolling();
      stopSyncPolling();
      updateNavUserState();
      fetchListings();
      alert("Logged out successfully.");
    }

    function setAuthTab(tab) {
      new bootstrap.Tab(document.querySelector(`#${tab}-tab`)).show();
    }

    // ============ Background Sync Polling ============
    function startSyncPolling() {
      stopSyncPolling();
      syncPollTimer = setInterval(() => {
        if (!currentUser) return;
        if (currentActiveTab === "marketplace") fetchListings(true);
        if (currentActiveTab === "orders") fetchOrdersData(true);
      }, 4000);
    }

    function stopSyncPolling() {
      if (syncPollTimer) {
        clearInterval(syncPollTimer);
        syncPollTimer = null;
      }
    }

    // ============ TAB 1: Marketplace API & Rendering ============
    async function fetchListings(isSilent = false) {
      const searchEl = document.getElementById("searchInput");
      const zipEl = document.getElementById("zipInput");
      const sellerTypeEl = document.getElementById("sellerTypeFilter");

      const crop = searchEl ? searchEl.value.trim() : "";
      const zip = zipEl ? zipEl.value.trim() : "";
      const sellerType = sellerTypeEl ? sellerTypeEl.value.trim() : "";

      try {
        const res = await fetch(`/api/listings?crop=${encodeURIComponent(crop)}&zip_code=${encodeURIComponent(zip)}&seller_type=${encodeURIComponent(sellerType)}`);
        if (!res.ok) return;
        const data = await res.json();
        window._lastListings = data;
        renderBuyerListings(data);
      } catch (err) {
        if (!isSilent) console.error("fetchListings error:", err);
      }
    }

    function renderBuyerListings(data) {
      const container = document.getElementById("listingsContainer");
      const noEl = document.getElementById("noListings");
      if (!container) return;
      container.innerHTML = "";

      if (!data || data.length === 0) {
        if (noEl) noEl.classList.remove("d-none");
        return;
      }
      if (noEl) noEl.classList.add("d-none");

      data.forEach(item => {
        const isFPO = (item.seller_type === "FPO");
        const sellerBadgeClass = isFPO ? "badge-fpo" : "badge-farmer";
        const sellerTypeTitle = isFPO ? "🚜 FPO Collective" : "🧑‍🌾 Direct Farmer";
        const sourceLabel = item.source === "SMS" ? "SMS Listed" : "Web Verified";

        const savingsAmount = Math.max(0, (item.retail_market_price_per_kg || (item.price_per_kg * 1.45)) - item.price_per_kg);
        const savingsPercent = Math.round((savingsAmount / (item.retail_market_price_per_kg || (item.price_per_kg * 1.45))) * 100);

        container.innerHTML += `
          <div class="col-md-6 col-lg-4">
            <div class="card card-listing h-100 shadow-sm bg-white p-3">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <span class="badge ${sellerBadgeClass} mb-1">${sellerTypeTitle}</span>
                  <h5 class="fw-bold text-success mb-0">${esc(item.crop_name)}</h5>
                </div>
                <div class="text-end">
                  <span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">
                    ${item.quantity_kg} ${t("kg_left")}
                  </span>
                  <small class="text-muted d-block" style="font-size:0.72rem;">${sourceLabel}</small>
                </div>
              </div>

              <div class="p-2 bg-light rounded-3 mb-3">
                <div class="d-flex justify-content-between align-items-baseline">
                  <div>
                    <span class="price-tag">₹${item.price_per_kg}</span>
                    <span class="text-muted small">/KG</span>
                  </div>
                  <div class="text-end">
                    <span class="badge bg-warning text-dark border"><i class="bi bi-tag-fill me-1"></i>Save ~${savingsPercent}%</span>
                  </div>
                </div>
                <div class="d-flex justify-content-between text-muted" style="font-size:0.75rem; margin-top:2px;">
                  <span>${t("market_benchmark")} <del>₹${item.retail_market_price_per_kg || Math.round(item.price_per_kg * 1.45)}</del></span>
                  <span class="text-success fw-bold">₹${savingsAmount.toFixed(1)}/kg cheaper</span>
                </div>
              </div>

              <div class="mb-3 small">
                <div class="text-secondary mb-1">
                  <i class="bi bi-person-circle text-primary me-1"></i> ${t("seller")}: <strong>${esc(item.farmer_name)}</strong>
                </div>
                <div class="text-secondary mb-1">
                  <i class="bi bi-geo-alt-fill text-danger me-1"></i> ${esc(item.location_name || item.zip_code)} (Pin: ${esc(item.zip_code)})
                </div>
                <div class="text-secondary">
                  <i class="bi bi-patch-check-fill text-success me-1"></i> ${esc(item.quality_grade || "Grade A")} &nbsp;|&nbsp;
                  <i class="bi bi-box me-1"></i> Min: <strong>${item.min_order_kg || 1} KG</strong>
                </div>
              </div>

              <div class="mt-auto d-grid gap-2">
                <button class="btn btn-outline-success btn-sm fw-semibold" onclick="openChatForListing(${item.id}, '${esc(item.crop_name)}', '${esc(item.farmer_phone)}', '${esc(item.farmer_name)}')">
                  <i class="bi bi-chat-dots-fill me-1"></i> ${t("chat_seller")}
                </button>
                <button class="btn btn-success btn-sm fw-semibold" onclick='openOrderModal(${JSON.stringify(item)})'>
                  <i class="bi bi-cart-check-fill me-1"></i> ${t("order_now")}
                </button>
              </div>
            </div>
          </div>`;
      });
    }

    // ============ Order Request Modal Handlers ============
    function openOrderModal(item) {
      if (!currentUser) {
        alert("Please log in or register first to place an order.");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }

      document.getElementById("orderListingId").value = item.id;
      document.getElementById("orderPricePerKg").value = item.price_per_kg;
      document.getElementById("orderBulkPricePerKg").value = item.bulk_price_per_kg || item.price_per_kg;
      document.getElementById("orderCropName").textContent = item.crop_name;
      document.getElementById("orderPriceBadge").textContent = `₹${item.price_per_kg}/kg`;
      document.getElementById("orderFarmerName").textContent = item.farmer_name;
      document.getElementById("orderFarmerPhone").textContent = item.farmer_phone;
      document.getElementById("orderAvailableQty").textContent = item.quantity_kg;
      document.getElementById("orderMinQty").textContent = item.min_order_kg || 1;

      const qtyInput = document.getElementById("orderQuantityInput");
      qtyInput.min = item.min_order_kg || 1;
      qtyInput.max = item.quantity_kg;
      qtyInput.value = item.min_order_kg || 5;

      document.getElementById("orderDeliveryAddress").value = currentUser.name ? `${currentUser.name} Address, Pin: ${currentUser.zip_code}` : "Direct Customer Delivery Address";
      document.getElementById("orderNotesInput").value = "";

      updateOrderTotal();
      new bootstrap.Modal(document.getElementById("orderModal")).show();
    }

    function updateOrderTotal() {
      const qty = parseFloat(document.getElementById("orderQuantityInput").value) || 0;
      const basePrice = parseFloat(document.getElementById("orderPricePerKg").value) || 0;
      const bulkPrice = parseFloat(document.getElementById("orderBulkPricePerKg").value) || basePrice;

      const effectivePrice = (qty >= 50 && bulkPrice) ? bulkPrice : basePrice;
      const total = Math.round(qty * effectivePrice);
      document.getElementById("orderTotalPriceEst").textContent = `₹${total}`;

      const retailBench = effectivePrice * 1.45;
      const totalSaved = Math.round(qty * (retailBench - effectivePrice));
      document.getElementById("orderSavingsBadge").textContent = `You save ~₹${totalSaved} vs Retail!`;
    }

    async function handleSubmitOrder(e) {
      e.preventDefault();
      if (!currentUser) return;

      const listing_id = parseInt(document.getElementById("orderListingId").value, 10);
      const quantity_kg = parseFloat(document.getElementById("orderQuantityInput").value);
      const delivery_address = document.getElementById("orderDeliveryAddress").value;
      const delivery_lat = parseFloat(document.getElementById("orderDeliveryLat").value) || 17.4156;
      const delivery_lon = parseFloat(document.getElementById("orderDeliveryLon").value) || 78.4350;
      const notes = document.getElementById("orderNotesInput").value;

      try {
        const res = await fetch("/api/order", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            listing_id,
            buyer_phone: currentUser.phone,
            quantity_kg,
            delivery_address,
            delivery_lat,
            delivery_lon,
            notes
          })
        });

        const data = await res.json();
        if (res.ok) {
          bootstrap.Modal.getInstance(document.getElementById("orderModal")).hide();
          alert(data.message || "Order placed successfully!");
          fetchListings();
          switchTab("orders");
        } else {
          alert(data.detail || "Error placing order");
        }
      } catch (err) {
        console.error("Order submit error:", err);
      }
    }

    // ============ TAB 2: Orders API & Table Rendering ============
    async function fetchOrdersData(isSilent = false) {
      if (!currentUser) {
        document.getElementById("ordersTableContainer").innerHTML = `
          <div class="text-center py-5 text-muted">
            <i class="bi bi-shield-lock fs-1 d-block mb-2 text-warning"></i>
            <p>Please log in to view and manage your orders and batch requests.</p>
            <button class="btn btn-success btn-sm fw-semibold" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')">Log In Now</button>
          </div>`;
        return;
      }

      const isSellerRole = (currentUser.role === "FARMER" || currentUser.role === "FPO");
      const url = isSellerRole 
        ? `/api/farmer/orders?farmer_phone=${encodeURIComponent(currentUser.phone)}`
        : `/api/buyer/orders?buyer_phone=${encodeURIComponent(currentUser.phone)}`;

      try {
        const res = await fetch(url);
        if (!res.ok) return;
        const orders = await res.json();
        window._lastOrders = orders;
        renderOrdersTable(orders);
      } catch (err) {
        if (!isSilent) console.error("fetchOrdersData error:", err);
      }
    }

    function renderOrdersTable(orders) {
      const container = document.getElementById("ordersTableContainer");
      const badge = document.getElementById("tabOrdersBadge");
      const isSellerRole = currentUser && (currentUser.role === "FARMER" || currentUser.role === "FPO");

      const pendingCount = (orders || []).filter(o => o.status === "PENDING").length;
      if (pendingCount > 0) {
        badge.textContent = pendingCount;
        badge.classList.remove("d-none");
      } else {
        badge.classList.add("d-none");
      }

      if (!orders || orders.length === 0) {
        container.innerHTML = `
          <div class="text-center py-5 text-muted">
            <i class="bi bi-inbox fs-1 d-block mb-2 text-secondary"></i>
            <p>No orders recorded yet.</p>
          </div>`;
        return;
      }

      container.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col"># Order</th>
                <th scope="col">${t("crop_name")}</th>
                <th scope="col">${isSellerRole ? "Buyer / Destination" : "Farmer / FPO"}</th>
                <th scope="col">${t("quantity_kg")}</th>
                <th scope="col">${t("total_price")}</th>
                <th scope="col">${t("status")}</th>
                <th scope="col" class="text-end">${t("actions")}</th>
              </tr>
            </thead>
            <tbody>
              ${orders.map(o => {
                let statusBadge = "";
                if (o.status === "PENDING") statusBadge = `<span class="badge bg-warning text-dark border"><i class="bi bi-hourglass-split me-1"></i>Pending</span>`;
                else if (o.status === "ACCEPTED") statusBadge = `<span class="badge bg-primary"><i class="bi bi-check-circle-fill me-1"></i>Accepted</span>`;
                else if (o.status === "DISPATCHED") statusBadge = `<span class="badge bg-info text-dark"><i class="bi bi-truck me-1"></i>Dispatched</span>`;
                else if (o.status === "DELIVERED") statusBadge = `<span class="badge bg-success"><i class="bi bi-patch-check-fill me-1"></i>Delivered</span>`;
                else if (o.status === "REJECTED") statusBadge = `<span class="badge bg-danger">Declined</span>`;
                else statusBadge = `<span class="badge bg-secondary">Cancelled</span>`;

                const buyerOrSellerInfo = isSellerRole ? `
                  <div>
                    <strong>${esc(o.buyer_name)}</strong>
                    <small class="badge bg-light text-dark border ms-1">${esc(o.buyer_role || "Consumer")}</small>
                    <div class="text-muted" style="font-size:0.75rem;">${esc(o.delivery_address || o.delivery_zip)}</div>
                  </div>` : `
                  <div>
                    <strong>${esc(o.farmer_name)}</strong>
                    <div class="text-muted" style="font-size:0.75rem;">${esc(o.farmer_phone)}</div>
                  </div>`;

                let actions = "";
                if (isSellerRole) {
                  if (o.status === "PENDING") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-success fw-semibold" onclick="handleAcceptOrder(${o.id})">
                          <i class="bi bi-check-lg me-1"></i> Accept
                        </button>
                        <button class="btn btn-outline-danger" onclick="handleRejectOrder(${o.id})">
                          <i class="bi bi-x-lg"></i>
                        </button>
                        <button class="btn btn-outline-primary" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')">
                          <i class="bi bi-chat-dots-fill"></i>
                        </button>
                      </div>`;
                  } else if (o.status === "ACCEPTED") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="loadSingleOrderToRoute(${JSON.stringify(o).replace(/"/g, '&quot;')})">
                          <i class="bi bi-truck me-1"></i> Route
                        </button>
                        <button class="btn btn-outline-success" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')">
                          <i class="bi bi-chat-dots-fill"></i>
                        </button>
                      </div>`;
                  } else {
                    actions = `
                      <button class="btn btn-sm btn-outline-secondary" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')">
                        <i class="bi bi-chat-dots-fill me-1"></i> Chat
                      </button>`;
                  }
                } else {
                  if (o.status === "PENDING") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-danger" onclick="handleCancelOrder(${o.id})">
                          Cancel
                        </button>
                        <button class="btn btn-outline-success" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.farmer_phone)}', '${esc(o.farmer_name)}')">
                          <i class="bi bi-chat-dots-fill"></i> Chat
                        </button>
                      </div>`;
                  } else {
                    actions = `
                      <button class="btn btn-sm btn-outline-success" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.farmer_phone)}', '${esc(o.farmer_name)}')">
                        <i class="bi bi-chat-dots-fill me-1"></i> Chat
                      </button>`;
                  }
                }

                return `
                  <tr>
                    <td><strong class="text-secondary">#${o.id}</strong></td>
                    <td><strong class="text-success">${esc(o.crop_name)}</strong></td>
                    <td>${buyerOrSellerInfo}</td>
                    <td><strong>${o.quantity_kg} KG</strong></td>
                    <td><strong>₹${o.total_price}</strong> <small class="text-muted">(@ ₹${o.price_per_kg}/kg)</small></td>
                    <td>${statusBadge}</td>
                    <td class="text-end">${actions}</td>
                  </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>`;
    }

    async function handleAcceptOrder(orderId) {
      if (!confirm("Accept this batch request? Inventory will be allocated and scheduled for logistics dispatch.")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/accept?farmer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || "Order accepted!");
          fetchOrdersData();
          fetchListings();
        } else {
          alert(data.detail || "Error accepting order");
        }
      } catch (err) {
        console.error("Accept error:", err);
      }
    }

    async function handleRejectOrder(orderId) {
      if (!confirm("Decline this batch request?")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/reject?farmer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || "Order declined.");
          fetchOrdersData();
        } else {
          alert(data.detail || "Error declining order");
        }
      } catch (err) {
        console.error("Reject error:", err);
      }
    }

    async function handleCancelOrder(orderId) {
      if (!confirm("Cancel this order request?")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/cancel?buyer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || "Order cancelled.");
          fetchOrdersData();
          fetchListings();
        } else {
          alert(data.detail || "Error cancelling order");
        }
      } catch (err) {
        console.error("Cancel error:", err);
      }
    }

    // ============ TAB 3: AI Demand Forecasting ============
    function syncForecastCropInput(val) {
      document.getElementById("forecastCropInput").value = val;
    }

    async function runAIDemandForecast() {
      const crop = (document.getElementById("forecastCropInput").value || "TOMATO").trim();
      const days = document.getElementById("forecastDaysSelect").value || "7";
      const card = document.getElementById("forecastResultsCard");

      card.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2"></span>Analyzing multi-factor demand trends...</div>`;

      try {
        const res = await fetch(`/api/ai/demand-forecast?crop=${encodeURIComponent(crop)}&days=${encodeURIComponent(days)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Forecast calculation error");

        const trendBadge = data.trend === "rising" ? "bg-success" : (data.trend === "falling" ? "bg-danger" : "bg-primary");
        const trendIcon = data.trend === "rising" ? "bi-arrow-up-right" : (data.trend === "falling" ? "bi-arrow-down-right" : "bi-dash-lg");

        const maxVal = Math.max(...data.daily_projection.map(d => d.demand_kg), 10);
        const barsHtml = data.daily_projection.map((d, i) => {
          const heightPct = Math.round((d.demand_kg / maxVal) * 100);
          return `
            <div class="d-flex flex-column align-items-center flex-fill" style="min-width:42px;">
              <span class="small fw-bold text-success mb-1" style="font-size:0.72rem;">${d.demand_kg}kg</span>
              <div class="w-100 bg-success bg-opacity-75 rounded-top" style="height:${heightPct}px; min-height:8px;"></div>
              <span class="text-muted text-truncate mt-1" style="font-size:0.68rem;">${d.day.split(" ")[0]}</span>
            </div>`;
        }).join("");

        card.innerHTML = `
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <span class="badge ${trendBadge} px-2 py-1 mb-1"><i class="bi ${trendIcon} me-1"></i>Trend: ${esc(data.trend.toUpperCase())}</span>
              <h4 class="fw-bold text-success mb-0">${esc(data.crop)} AI Demand Forecast (${data.forecast_days} Days)</h4>
            </div>
            <div class="text-end">
              <span class="badge bg-light text-dark border px-2 py-1">Confidence: <strong>${data.confidence_percent}%</strong></span>
            </div>
          </div>

          <div class="row g-3 mb-4">
            <div class="col-md-3 col-6">
              <div class="metric-box text-center">
                <small class="text-muted d-block">Projected Demand</small>
                <h5 class="fw-bold text-dark mb-0">${data.forecast_total_kg} KG</h5>
                <small class="text-muted">~${data.forecast_daily_kg} kg/day</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-box text-center">
                <small class="text-muted d-block">Current Supply</small>
                <h5 class="fw-bold text-dark mb-0">${data.current_supply_kg} KG</h5>
                <small class="text-muted">Active in Portal</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-box text-center">
                <small class="text-muted d-block">Supply Gap</small>
                <h5 class="fw-bold ${data.supply_gap_kg > 0 ? 'text-danger' : 'text-success'} mb-0">
                  ${data.supply_gap_kg > 0 ? '+' + data.supply_gap_kg : data.supply_gap_kg} KG
                </h5>
                <small class="text-muted">${data.supply_gap_kg > 0 ? 'Deficit' : 'Surplus'}</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-box text-center">
                <small class="text-muted d-block">Target Stocking</small>
                <h5 class="fw-bold text-primary mb-0">${data.recommended_stock_kg} KG</h5>
                <small class="text-muted">+15% safety buffer</small>
              </div>
            </div>
          </div>

          <div class="p-3 bg-light rounded-3 mb-4 border">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6 class="fw-bold text-dark small mb-0"><i class="bi bi-graph-up text-success me-1"></i>Daily Projected Consumption (KG)</h6>
              <span class="badge bg-white text-muted border small">Shelf Life: ${data.shelf_life_days} Days</span>
            </div>
            <div class="d-flex align-items-end gap-2 pt-3 pb-1" style="height:140px; overflow-x:auto;">
              ${barsHtml}
            </div>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <div class="p-3 bg-success bg-opacity-10 border border-success border-opacity-25 rounded-3">
                <h6 class="fw-bold text-success mb-1"><i class="bi bi-cash-coin me-1"></i>Recommended Farmer Price</h6>
                <div class="fs-4 fw-bold text-success">₹${data.fair_farmer_price_inr} / KG</div>
                <small class="text-muted">Mandi Baseline: <del>₹${data.mandi_benchmark_inr}</del> (Farmer earns <strong>+45% more</strong>)</small>
              </div>
            </div>
            <div class="col-md-6">
              <div class="p-3 bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-3">
                <h6 class="fw-bold text-primary mb-1"><i class="bi bi-bag-check-fill me-1"></i>Target Direct Consumer Price</h6>
                <div class="fs-4 fw-bold text-primary">₹${data.fair_consumer_price_inr} / KG</div>
                <small class="text-muted">Retail Supermarket: <del>₹${data.retail_benchmark_inr}</del> (Consumer saves <strong>25%</strong>)</small>
              </div>
            </div>
          </div>

          <div class="alert alert-success d-flex align-items-center mb-0">
            <i class="bi bi-lightbulb-fill text-success fs-3 me-3"></i>
            <div>
              <strong class="d-block mb-1">AI Recommendation:</strong>
              <span class="small">${esc(data.recommendation)}</span>
            </div>
          </div>`;
      } catch (err) {
        card.innerHTML = `<div class="alert alert-danger mb-0">${esc(err.message)}</div>`;
      }
    }

    // ============ TAB 4: Smart Logistics & 2-Opt Optimizer ============
    let lastOptimizedData = null;

    function autoLoadOrdersToLogistics() {
      switchTab("logistics");
      const acceptedOrders = (window._lastOrders || []).filter(o => o.status === "ACCEPTED");
      if (acceptedOrders.length === 0) {
        alert("No ACCEPTED orders available yet. Accept pending orders first to load them into the delivery route.");
        return;
      }

      const stopsLines = acceptedOrders.map(o => {
        const name = o.buyer_name || `Buyer #${o.id}`;
        const lat = o.delivery_lat || 17.4156;
        const lon = o.delivery_lon || 78.4350;
        const kg = o.quantity_kg || 10;
        const addr = (o.delivery_address || `Order #${o.id}`).replace(/,/g, ' ');
        return `${name}, ${lat}, ${lon}, ${kg}, ${addr}`;
      });

      document.getElementById("routeStops").value = stopsLines.join("\n");
      runRouteOptimizer();
    }

    function loadSingleOrderToRoute(order) {
      switchTab("logistics");
      const name = order.buyer_name || `Buyer #${order.id}`;
      const lat = order.delivery_lat || 17.4156;
      const lon = order.delivery_lon || 78.4350;
      const kg = order.quantity_kg || 10;
      const addr = (order.delivery_address || `Order #${order.id}`).replace(/,/g, ' ');
      document.getElementById("routeStops").value = `${name}, ${lat}, ${lon}, ${kg}, ${addr}`;
      runRouteOptimizer();
    }

    function parseRouteStopsText() {
      const lines = document.getElementById("routeStops").value.split(/\r?\n/).map(x => x.trim()).filter(Boolean);
      const stops = [];
      for (const line of lines) {
        const parts = line.split(",").map(x => x.trim());
        if (parts.length < 4) throw new Error(`Invalid stop line: "${line}". Format: Name, Lat, Lon, KG, [Address]`);
        const lat = Number(parts[1]);
        const lon = Number(parts[2]);
        const kg = Number(parts[3]);
        const addr = parts.slice(4).join(", ") || "Delivery Destination";
        if (!Number.isFinite(lat) || !Number.isFinite(lon) || !Number.isFinite(kg) || kg < 0) {
          throw new Error(`Invalid numeric coordinates or weight in: "${line}"`);
        }
        stops.push({ name: parts[0], lat, lon, quantity_kg: kg, address: addr });
      }
      return stops;
    }

    async function runRouteOptimizer() {
      const resultBox = document.getElementById("routeResultsBox");
      try {
        const stops = parseRouteStopsText();
        const originName = document.getElementById("originName").value;
        const originLat = Number(document.getElementById("originLat").value);
        const originLon = Number(document.getElementById("originLon").value);
        const capacity = Number(document.getElementById("vehicleCapacity").value);

        resultBox.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2"></span>Running 2-Opt trajectory optimization...</div>`;

        const res = await fetch("/api/logistics/optimize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            origin_name: originName,
            origin_lat: originLat,
            origin_lon: originLon,
            stops,
            vehicle_capacity_kg: capacity
          })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Route optimization error");
        lastOptimizedData = data;

        const isSellerRole = currentUser && (currentUser.role === "FARMER" || currentUser.role === "FPO");

        resultBox.innerHTML = `
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <span class="badge bg-success px-2 py-1 mb-1"><i class="bi bi-lightning-charge-fill me-1"></i>2-Opt Optimized Sequence</span>
              <h5 class="fw-bold text-dark mb-0">Delivery Route Summary</h5>
            </div>
            ${isSellerRole ? `<button class="btn btn-success btn-sm fw-semibold" onclick="handleDispatchTripSubmit()"><i class="bi bi-send-check-fill me-1"></i> Create & Dispatch Trip</button>` : ''}
          </div>

          <div class="row g-2 mb-3">
            <div class="col-4">
              <div class="p-2 bg-white rounded border text-center">
                <small class="text-muted d-block">Total Route</small>
                <strong>${data.total_distance_km} km</strong>
                <small class="text-success d-block" style="font-size:0.7rem;">-${data.distance_saved_km} km saved</small>
              </div>
            </div>
            <div class="col-4">
              <div class="p-2 bg-white rounded border text-center">
                <small class="text-muted d-block">Est. Travel Time</small>
                <strong>${data.estimated_travel_minutes} mins</strong>
                <small class="text-muted d-block" style="font-size:0.7rem;">(${data.estimated_travel_hours} hrs)</small>
              </div>
            </div>
            <div class="col-4">
              <div class="p-2 bg-white rounded border text-center">
                <small class="text-muted d-block">Load Utilization</small>
                <strong>${data.load_utilization_percent}%</strong>
                <small class="text-muted d-block" style="font-size:0.7rem;">${data.total_load_kg}/${data.vehicle_capacity_kg} kg</small>
              </div>
            </div>
          </div>

          <div class="alert alert-success py-2 px-3 small mb-3">
            <div class="d-flex justify-content-between align-items-center">
              <div><i class="bi bi-truck me-1"></i><strong>Recommended Vehicle:</strong> ${esc(data.recommended_vehicle)}</div>
              <div><span class="badge bg-success-subtle text-success">Est. Fuel: ₹${data.estimated_fuel_cost_inr}</span></div>
            </div>
            <div class="text-muted mt-1" style="font-size:0.75rem;">
              🌱 <strong>Green Impact:</strong> Consolidated routing saves <strong>${data.co2_saved_kg} KG of CO2</strong> and ₹${data.cost_savings_inr} in direct transport expenses.
            </div>
          </div>

          <h6 class="fw-bold text-dark small mb-2"><i class="bi bi-signpost-split text-success me-1"></i>Optimized Delivery Sequence:</h6>
          <div class="d-flex flex-column gap-2" style="max-height: 250px; overflow-y:auto;">
            <div class="p-2 bg-white rounded border-start border-success border-4">
              <strong class="text-success">🚀 Origin: ${esc(data.origin.name)}</strong>
              <small class="text-muted d-block">Coordinates: [${data.origin.lat}, ${data.origin.lon}]</small>
            </div>
            ${data.route.map(stop => `
              <div class="route-stop-item p-2 shadow-sm border">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong>${stop.sequence}. ${esc(stop.name)}</strong>
                  <span class="badge bg-success-subtle text-success">${stop.quantity_kg} KG</span>
                </div>
                <div class="text-muted small" style="font-size:0.78rem;">
                  <i class="bi bi-geo-alt me-1"></i>${esc(stop.address)} &nbsp;|&nbsp;
                  <i class="bi bi-arrow-right-short text-primary"></i> ${stop.distance_from_previous_km} km from previous stop
                </div>
              </div>
            `).join("")}
          </div>`;
      } catch (err) {
        resultBox.innerHTML = `<div class="alert alert-danger mb-0">${esc(err.message)}</div>`;
      }
    }

    async function handleDispatchTripSubmit() {
      if (!currentUser || !lastOptimizedData) return;
      if (!confirm("Dispatch this logistics trip? Connected customer orders will be marked DISPATCHED.")) return;

      const acceptedOrderIds = (window._lastOrders || []).filter(o => o.status === "ACCEPTED").map(o => o.id);

      try {
        const res = await fetch("/api/logistics/dispatch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            farmer_phone: currentUser.phone,
            origin_name: lastOptimizedData.origin.name,
            origin_lat: lastOptimizedData.origin.lat,
            origin_lon: lastOptimizedData.origin.lon,
            vehicle_type: lastOptimizedData.recommended_vehicle,
            vehicle_number: "TS-09-UB-8821",
            driver_name: "Raju Logistics Driver",
            driver_phone: "+919876540000",
            stops: lastOptimizedData.route,
            order_ids: acceptedOrderIds,
            total_distance_km: lastOptimizedData.total_distance_km,
            total_load_kg: lastOptimizedData.total_load_kg,
            estimated_travel_minutes: lastOptimizedData.estimated_travel_minutes,
            fuel_cost_est: lastOptimizedData.estimated_fuel_cost_inr,
            co2_saved_kg: lastOptimizedData.co2_saved_kg
          })
        });

        const data = await res.json();
        if (res.ok) {
          alert(data.message || "Trip dispatched successfully!");
          fetchTripsData();
          fetchOrdersData();
        } else {
          alert(data.detail || "Dispatch failed");
        }
      } catch (err) {
        console.error("Dispatch error:", err);
      }
    }

    async function fetchTripsData() {
      const container = document.getElementById("tripsListContainer");
      if (!currentUser) {
        container.innerHTML = `<p class="text-muted small">Log in to view active delivery trips.</p>`;
        return;
      }

      try {
        const res = await fetch(`/api/logistics/trips?phone=${encodeURIComponent(currentUser.phone)}`);
        if (!res.ok) return;
        const trips = await res.json();

        if (!trips || trips.length === 0) {
          container.innerHTML = `<p class="text-muted small py-2 mb-0">No active trips dispatched yet.</p>`;
          return;
        }

        const isSellerRole = (currentUser.role === "FARMER" || currentUser.role === "FPO");

        container.innerHTML = `
          <div class="row g-3">
            ${trips.map(tr => `
              <div class="col-md-6">
                <div class="p-3 bg-white rounded-3 border shadow-sm h-100">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-bold text-success">Trip #${tr.id}</span>
                    <span class="badge ${tr.status === 'DELIVERED' ? 'bg-success' : 'bg-primary'}">${tr.status}</span>
                  </div>
                  <div class="small text-secondary mb-2">
                    <div><i class="bi bi-truck me-1"></i> ${esc(tr.vehicle_type)} (${esc(tr.vehicle_number)})</div>
                    <div><i class="bi bi-person-badge me-1"></i> Driver: ${esc(tr.driver_name)} (${esc(tr.driver_phone)})</div>
                    <div><i class="bi bi-speedometer2 me-1"></i> ${tr.total_distance_km} km &nbsp;|&nbsp; ${tr.total_load_kg} KG load</div>
                  </div>
                  ${isSellerRole && tr.status !== 'DELIVERED' ? `
                    <button class="btn btn-outline-success btn-sm w-100 fw-semibold" onclick="handleMarkTripDelivered(${tr.id})">
                      <i class="bi bi-check-circle-fill me-1"></i> Mark Trip & Orders Delivered
                    </button>
                  ` : ''}
                </div>
              </div>
            `).join("")}
          </div>`;
      } catch (err) {
        console.error("fetchTrips error:", err);
      }
    }

    async function handleMarkTripDelivered(tripId) {
      if (!confirm("Confirm all stops have been delivered? Connected customer orders will be marked DELIVERED.")) return;
      try {
        const res = await fetch(`/api/logistics/trips/${tripId}/deliver?phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || "Trip marked delivered!");
          fetchTripsData();
          fetchOrdersData();
        } else {
          alert(data.detail || "Error updating trip");
        }
      } catch (err) {
        console.error("Mark trip error:", err);
      }
    }

    // ============ TAB 5: Fair Price & Value Chain Transparency ============
    async function fetchValueDistribution(crop) {
      const container = document.getElementById("valueDistributionContent");
      container.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2"></span>Loading value distribution breakdown...</div>`;

      try {
        const res = await fetch(`/api/analytics/value-distribution?crop=${encodeURIComponent(crop)}`);
        const data = await res.json();
        if (!res.ok) throw new Error("Could not load value distribution");

        container.innerHTML = `
          <div class="row g-4 mb-4">
            <div class="col-lg-6">
              <div class="p-4 bg-danger bg-opacity-10 rounded-4 border border-danger border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-danger mb-0"><i class="bi bi-x-circle-fill me-2"></i>Traditional Multi-Tier Mandi Chain</h5>
                  <span class="badge bg-danger">High Inefficiency</span>
                </div>
                <p class="text-muted small">Passes through 3-4 intermediaries before reaching consumers, resulting in massive margins lost to middlemen and 25% post-harvest food waste.</p>

                <div class="d-flex flex-column gap-2 mb-3">
                  <div class="p-2 bg-white rounded border d-flex justify-content-between">
                    <span>🌾 Farmer Realization</span>
                    <strong class="text-danger">₹${data.traditional_chain.farmer_earns_inr}/KG (42%)</strong>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between text-muted small">
                    <span>1. Village Aggregator Margin</span>
                    <span>₹${data.traditional_chain.village_middleman_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between text-muted small">
                    <span>2. Mandi Arhatiya Commission</span>
                    <span>₹${data.traditional_chain.mandi_commission_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between text-muted small">
                    <span>3. Wholesaler + Retailer Markup</span>
                    <span>₹${(data.traditional_chain.wholesaler_margin_inr + data.traditional_chain.retailer_margin_inr).toFixed(1)}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between">
                    <span>🛒 Consumer Pays</span>
                    <strong class="text-dark">₹${data.traditional_chain.consumer_pays_inr}/KG</strong>
                  </div>
                </div>

                <div class="badge bg-danger bg-opacity-25 text-danger border border-danger p-2 w-100 text-start">
                  ⚠️ <strong>Supply Chain Loss:</strong> ~25% perishable spoilage due to delayed multi-hop handling.
                </div>
              </div>
            </div>

            <div class="col-lg-6">
              <div class="p-4 bg-success bg-opacity-10 rounded-4 border border-success border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-success mb-0"><i class="bi bi-check-circle-fill me-2"></i>CropConnect Direct Model</h5>
                  <span class="badge bg-success">Direct Linkage</span>
                </div>
                <p class="text-muted small">Connects farmers/FPOs directly with buyers via automated matchmaking and consolidated 2-Opt logistics.</p>

                <div class="d-flex flex-column gap-2 mb-3">
                  <div class="p-2 bg-white rounded border d-flex justify-content-between">
                    <span>🌾 Farmer Realization</span>
                    <strong class="text-success">₹${data.cropconnect_direct_chain.farmer_earns_inr}/KG (+${data.benefits.farmer_income_increase_percent}%)</strong>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between text-muted small">
                    <span>🚚 Direct Smart Logistics</span>
                    <span>₹${data.cropconnect_direct_chain.direct_logistics_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between text-muted small">
                    <span>❌ Intermediary Middleman Cut</span>
                    <span class="text-success fw-bold">₹0.0 (Eliminated)</span>
                  </div>
                  <div class="p-2 bg-white rounded border d-flex justify-content-between">
                    <span>🛒 Consumer Pays</span>
                    <strong class="text-success">₹${data.cropconnect_direct_chain.consumer_pays_inr}/KG (-${data.benefits.consumer_price_savings_percent}%)</strong>
                  </div>
                </div>

                <div class="badge bg-success bg-opacity-25 text-success border border-success p-2 w-100 text-start">
                  ✅ <strong>Direct Freshness:</strong> < 4.5% food loss through farm-to-table optimized routes.
                </div>
              </div>
            </div>
          </div>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="p-3 bg-light rounded-3 text-center border">
                <i class="bi bi-cash-stack fs-2 text-success mb-2 d-block"></i>
                <h4 class="fw-bold text-success mb-0">+${data.benefits.farmer_income_increase_percent}%</h4>
                <small class="text-muted">Direct Income Boost for Farmers</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 bg-light rounded-3 text-center border">
                <i class="bi bi-wallet2 fs-2 text-primary mb-2 d-block"></i>
                <h4 class="fw-bold text-primary mb-0">-${data.benefits.consumer_price_savings_percent}%</h4>
                <small class="text-muted">Price Discount for Consumers</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 bg-light rounded-3 text-center border">
                <i class="bi bi-shield-check fs-2 text-warning mb-2 d-block"></i>
                <h4 class="fw-bold text-warning mb-0">${data.benefits.supply_chain_waste_reduction_percent}%</h4>
                <small class="text-muted">Post-Harvest Waste Reduced</small>
              </div>
            </div>
          </div>`;
      } catch (err) {
        container.innerHTML = `<div class="alert alert-danger">${esc(err.message)}</div>`;
      }
    }

    // ============ Listing CRUD Modal Handlers ============
    function openCreateListingModal() {
      if (!currentUser || (currentUser.role !== "FARMER" && currentUser.role !== "FPO")) {
        alert("Please register or log in as a Farmer or FPO to add listings.");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }
      document.getElementById("listingId").value = "";
      document.getElementById("listingCrop").value = "";
      document.getElementById("listingQty").value = "";
      document.getElementById("listingPrice").value = "";
      document.getElementById("listingMinQty").value = "5";
      document.getElementById("listingBulkPrice").value = "";
      document.getElementById("listingZip").value = currentUser.zip_code || "500001";
      document.getElementById("listingShelfLife").value = "7";
      document.getElementById("listingGrade").value = "Grade A - Freshly Harvested";
      document.getElementById("listingModalTitle").textContent = t("new_listing_title");
      new bootstrap.Modal(document.getElementById("listingModal")).show();
    }

    async function handleSaveListing(e) {
      e.preventDefault();
      if (!currentUser) return;

      const id = document.getElementById("listingId").value;
      const crop_name = document.getElementById("listingCrop").value;
      const quantity_kg = parseFloat(document.getElementById("listingQty").value);
      const price_per_kg = parseFloat(document.getElementById("listingPrice").value);
      const min_order_kg = parseFloat(document.getElementById("listingMinQty").value) || 5;
      const bulk_price_per_kg = parseFloat(document.getElementById("listingBulkPrice").value) || null;
      const zip_code = document.getElementById("listingZip").value;
      const shelf_life_days = parseInt(document.getElementById("listingShelfLife").value, 10) || 7;
      const quality_grade = document.getElementById("listingGrade").value;

      try {
        let res;
        if (id) {
          res = await fetch(`/api/listings/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              farmer_phone: currentUser.phone,
              crop_name, quantity_kg, price_per_kg, min_order_kg,
              bulk_price_per_kg, zip_code, shelf_life_days, quality_grade
            })
          });
        } else {
          res = await fetch(`/api/listings`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              farmer_phone: currentUser.phone,
              crop_name, quantity_kg, price_per_kg, min_order_kg,
              bulk_price_per_kg, zip_code, shelf_life_days, quality_grade
            })
          });
        }

        const data = await res.json();
        if (res.ok) {
          bootstrap.Modal.getInstance(document.getElementById("listingModal")).hide();
          alert(data.message || "Listing saved successfully!");
          fetchListings();
        } else {
          alert(data.detail || "Error saving listing");
        }
      } catch (err) {
        console.error("Save listing error:", err);
      }
    }

    // ============ Robust Direct Chat Handlers ============
    function openChatForListing(listingId, cropName, partnerPhone, partnerName) {
      if (!currentUser) {
        alert("Please log in first to chat with the seller.");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }

      activeChatListing = { id: listingId, crop_name: cropName };
      activeChatPartnerPhone = partnerPhone;
      activeChatPartnerName = partnerName;

      document.getElementById("chatCropTitle").textContent = `${cropName} - Chat`;
      document.getElementById("chatPartnerTitle").textContent = `${partnerName} (${partnerPhone})`;
      document.getElementById("farmerBuyerBar").classList.add("d-none");
      document.getElementById("chatInputText").value = "";
      document.getElementById("chatInputText").disabled = false;
      document.getElementById("chatSendBtn").disabled = false;

      const modal = new bootstrap.Modal(document.getElementById("chatModal"));
      modal.show();

      fetchChatMessages();
      startChatPolling();
    }

    async function fetchChatMessages() {
      if (!activeChatListing || !currentUser || !activeChatPartnerPhone) return;
      try {
        const url = `/api/listings/${activeChatListing.id}/messages?phone=${encodeURIComponent(currentUser.phone)}&partner_phone=${encodeURIComponent(activeChatPartnerPhone)}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const messages = await res.json();
        renderChatMessages(messages);
      } catch (err) {
        console.error("fetchChatMessages error:", err);
      }
    }

    function renderChatMessages(messages) {
      const container = document.getElementById("chatMessagesList");
      if (!messages || messages.length === 0) {
        container.innerHTML = `<p class="text-muted small text-center my-auto">No messages yet. Start the direct conversation!</p>`;
        return;
      }

      container.innerHTML = messages.map(m => {
        const isSelf = (m.from_phone === currentUser.phone || m.from_phone.replace(/\D/g,'') === currentUser.phone.replace(/\D/g,''));
        const alignClass = isSelf ? "align-self-end" : "align-self-start";
        const bubbleClass = isSelf ? "chat-msg-self" : "chat-msg-other";
        const senderName = isSelf ? t("you") : (m.from_name || m.from_phone);
        const timeStr = m.ts ? new Date(m.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "";

        return `
          <div class="chat-bubble p-2 rounded shadow-sm ${bubbleClass} ${alignClass}">
            <div class="d-flex justify-content-between align-items-center gap-2 mb-1">
              <small class="fw-bold ${isSelf ? 'text-white-50' : 'text-success'}" style="font-size:0.72rem;">${esc(senderName)}</small>
              <small class="${isSelf ? 'text-white-50' : 'text-muted'}" style="font-size:0.68rem;">${timeStr}</small>
            </div>
            <div class="small">${esc(m.body)}</div>
          </div>`;
      }).join("");

      container.scrollTop = container.scrollHeight;
    }

    async function handleSendMessage(e) {
      e.preventDefault();
      const input = document.getElementById("chatInputText");
      const body = input.value.trim();
      if (!body || !activeChatListing || !currentUser || !activeChatPartnerPhone) return;

      try {
        const res = await fetch(`/api/listings/${activeChatListing.id}/messages`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            from_phone: currentUser.phone,
            to_phone: activeChatPartnerPhone,
            body: body
          })
        });

        if (res.ok) {
          input.value = "";
          fetchChatMessages();
        } else {
          const err = await res.json();
          alert(err.detail || "Error sending message");
        }
      } catch (err) {
        console.error("Send message error:", err);
      }
    }

    function startChatPolling() {
      stopChatPolling();
      chatPollTimer = setInterval(() => {
        if (activeChatListing && activeChatPartnerPhone) {
          fetchChatMessages();
        }
      }, 2500);
    }

    function stopChatPolling() {
      if (chatPollTimer) {
        clearInterval(chatPollTimer);
        chatPollTimer = null;
      }
    }

    document.getElementById("chatModal").addEventListener("hidden.bs.modal", () => {
      stopChatPolling();
      activeChatListing = null;
      activeChatPartnerPhone = null;
    });

    // ============ Auth Submit Handlers ============
    async function handleLogin(e) {
      e.preventDefault();
      try {
        const res = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role: document.getElementById("loginRole").value,
            phone: document.getElementById("loginPhone").value,
            password: document.getElementById("loginPassword").value
          })
        });
        const data = await res.json();
        if (res.ok) {
          currentUser = data.user;
          localStorage.setItem("cc_user", JSON.stringify(currentUser));
          bootstrap.Modal.getInstance(document.getElementById("authModal")).hide();
          updateNavUserState();
          fetchListings();
          startSyncPolling();
          alert(`Welcome back, ${currentUser.name}!`);
        } else {
          alert(data.detail || "Login failed");
        }
      } catch (err) {
        console.error("Login error:", err);
      }
    }

    async function handleRegister(e) {
      e.preventDefault();
      try {
        const res = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role: document.getElementById("regRole").value,
            name: document.getElementById("regName").value,
            phone: document.getElementById("regPhone").value,
            zip_code: document.getElementById("regZip").value,
            password: document.getElementById("regPassword").value
          })
        });
        const data = await res.json();
        if (res.ok) {
          alert("Account created successfully! You can now log in.");
          setAuthTab("login");
        } else {
          alert(data.detail || "Registration failed");
        }
      } catch (err) {
        console.error("Register error:", err);
      }
    }

    // ============ App Init ============
    setLang(currentLang);
    updateNavUserState();
    fetchListings();
    startSyncPolling();
  </script>
</body>
</html>
"""