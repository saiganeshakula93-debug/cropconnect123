import re
import json
import os
import hashlib
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, Form, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="CropConnect")

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

def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def load_users() -> dict:
    """Read users from disk. Create the file with a default test user if missing."""
    if not os.path.exists(USERS_FILE):
        seed = {
            "+1234567890": {
                "name": "Farmer John",
                "phone": "+1234567890",
                "zip_code": "90210",
                "role": "FARMER",
                "password": hash_password("password123")
            }
        }
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
        return seed
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users: dict) -> None:
    """Write users to disk after any change."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

USERS_DB = load_users()


def load_listings() -> list:
    """Read listings from disk. Create with seed data if missing."""
    if not os.path.exists(LISTINGS_FILE):
        seed = [
            {
                "id": 1,
                "farmer_name": "Farmer John",
                "farmer_phone": "+1234567890",
                "crop_name": "TOMATO",
                "quantity_kg": 50,
                "price_per_kg": 30,
                "zip_code": "90210",
                "source": "SMS"
            },
            {
                "id": 2,
                "farmer_name": "Sarah Smith",
                "farmer_phone": "+1987654321",
                "crop_name": "POTATO",
                "quantity_kg": 120,
                "price_per_kg": 15,
                "zip_code": "10001",
                "source": "WEB"
            }
        ]
        with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
        return seed
    with open(LISTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_listings(items: list) -> None:
    with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

LISTINGS_DB = load_listings()


def load_messages() -> list:
    """Read messages from disk. Empty list if file missing."""
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_messages(items: list) -> None:
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

MESSAGES_DB = load_messages()


def load_orders() -> list:
    """Read batch order requests from disk. Empty list if file missing."""
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_orders(items: list) -> None:
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

ORDERS_DB = load_orders()


# ==========================================
# FASTAPI BACKEND API SCHEMAS & HELPERS
# ==========================================

class RegisterSchema(BaseModel):
    name: str
    phone: str
    zip_code: str
    role: str
    password: str

class LoginSchema(BaseModel):
    phone: str
    password: str
    role: str

class CreateOrderSchema(BaseModel):
    listing_id: int
    buyer_phone: str
    quantity_kg: int
    notes: Optional[str] = None

class CreateListingSchema(BaseModel):
    crop_name: str
    quantity_kg: int
    price_per_kg: int
    zip_code: str
    farmer_phone: str  # identifies caller

class UpdateListingSchema(BaseModel):
    crop_name: Optional[str] = None
    quantity_kg: Optional[int] = None
    price_per_kg: Optional[int] = None
    zip_code: Optional[str] = None
    farmer_phone: str  # identifies caller

class SendMessageSchema(BaseModel):
    from_phone: str
    to_phone: str
    body: str


def require_user(phone: str) -> dict:
    """Look up caller and reject if unknown."""
    user = USERS_DB.get(phone)
    if not user:
        raise HTTPException(status_code=403, detail="Unknown phone number. Please log in.")
    return user

def require_role(phone: str, role: str) -> dict:
    """Require caller to exist AND have a specific role."""
    user = require_user(phone)
    if user["role"] != role:
        raise HTTPException(status_code=403, detail=f"This action is for {role}s only.")
    return user


# ==========================================
# FASTAPI BACKEND API ENDPOINTS
# ==========================================

@app.post("/api/register")
def register_user(data: RegisterSchema):
    if data.phone in USERS_DB:
        raise HTTPException(status_code=400, detail="Phone number already registered.")

    USERS_DB[data.phone] = {
        "name": data.name,
        "phone": data.phone,
        "zip_code": data.zip_code,
        "role": data.role,
        "password": hash_password(data.password),
    }
    save_users(USERS_DB)
    safe_user = {k: v for k, v in USERS_DB[data.phone].items() if k != "password"}
    return {"message": "Account created successfully!", "user": safe_user}

@app.post("/api/login")
def login_user(data: LoginSchema):
    user = USERS_DB.get(data.phone)
    if not user or user["password"] != hash_password(data.password) or user["role"] != data.role:
        raise HTTPException(status_code=401, detail="Invalid phone, password, or account type.")
    safe_user = {k: v for k, v in user.items() if k != "password"}
    return {"message": "Login successful", "user": safe_user}

@app.get("/api/listings")
def get_listings(crop: Optional[str] = None, zip_code: Optional[str] = None):
    # Only return listings with available quantity > 0
    results = [l for l in LISTINGS_DB if l.get("quantity_kg", 0) > 0]
    if crop and crop.strip():
        results = [l for l in results if crop.strip().lower() in l["crop_name"].lower()]
    if zip_code and zip_code.strip():
        results = [l for l in results if l["zip_code"] == zip_code.strip()]
    return results

# ----- Batch Orders Endpoints -----
@app.post("/api/order")
def place_order(data: CreateOrderSchema):
    buyer = require_role(data.buyer_phone, "BUYER")
    listing = next((l for l in LISTINGS_DB if l["id"] == data.listing_id), None)
    if not listing or listing.get("quantity_kg", 0) <= 0:
        raise HTTPException(status_code=404, detail="Crop listing is no longer available or sold out.")

    if data.quantity_kg <= 0:
        raise HTTPException(status_code=400, detail="Requested quantity must be greater than 0.")

    if data.quantity_kg > listing["quantity_kg"]:
        raise HTTPException(
            status_code=400,
            detail=f"Requested quantity ({data.quantity_kg} KG) exceeds available stock ({listing['quantity_kg']} KG)."
        )

    total_price = data.quantity_kg * listing["price_per_kg"]
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
        "quantity_kg": data.quantity_kg,
        "price_per_kg": listing["price_per_kg"],
        "total_price": total_price,
        "status": "PENDING",
        "notes": (data.notes or "").strip(),
        "created_at": now_iso,
        "updated_at": now_iso
    }
    ORDERS_DB.insert(0, new_order)
    save_orders(ORDERS_DB)

    # Automatically notify farmer via chat
    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    auto_msg = {
        "id": msg_id,
        "listing_id": listing["id"],
        "crop_name": listing["crop_name"],
        "from_phone": buyer["phone"],
        "from_name": buyer["name"],
        "to_phone": listing["farmer_phone"],
        "to_name": listing["farmer_name"],
        "body": f"📦 Batch Order Request #{new_order_id}: Requested {data.quantity_kg} KG of {listing['crop_name']} for ${total_price}." + (f" Note: {data.notes}" if data.notes else ""),
        "ts": now_iso
    }
    MESSAGES_DB.append(auto_msg)
    save_messages(MESSAGES_DB)

    return {
        "status": "SUCCESS",
        "message": f"Batch request for {data.quantity_kg} KG of {listing['crop_name']} sent to Farmer ({listing['farmer_name']}).",
        "order": new_order
    }

@app.get("/api/farmer/orders")
def get_farmer_orders(farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    return [o for o in ORDERS_DB if o["farmer_phone"] == farmer_phone]

@app.get("/api/buyer/orders")
def get_buyer_orders(buyer_phone: str):
    require_role(buyer_phone, "BUYER")
    return [o for o in ORDERS_DB if o["buyer_phone"] == buyer_phone]

@app.post("/api/orders/{order_id}/accept")
def accept_order(order_id: int, farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    order = next((o for o in ORDERS_DB if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order request not found.")
    if order["farmer_phone"] != farmer_phone:
        raise HTTPException(status_code=403, detail="You can only manage orders for your own crops.")
    if order["status"] != "PENDING":
        raise HTTPException(status_code=400, detail=f"Order is already {order['status'].lower()}.")

    # Locate listing and deduct quantity
    listing = next((l for l in LISTINGS_DB if l["id"] == order["listing_id"]), None)
    remaining_kg = 0

    if listing:
        if listing["quantity_kg"] < order["quantity_kg"]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot accept order: Available stock ({listing['quantity_kg']} KG) is less than requested quantity ({order['quantity_kg']} KG)."
            )
        
        listing["quantity_kg"] -= order["quantity_kg"]
        remaining_kg = listing["quantity_kg"]

        if listing["quantity_kg"] <= 0:
            # Fully sold out! Remove listing from active listings
            LISTINGS_DB.remove(listing)
        
        save_listings(LISTINGS_DB)

    now_iso = datetime.now(timezone.utc).isoformat()
    order["status"] = "ACCEPTED"
    order["updated_at"] = now_iso
    save_orders(ORDERS_DB)

    # Send chat confirmation to buyer
    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    accept_msg = {
        "id": msg_id,
        "listing_id": order["listing_id"],
        "crop_name": order["crop_name"],
        "from_phone": farmer_phone,
        "from_name": order["farmer_name"],
        "to_phone": order["buyer_phone"],
        "to_name": order["buyer_name"],
        "body": f"✅ Order Accepted! Your request for {order['quantity_kg']} KG of {order['crop_name']} (${order['total_price']}) has been approved.",
        "ts": now_iso
    }
    MESSAGES_DB.append(accept_msg)
    save_messages(MESSAGES_DB)

    return {
        "message": "Order accepted successfully! Inventory stock has been updated.",
        "order": order,
        "remaining_kg": remaining_kg
    }

@app.post("/api/orders/{order_id}/reject")
def reject_order(order_id: int, farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    order = next((o for o in ORDERS_DB if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order request not found.")
    if order["farmer_phone"] != farmer_phone:
        raise HTTPException(status_code=403, detail="You can only manage orders for your own crops.")
    if order["status"] != "PENDING":
        raise HTTPException(status_code=400, detail=f"Order is already {order['status'].lower()}.")

    now_iso = datetime.now(timezone.utc).isoformat()
    order["status"] = "REJECTED"
    order["updated_at"] = now_iso
    save_orders(ORDERS_DB)

    # Send chat notification to buyer
    msg_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    reject_msg = {
        "id": msg_id,
        "listing_id": order["listing_id"],
        "crop_name": order["crop_name"],
        "from_phone": farmer_phone,
        "from_name": order["farmer_name"],
        "to_phone": order["buyer_phone"],
        "to_name": order["buyer_name"],
        "body": f"❌ Order Declined: The batch request for {order['quantity_kg']} KG of {order['crop_name']} could not be accepted.",
        "ts": now_iso
    }
    MESSAGES_DB.append(reject_msg)
    save_messages(MESSAGES_DB)

    return {"message": "Order declined.", "order": order}

# ----- Listings CRUD (Farmers) -----
@app.post("/api/listings")
def create_listing(data: CreateListingSchema):
    farmer = require_role(data.farmer_phone, "FARMER")
    new_id = max([l["id"] for l in LISTINGS_DB], default=0) + 1
    new_listing = {
        "id": new_id,
        "farmer_name": farmer["name"],
        "farmer_phone": farmer["phone"],
        "crop_name": data.crop_name.upper().strip(),
        "quantity_kg": data.quantity_kg,
        "price_per_kg": data.price_per_kg,
        "zip_code": data.zip_code.strip(),
        "source": "WEB"
    }
    LISTINGS_DB.insert(0, new_listing)
    save_listings(LISTINGS_DB)
    return {"message": "Listing created successfully.", "listing": new_listing}

@app.put("/api/listings/{listing_id}")
def update_listing(listing_id: int, data: UpdateListingSchema):
    require_role(data.farmer_phone, "FARMER")
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    if listing["farmer_phone"] != data.farmer_phone:
        raise HTTPException(status_code=403, detail="You can only edit your own listings.")
    
    if data.crop_name is not None and data.crop_name.strip():
        listing["crop_name"] = data.crop_name.upper().strip()
    if data.quantity_kg is not None:
        listing["quantity_kg"] = data.quantity_kg
    if data.price_per_kg is not None:
        listing["price_per_kg"] = data.price_per_kg
    if data.zip_code is not None and data.zip_code.strip():
        listing["zip_code"] = data.zip_code.strip()
    
    save_listings(LISTINGS_DB)
    return {"message": "Listing updated successfully.", "listing": listing}

@app.delete("/api/listings/{listing_id}")
def delete_listing(listing_id: int, farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    if listing["farmer_phone"] != farmer_phone:
        raise HTTPException(status_code=403, detail="You can only delete your own listings.")
    
    LISTINGS_DB.remove(listing)
    save_listings(LISTINGS_DB)
    return {"message": "Listing deleted successfully."}

# ----- Chat per listing -----
@app.get("/api/listings/{listing_id}/messages")
def list_messages(listing_id: int, phone: str, partner_phone: Optional[str] = None):
    caller = require_user(phone)
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    
    if caller["role"] == "FARMER":
        if partner_phone:
            return [
                m for m in MESSAGES_DB
                if m["listing_id"] == listing_id and (
                    (m["from_phone"] == phone and m["to_phone"] == partner_phone) or
                    (m["from_phone"] == partner_phone and m["to_phone"] == phone)
                )
            ]
        else:
            return [
                m for m in MESSAGES_DB
                if m["listing_id"] == listing_id and (m["from_phone"] == phone or m["to_phone"] == phone)
            ]
    else:
        # Caller is Buyer
        farmer_p = partner_phone or (listing["farmer_phone"] if listing else None)
        if not farmer_p:
            existing = next((m for m in MESSAGES_DB if m["listing_id"] == listing_id and (m["from_phone"] == phone or m["to_phone"] == phone)), None)
            if existing:
                farmer_p = existing["to_phone"] if existing["from_phone"] == phone else existing["from_phone"]
        
        return [
            m for m in MESSAGES_DB
            if m["listing_id"] == listing_id and (
                (m["from_phone"] == phone and (not farmer_p or m["to_phone"] == farmer_p)) or
                (m["to_phone"] == phone and (not farmer_p or m["from_phone"] == farmer_p))
            )
        ]

@app.get("/api/listings/{listing_id}/conversations")
def list_conversations(listing_id: int, farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    listing_msgs = [
        m for m in MESSAGES_DB
        if m["listing_id"] == listing_id and (m["from_phone"] == farmer_phone or m["to_phone"] == farmer_phone)
    ]
    
    buyers_map = {}
    for m in listing_msgs:
        buyer_p = m["from_phone"] if m["from_phone"] != farmer_phone else m["to_phone"]
        buyer_user = USERS_DB.get(buyer_p, {})
        buyer_n = buyer_user.get("name", m.get("from_name" if m["from_phone"] == buyer_p else "to_name", buyer_p))
        if buyer_p not in buyers_map:
            buyers_map[buyer_p] = {
                "buyer_phone": buyer_p,
                "buyer_name": buyer_n,
                "last_message": m["body"],
                "last_ts": m["ts"],
                "msg_count": 1
            }
        else:
            buyers_map[buyer_p]["last_message"] = m["body"]
            buyers_map[buyer_p]["last_ts"] = m["ts"]
            buyers_map[buyer_p]["msg_count"] += 1
            
    return list(buyers_map.values())

@app.get("/api/farmer/inbox_counts")
def get_inbox_counts(farmer_phone: str):
    require_role(farmer_phone, "FARMER")
    counts = {}
    for m in MESSAGES_DB:
        if m["to_phone"] == farmer_phone or m["from_phone"] == farmer_phone:
            lid = m["listing_id"]
            buyer_p = m["from_phone"] if m["from_phone"] != farmer_phone else m["to_phone"]
            if lid not in counts:
                counts[lid] = set()
            counts[lid].add(buyer_p)
    return {str(lid): len(buyers) for lid, buyers in counts.items()}

@app.post("/api/listings/{listing_id}/messages")
def send_message(listing_id: int, data: SendMessageSchema):
    sender = require_user(data.from_phone)
    recipient = USERS_DB.get(data.to_phone, {})
    
    listing = next((l for l in LISTINGS_DB if l["id"] == listing_id), None)
    crop_name = listing["crop_name"] if listing else "CROP"
    
    new_id = max([m["id"] for m in MESSAGES_DB], default=0) + 1
    msg = {
        "id": new_id,
        "listing_id": listing_id,
        "crop_name": crop_name,
        "from_phone": data.from_phone,
        "from_name": sender.get("name", data.from_phone),
        "to_phone": data.to_phone,
        "to_name": recipient.get("name", data.to_phone),
        "body": data.body.strip(),
        "ts": datetime.now(timezone.utc).isoformat()
    }
    MESSAGES_DB.append(msg)
    save_messages(MESSAGES_DB)
    return {"message": "Sent.", "msg": msg}

# Twilio SMS Inbound Webhook Endpoint
@app.post("/sms/webhook")
async def twilio_sms_webhook(From: str = Form(...), Body: str = Form(...)):
    farmer = USERS_DB.get(From)

    if not farmer:
        reply = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect Error: Your phone is not registered. Please register on the website first.</Message></Response>"
        return Response(content=reply, media_type="text/xml")

    pattern = r'^SELL\s+([A-Za-z]+)\s+(\d+)KG\s+(\d+)/KG$'
    match = re.match(pattern, Body.strip(), re.IGNORECASE)

    if match:
        crop, qty, price = match.groups()
        new_id = max([l["id"] for l in LISTINGS_DB], default=0) + 1
        new_listing = {
            "id": new_id,
            "farmer_name": farmer["name"],
            "farmer_phone": farmer["phone"],
            "crop_name": crop.upper(),
            "quantity_kg": int(qty),
            "price_per_kg": int(price),
            "zip_code": farmer.get("zip_code", "90210"),
            "source": "SMS"
        }
        LISTINGS_DB.insert(0, new_listing)
        save_listings(LISTINGS_DB)
        reply = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect: Successfully listed {qty}KG of {crop.upper()} at ${price}/KG.</Message></Response>"
    else:
        reply = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>CropConnect Error: Invalid format. Use: SELL CROP QTYKG PRICE/KG (e.g. SELL TOMATO 50KG 30/KG)</Message></Response>"

    return Response(content=reply, media_type="text/xml")


# ==========================================
# FRONTEND HTML EMBEDDED RESPONSE
# ==========================================

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CropConnect</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    :root { --primary-green: #2e7d32; --accent-gold: #fbc02d; }
    .navbar-brand { font-weight: 700; color: var(--primary-green) !important; }
    .hero-section { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 2.5rem 0; }
    .card-listing { border: none; transition: transform 0.2s, box-shadow 0.2s; }
    .card-listing:hover { transform: translateY(-4px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .lang-flag { width: 22px; height: 22px; border-radius: 50%; display:inline-block; vertical-align:middle; margin-right:4px; font-size:11px; line-height:22px; text-align:center; color:#fff; font-weight:700; }
    .lang-en{background:#3b82f6;} .lang-hi{background:#f59e0b;} .lang-te{background:#ef4444;} .lang-ta{background:#10b981;}
    .dashboard-hero { background: linear-gradient(135deg, #fff8e1 0%, #c8e6c9 100%); padding: 1.5rem 0; }
    .chat-bubble { max-width: 82%; word-break: break-word; }
    .chat-msg-self { background-color: #2e7d32; color: #fff; border-bottom-right-radius: 2px; }
    .chat-msg-other { background-color: #ffffff; color: #212529; border: 1px solid #dee2e6; border-bottom-left-radius: 2px; }
    .chat-box { height: 330px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
    .buyer-tab-btn.active { background-color: #2e7d32 !important; color: white !important; }
  </style>
</head>
<body class="bg-light">

  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <i class="bi bi-tree-fill text-success fs-3 me-2"></i>
        <span data-i18n="app_name">CropConnect</span>
      </a>
      <div class="d-flex align-items-center gap-2 flex-wrap">
        <!-- Language switcher -->
        <div class="dropdown">
          <button class="btn btn-light border dropdown-toggle" type="button" data-bs-toggle="dropdown">
            <span id="langLabel">English</span>
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow">
            <li><a class="dropdown-item" href="#" onclick="setLang('en');return false;"><span class="lang-flag lang-en">EN</span>English</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('hi');return false;"><span class="lang-flag lang-hi">हि</span>हिन्दी (Hindi)</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('te');return false;"><span class="lang-flag lang-te">తె</span>తెలుగు (Telugu)</a></li>
            <li><a class="dropdown-item" href="#" onclick="setLang('ta');return false;"><span class="lang-flag lang-ta">த</span>தமிழ் (Tamil)</a></li>
          </ul>
        </div>
        <div id="navAuthBtns" class="d-flex gap-2">
          <button class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')" data-i18n="login">Log In</button>
          <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('register')" data-i18n="register">Register</button>
        </div>
        <div id="navUserArea" class="d-none d-flex align-items-center gap-2">
          <button class="btn btn-outline-success btn-sm d-none" id="navMyOrdersBtn" onclick="openMyOrdersModal()">
            <i class="bi bi-box-seam me-1"></i> <span data-i18n="my_orders">My Orders</span>
          </button>
          <span class="badge bg-success-subtle text-success border border-success-subtle px-2 py-1" id="navUserBadge"></span>
          <span class="text-dark fw-semibold" id="navUserName"></span>
          <button class="btn btn-outline-secondary btn-sm" onclick="logout()" data-i18n="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>

  <!-- ============ PUBLIC LANDING ============ -->
  <div id="publicView">
    <section class="hero-section text-center">
      <div class="container">
        <h1 class="fw-bold text-success" data-i18n="hero_title">Field to Consumer Market Board</h1>
        <p class="lead text-secondary" data-i18n="hero_subtitle">Buy directly from smallholder farmers or sell harvest via SMS.</p>
        <div class="alert alert-warning d-inline-block text-start shadow-sm mt-2 p-3 rounded">
          <i class="bi bi-phone-vibrate text-dark fs-4 me-2"></i>
          <span data-i18n="sms_hint_prefix">Farmers can text:</span>
          <code class="bg-white px-2 py-1 rounded border">SELL TOMATO 50KG 30/KG</code>
          <span data-i18n="sms_hint_suffix">to list harvest.</span>
        </div>
      </div>
    </section>
    <main class="container my-5 text-center">
      <p class="text-muted" data-i18n="please_login">Please log in or register to continue.</p>
      <button class="btn btn-success btn-lg" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')" data-i18n="login">Log In</button>
      <button class="btn btn-outline-success btn-lg ms-2" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('register')" data-i18n="register">Register</button>
    </main>
  </div>

  <!-- ============ FARMER DASHBOARD ============ -->
  <div id="farmerView" class="d-none">
    <section class="dashboard-hero text-center">
      <div class="container">
        <h2 class="fw-bold text-success mb-1"><span data-i18n="welcome">Welcome</span>, <span id="farmerName"></span>!</h2>
        <p class="text-secondary mb-0" data-i18n="farmer_tagline">Manage your harvest listings, orders, or list via SMS.</p>
      </div>
    </section>
    <main class="container my-4">
      <!-- 1. Incoming Batch Requests Section -->
      <div class="card shadow-sm border-0 mb-4">
        <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
          <h5 class="fw-bold text-success mb-0">
            <i class="bi bi-box-seam-fill me-2 text-success"></i><span data-i18n="incoming_orders">Incoming Batch Requests</span>
          </h5>
          <span class="badge bg-warning-subtle text-warning-emphasis border border-warning" id="pendingOrdersBadge">0 Pending</span>
        </div>
        <div class="card-body p-0">
          <div id="farmerOrdersContainer">
            <p class="text-muted small p-3 text-center mb-0" data-i18n="loading">Loading batch requests...</p>
          </div>
        </div>
      </div>

      <!-- 2. Active Listings Section -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="fw-bold text-success mb-0"><i class="bi bi-grid-fill me-1"></i> <span data-i18n="your_listings_title">Your Active Listings</span></h4>
        <button class="btn btn-success" onclick="openCreateListingModal()">
          <i class="bi bi-plus-circle me-1"></i> <span data-i18n="add_listing">+ Add Listing</span>
        </button>
      </div>
      <div class="row g-4">
        <div class="col-lg-8">
          <div class="card shadow-sm h-100 border-0">
            <div class="card-body p-0">
              <div id="farmerListings">
                <p class="text-muted small p-3" data-i18n="loading">Loading...</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card shadow-sm h-100 border-0">
            <div class="card-body">
              <h5 class="card-title text-success"><i class="bi bi-phone-vibrate"></i> <span data-i18n="how_to_list_title">How to list via SMS</span></h5>
              <p class="mb-2 text-secondary small" data-i18n="how_to_list_body">Send an SMS in this exact format:</p>
              <div class="bg-light p-2 rounded text-center fw-bold mb-2 font-monospace">SELL CROP QTYKG PRICE/KG</div>
              <p class="small text-muted mb-1" data-i18n="example_label">Example:</p>
              <div class="bg-success-subtle text-success p-2 rounded text-center fw-bold mb-3 font-monospace">SELL TOMATO 50KG 30/KG</div>
              <p class="small mb-0"><span class="fw-semibold text-secondary" data-i18n="your_registered_phone">Your registered phone:</span><br><code id="farmerPhone" class="fs-6"></code></p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <!-- ============ BUYER MARKETPLACE ============ -->
  <div id="buyerView" class="d-none">
    <section class="dashboard-hero text-center">
      <div class="container">
        <h2 class="fw-bold text-success mb-1"><span data-i18n="welcome">Welcome</span>, <span id="buyerName"></span>!</h2>
        <p class="text-secondary mb-0" data-i18n="buyer_tagline">Browse fresh harvest from farmers near you.</p>
      </div>
    </section>
    <main class="container my-4">
      <div class="row g-3 mb-4 bg-white p-3 rounded shadow-sm align-items-center">
        <div class="col-md-5">
          <div class="input-group">
            <span class="input-group-text bg-light"><i class="bi bi-search"></i></span>
            <input type="text" id="searchInput" class="form-control" oninput="fetchListings()" data-i18n-attr="placeholder" data-i18n="search_placeholder" placeholder="Search crops (e.g. Tomato)...">
          </div>
        </div>
        <div class="col-md-4">
          <div class="input-group">
            <span class="input-group-text bg-light"><i class="bi bi-geo-alt"></i></span>
            <input type="text" id="zipInput" class="form-control" oninput="fetchListings()" data-i18n-attr="placeholder" data-i18n="zip_placeholder" placeholder="Zip Code (e.g. 90210)...">
          </div>
        </div>
        <div class="col-md-3">
          <button class="btn btn-success w-100" onclick="fetchListings()" data-i18n="filter_btn">Filter Listings</button>
        </div>
      </div>
      <div class="row g-4" id="listingsContainer"></div>
      <div id="noListings" class="text-center text-muted d-none my-4 py-5" data-i18n="no_listings">No listings match your search.</div>
    </main>
  </div>

  <!-- ============ MODALS ============ -->

  <!-- Auth Modal -->
  <div class="modal fade" id="authModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
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
                  <label class="form-label small fw-semibold text-secondary">Account Role</label>
                  <select class="form-select" id="loginRole">
                    <option value="BUYER" data-i18n="buyer_label">Wholesale Buyer</option>
                    <option value="FARMER" data-i18n="farmer_label">Farmer</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="loginPhone" required data-i18n-attr="placeholder" data-i18n="phone_placeholder" placeholder="Phone Number">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="loginPassword" required data-i18n-attr="placeholder" data-i18n="password_placeholder" placeholder="Password">
                </div>
                <button type="submit" class="btn btn-success w-100 py-2 fw-semibold" data-i18n="sign_in">Sign In</button>
              </form>
            </div>
            <!-- REGISTER FORM -->
            <div class="tab-pane fade" id="register-pane">
              <form onsubmit="handleRegister(event)">
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary">Account Role</label>
                  <select class="form-select" id="regRole">
                    <option value="BUYER" data-i18n="buyer_label">Wholesale Buyer</option>
                    <option value="FARMER" data-i18n="farmer_label">Farmer</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="name_placeholder">Full / Business Name</label>
                  <input type="text" class="form-control" id="regName" required data-i18n-attr="placeholder" data-i18n="name_placeholder" placeholder="Full / Business Name">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="regPhone" required data-i18n-attr="placeholder" data-i18n="phone_placeholder" placeholder="Phone Number">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="zip_code">Zip Code</label>
                  <input type="text" class="form-control" id="regZip" required data-i18n-attr="placeholder" data-i18n="zip_placeholder" placeholder="Zip Code">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="regPassword" required data-i18n-attr="placeholder" data-i18n="password_placeholder" placeholder="Password">
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
      <div class="modal-content border-0 shadow">
        <div class="modal-header">
          <h5 class="modal-title fw-bold text-success" id="listingModalTitle" data-i18n="new_listing_title">Add New Crop Listing</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSaveListing(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="listingId">
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="crop_name">Crop Name</label>
              <input type="text" class="form-control" id="listingCrop" required placeholder="e.g. TOMATO">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="quantity_kg">Quantity (KG)</label>
                <input type="number" min="1" class="form-control" id="listingQty" required placeholder="e.g. 50">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="price_per_kg_label">Price per KG ($)</label>
                <input type="number" min="1" class="form-control" id="listingPrice" required placeholder="e.g. 30">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="zip_code">Zip Code</label>
              <input type="text" class="form-control" id="listingZip" required placeholder="e.g. 90210">
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

  <!-- Request Batch Order Modal -->
  <div class="modal fade" id="orderModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title fw-bold" id="orderModalTitle" data-i18n="request_batch_title">Request Crop Batch</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSubmitOrder(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="orderListingId">
            <input type="hidden" id="orderPricePerKg">
            <div class="alert alert-light border mb-3">
              <div class="d-flex justify-content-between mb-1">
                <span class="fw-bold text-success fs-5" id="orderCropName">TOMATO</span>
                <span class="badge bg-success-subtle text-success fs-6" id="orderPriceBadge">$30/kg</span>
              </div>
              <small class="text-muted d-block">
                <span data-i18n="seller">Seller</span>: <strong id="orderFarmerName">Farmer John</strong> (<span id="orderFarmerPhone"></span>)
              </small>
              <small class="text-muted d-block">
                <span data-i18n="available_stock">Available Stock</span>: <strong id="orderAvailableQty" class="text-dark">50</strong> KG
              </small>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="request_qty">Quantity to Buy (KG)</label>
              <input type="number" min="1" class="form-control form-control-lg" id="orderQuantityInput" oninput="updateOrderTotal()" required>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="order_notes">Notes / Delivery Instructions (Optional)</label>
              <textarea class="form-control" id="orderNotesInput" rows="2" placeholder="e.g. Need delivery by Friday"></textarea>
            </div>
            <div class="p-3 bg-light rounded d-flex justify-content-between align-items-center">
              <span class="fw-semibold text-secondary" data-i18n="total_price_est">Total Estimated Price:</span>
              <span class="fs-4 fw-bold text-success" id="orderTotalPriceEst">$0</span>
            </div>
          </div>
          <div class="modal-footer bg-light">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" data-i18n="cancel">Cancel</button>
            <button type="submit" class="btn btn-success fw-semibold" data-i18n="submit_request">Submit Batch Request</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Buyer My Orders Modal -->
  <div class="modal fade" id="myOrdersModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg modal-dialog-scrollable">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title fw-bold"><i class="bi bi-box-seam me-2"></i><span data-i18n="my_orders">My Orders</span></h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-0">
          <div id="buyerOrdersList">
            <p class="text-muted p-4 text-center my-auto" data-i18n="loading">Loading your orders...</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Chat Modal -->
  <div class="modal fade" id="chatModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-success text-white">
          <div>
            <h5 class="modal-title fw-bold mb-0"><i class="bi bi-chat-dots-fill me-2"></i><span id="chatCropTitle">Crop Chat</span></h5>
            <small class="text-white-50" id="chatPartnerTitle"></small>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        
        <!-- Farmer Buyer Selection Bar -->
        <div id="farmerBuyerBar" class="d-none bg-light p-2 border-bottom">
          <small class="text-muted d-block mb-1 fw-semibold" data-i18n="select_buyer">Select Buyer:</small>
          <div class="d-flex gap-1 flex-wrap" id="farmerBuyerPills"></div>
        </div>

        <div class="modal-body p-3 bg-light">
          <div class="chat-box" id="chatMessagesList">
            <p class="text-muted small text-center my-auto" data-i18n="loading">Loading messages...</p>
          </div>
        </div>
        <div class="modal-footer p-2 bg-white">
          <form class="input-group" onsubmit="handleSendMessage(event)" id="chatForm">
            <input type="text" class="form-control" id="chatInputText" required data-i18n-attr="placeholder" data-i18n="type_message" placeholder="Type a message...">
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
    // ============ i18n Dictionary ============
    const I18N = {
      en: {
        app_name: "CropConnect",
        login: "Log In", register: "Register", logout: "Logout",
        welcome: "Welcome",
        hero_title: "Field to Consumer Market Board",
        hero_subtitle: "Buy directly from smallholder farmers or sell harvest via SMS.",
        sms_hint_prefix: "Farmers can text:",
        sms_hint_suffix: "to list harvest.",
        please_login: "Please log in or register to continue.",
        buyer_label: "Wholesale Buyer", farmer_label: "Farmer",
        phone_placeholder: "Phone Number", password_placeholder: "Password",
        name_placeholder: "Full / Business Name", zip_placeholder: "Zip Code (e.g. 90210)...",
        sign_in: "Sign In", create_account: "Create Account",
        search_placeholder: "Search crops (e.g. Tomato)...",
        filter_btn: "Filter Listings", no_listings: "No listings match your search.",
        kg_left: "KG Left", zip: "Zip", seller: "Seller",
        price_per_kg: "/kg", request_batch: "Request Batch",
        source_listing: "Source", source_sms: "SMS", source_web: "WEB",
        farmer_tagline: "Manage your harvest listings, batch orders, or list via SMS.",
        buyer_tagline: "Browse fresh harvest from farmers near you.",
        how_to_list_title: "How to list via SMS",
        how_to_list_body: "Send an SMS in this exact format:",
        example_label: "Example:",
        your_listings_title: "Your Active Listings",
        your_registered_phone: "Your registered phone:",
        your_no_listings: "You have no active listings yet. Click '+ Add Listing' or send an SMS!",
        loading: "Loading...",
        alert_login_first: "Please log in first to place an order request.",
        alert_welcome: "Welcome back, ",
        alert_register_ok: "Account created successfully! You can now log in.",
        add_listing: "+ Add Listing",
        new_listing_title: "Add New Crop Listing",
        edit_listing_title: "Edit Crop Listing",
        crop_name: "Crop Name",
        quantity_kg: "Quantity (KG)",
        price_per_kg_label: "Price per KG ($)",
        zip_code: "Zip Code",
        save: "Save Listing",
        cancel: "Cancel",
        edit: "Edit",
        delete: "Delete",
        chat: "Chat",
        chat_with_farmer: "Chat with Farmer",
        chat_title: "Crop Chat",
        send: "Send",
        type_message: "Type a message...",
        no_messages: "No messages yet. Start the conversation!",
        no_buyer_chats: "No buyer inquiries on this listing yet.",
        confirm_delete: "Are you sure you want to delete this listing?",
        listing_saved: "Listing saved successfully!",
        listing_deleted: "Listing deleted successfully!",
        select_buyer: "Select Buyer to chat with:",
        incoming_orders: "Incoming Batch Requests",
        request_batch_title: "Request Crop Batch",
        request_qty: "Quantity to Buy (KG)",
        total_price_est: "Total Estimated Price",
        available_stock: "Available Stock",
        order_notes: "Notes / Delivery Instructions (Optional)",
        submit_request: "Submit Batch Request",
        accept: "Accept Request",
        decline: "Decline",
        status_pending: "Pending",
        status_accepted: "Accepted",
        status_rejected: "Declined",
        order_accepted_msg: "Batch request accepted! Inventory stock has been updated.",
        order_rejected_msg: "Batch request declined.",
        sold_out: "Sold Out",
        no_orders_yet: "No batch requests received yet.",
        my_orders: "My Orders",
        confirm_accept_order: "Accept this batch request? This will deduct the inventory stock.",
        confirm_reject_order: "Decline this batch request?",
        you: "You"
      },
      hi: {
        app_name: "क्रॉपकनेक्ट",
        login: "लॉग इन", register: "पंजीकरण", logout: "लॉग आउट",
        welcome: "स्वागत है",
        hero_title: "खेत से उपभोक्ता तक सीधा बाज़ार",
        hero_subtitle: "छोटे किसानों से सीधे खरीदें या SMS से फसल बेचें।",
        sms_hint_prefix: "किसान इस तरह SMS भेजें:",
        sms_hint_suffix: "फसल सूचीबद्ध करने के लिए।",
        please_login: "जारी रखने के लिए कृपया लॉग इन या पंजीकरण करें।",
        buyer_label: "थोक खरीदार", farmer_label: "किसान",
        phone_placeholder: "फ़ोन नंबर", password_placeholder: "पासवर्ड",
        name_placeholder: "पूरा / व्यापार का नाम", zip_placeholder: "पिन कोड (जैसे 110001)...",
        sign_in: "साइन इन", create_account: "खाता बनाएं",
        search_placeholder: "फसल खोजें (जैसे टमाटर)...",
        filter_btn: "सूची फ़िल्टर करें", no_listings: "कोई सूची नहीं मिली।",
        kg_left: "किलो शेष", zip: "पिन कोड", seller: "विक्रेता",
        price_per_kg: "/किग्रा", request_batch: "ऑर्डर भेजें",
        source_listing: "स्रोत", source_sms: "SMS", source_web: "वेब",
        farmer_tagline: "अपनी फसल सूची, बैच ऑर्डर प्रबंधित करें या SMS द्वारा जोड़ें।",
        buyer_tagline: "अपने आस-पास के किसानों की ताज़ी फसल देखें।",
        how_to_list_title: "SMS से फसल कैसे जोड़ें",
        how_to_list_body: "इस प्रारूप में SMS भेजें:",
        example_label: "उदाहरण:",
        your_listings_title: "आपकी सक्रिय फसल सूचियां",
        your_registered_phone: "आपका पंजीकृत फ़ोन:",
        your_no_listings: "अभी कोई सूची नहीं है। '+ नई फसल जोड़ें' पर क्लिक करें या SMS भेजें!",
        loading: "लोड हो रहा है...",
        alert_login_first: "ऑर्डर देने के लिए कृपया पहले लॉग इन करें।",
        alert_welcome: "वापसी पर स्वागत है, ",
        alert_register_ok: "खाता सफलतापूर्वक बन गया! अब आप लॉग इन कर सकते हैं।",
        add_listing: "+ नई फसल जोड़ें",
        new_listing_title: "नई फसल सूची जोड़ें",
        edit_listing_title: "फसल सूची संपादित करें",
        crop_name: "फसल का नाम",
        quantity_kg: "मात्रा (किलो)",
        price_per_kg_label: "प्रति किलो मूल्य ($)",
        zip_code: "पिन कोड",
        save: "सूची सहेजें",
        cancel: "रद्द करें",
        edit: "संपादित करें",
        delete: "हटाएं",
        chat: "चैट",
        chat_with_farmer: "किसान से चैट करें",
        chat_title: "फसल चैट",
        send: "भेजें",
        type_message: "संदेश लिखें...",
        no_messages: "अभी कोई संदेश नहीं है। बातचीत शुरू करें!",
        no_buyer_chats: "इस फसल पर अभी कोई खरीदार पूछताछ नहीं है।",
        confirm_delete: "क्या आप वाकई इस सूची को हटाना चाहते हैं?",
        listing_saved: "सूची सफलतापूर्वक सहेजी गई!",
        listing_deleted: "सूची सफलतापूर्वक हटाई गई!",
        select_buyer: "चैट करने के लिए खरीदार चुनें:",
        incoming_orders: "आने वाले बैच अनुरोध",
        request_batch_title: "फसल बैच का अनुरोध करें",
        request_qty: "खरीदने की मात्रा (किलो)",
        total_price_est: "कुल अनुमानित मूल्य",
        available_stock: "उपलब्ध स्टॉक",
        order_notes: "टिप्पणियाँ / वितरण निर्देश (वैकल्पिक)",
        submit_request: "अनुरोध भेजें",
        accept: "स्वीकार करें",
        decline: "अस्वीकार करें",
        status_pending: "लंबित",
        status_accepted: "स्वीकृत",
        status_rejected: "अस्वीकृत",
        order_accepted_msg: "बैच अनुरोध स्वीकृत! स्टॉक अपडेट हो गया।",
        order_rejected_msg: "बैच अनुरोध अस्वीकृत।",
        sold_out: "समाप्त (Sold Out)",
        no_orders_yet: "अभी तक कोई बैच अनुरोध प्राप्त नहीं हुआ है।",
        my_orders: "मेरे ऑर्डर",
        confirm_accept_order: "क्या आप इस बैच अनुरोध को स्वीकार कर स्टॉक घटाना चाहते हैं?",
        confirm_reject_order: "क्या आप इस बैच अनुरोध को अस्वीकार करना चाहते हैं?",
        you: "आप"
      },
      te: {
        app_name: "క్రాప్‌కనెక్ట్",
        login: "లాగిన్", register: "నమోదు", logout: "లాగౌట్",
        welcome: "స్వాగతం",
        hero_title: "పొలం నుండి వినియోగదారునికి నేరుగా మార్కెట్",
        hero_subtitle: "చిన్న రైతుల నుండి నేరుగా కొనండి లేదా SMS ద్వారా పంట అమ్మండి.",
        sms_hint_prefix: "రైతులు ఇలా SMS పంపవచ్చు:",
        sms_hint_suffix: "పంటను జాబితా చేయడానికి.",
        please_login: "కొనసాగించడానికి దయచేసి లాగిన్ లేదా నమోదు చేయండి.",
        buyer_label: "హోల్‌సేల్ కొనుగోలుదారు", farmer_label: "రైతు",
        phone_placeholder: "ఫోన్ నంబర్", password_placeholder: "పాస్‌వర్డ్",
        name_placeholder: "పూర్తి / వ్యాపార పేరు", zip_placeholder: "పిన్ కోడ్ (ఉదా: 500001)...",
        sign_in: "సైన్ ఇన్", create_account: "ఖాతా సృష్టించండి",
        search_placeholder: "పంటలను శోధించండి (ఉదా: టమోటా)...",
        filter_btn: "జాబితాను ఫిల్టర్ చేయండి", no_listings: "మీ శోధనకు ఏ జాబితా దొరకలేదు.",
        kg_left: "కేజీ మిగిలి ఉంది", zip: "పిన్ కోడ్", seller: "అమ్మకందారు",
        price_per_kg: "/కేజీ", request_batch: "ఆర్డర్ పంపండి",
        source_listing: "మూలం", source_sms: "SMS", source_web: "వెబ్",
        farmer_tagline: "మీ పంట జాబితాలు, బ్యాచ్ ఆర్డర్లను నిర్వహించండి లేదా SMS ద్వారా చేర్చండి.",
        buyer_tagline: "మీ సమీపంలోని రైతుల తాజా పంటలను చూడండి.",
        how_to_list_title: "SMS ద్వారా పంటను ఎలా జాబితా చేయాలి",
        how_to_list_body: "ఈ ఫార్మాట్‌లో SMS పంపండి:",
        example_label: "ఉదాహరణ:",
        your_listings_title: "మీ క్రియాశీల జాబితాలు",
        your_registered_phone: "మీ నమోదైన ఫోన్:",
        your_no_listings: "మీకు ఇంకా జాబితాలు లేవు. '+ కొత్త పంటను జోడించండి' క్లిక్ చేయండి లేదా SMS పంపండి!",
        loading: "లోడ్ అవుతోంది...",
        alert_login_first: "ఆర్డర్ పంపడానికి దయచేసి ముందు లాగిన్ అవ్వండి.",
        alert_welcome: "తిరిగి స్వాగతం, ",
        alert_register_ok: "ఖాతా సృష్టించబడింది! మీరు ఇప్పుడు లాగిన్ అవ్వవచ్చు.",
        add_listing: "+ కొత్త పంటను జోడించండి",
        new_listing_title: "కొత్త పంట జాబితాను జోడించండి",
        edit_listing_title: "పంట జాబితాను సవరించండి",
        crop_name: "పంట పేరు",
        quantity_kg: "పరిమాణం (కేజీ)",
        price_per_kg_label: "కేజీ ధర ($)",
        zip_code: "పిన్ కోడ్",
        save: "భద్రపరచు",
        cancel: "రద్దు చేయి",
        edit: "సవరించు",
        delete: "తొలగించు",
        chat: "చాట్",
        chat_with_farmer: "రైతుతో చాట్ చేయండి",
        chat_title: "పంట చాట్",
        send: "పంపు",
        type_message: "సందేశాన్ని టైప్ చేయండి...",
        no_messages: "ఇంకా సందేశాలు లేవు. సంభాషణను ప్రారంభించండి!",
        no_buyer_chats: "ఈ పంటపై ఇంకా కొనుగోలుదారుల సందేశాలు లేవు.",
        confirm_delete: "మీరు ఖచ్చితంగా ఈ జాబితాను తొలగించాలనుకుంటున్నారా?",
        listing_saved: "జాబితా విజయవంతంగా భద్రపరచబడింది!",
        listing_deleted: "జాబితా విజయవంతంగా తొలగించబడింది!",
        select_buyer: "చాట్ చేయడానికి కొనుగోలుదారుని ఎంచుకోండి:",
        incoming_orders: "వచ్చిన బ్యాచ్ అభ్యర్థనలు",
        request_batch_title: "పంట బ్యాచ్ అభ్యర్థన",
        request_qty: "కొనుగోలు చేయవలసిన పరిమాణం (కేజీ)",
        total_price_est: "మొత్తం అంచనా ధర",
        available_stock: "అందుబాటులో ఉన్న నిల్వ",
        order_notes: "గమనికలు / డెలివరీ సూచనలు (ఐచ్ఛికం)",
        submit_request: "అభ్యర్థనను పంపండి",
        accept: "అంగీకరించు",
        decline: "తిరస్కరించు",
        status_pending: "పెండింగ్‌లో ఉంది",
        status_accepted: "అంగీకరించబడింది",
        status_rejected: "తిరస్కరించబడింది",
        order_accepted_msg: "బ్యాచ్ అభ్యర్థన అంగీకరించబడింది! నిల్వ నవీకరించబడింది.",
        order_rejected_msg: "బ్యాచ్ అభ్యర్థన తిరస్కరించబడింది.",
        sold_out: "పూర్తయింది (Sold Out)",
        no_orders_yet: "ఇంకా ఎలాంటి బ్యాచ్ అభ్యర్థనలు రాలేదు.",
        my_orders: "నా ఆర్డర్లు",
        confirm_accept_order: "ఈ బ్యాచ్ అభ్యర్థనను అంగీకరించి నిల్వను తగ్గించాలనుకుంటున్నారా?",
        confirm_reject_order: "ఈ బ్యాచ్ అభ్యర్థనను తిరస్కరించాలనుకుంటున్నారా?",
        you: "మీరు"
      },
      ta: {
        app_name: "கிராப்கனெக்ட்",
        login: "உள்நுழைவு", register: "பதிவு", logout: "வெளியேறு",
        welcome: "வரவேற்கிறோம்",
        hero_title: "பயிர் நேரடி சந்தை",
        hero_subtitle: "சிறு விவசாயிகளிடம் நேரடியாக வாங்கவும் அல்லது SMS மூலம் அறுவடை விற்கவும்.",
        sms_hint_prefix: "விவசாயிகள் இவ்வாறு SMS அனுப்பலாம்:",
        sms_hint_suffix: "அறுவடையைப் பட்டியலிட.",
        please_login: "தொடர உள்நுழையவும் அல்லது பதிவு செய்யவும்.",
        buyer_label: "மொத்த வாங்குபவர்", farmer_label: "விவசாயி",
        phone_placeholder: "தொலைபேசி எண்", password_placeholder: "கடவுச்சொல்",
        name_placeholder: "முழு / வணிகப் பெயர்", zip_placeholder: "அஞ்சல் குறியீடு (எ.கா: 600001)...",
        sign_in: "உள்நுழை", create_account: "கணக்கை உருவாக்கு",
        search_placeholder: "பயிர்களைத் தேடு (எ.கா: தக்காளி)...",
        filter_btn: "பட்டியலை வடிகட்டு", no_listings: "பட்டியல் எதுவும் இல்லை.",
        kg_left: "கிலோ உள்ளது", zip: "அஞ்சல் குறியீடு", seller: "விற்பவர்",
        price_per_kg: "/கிலோ", request_batch: "ஆர்டர் அனுப்பு",
        source_listing: "மூலம்", source_sms: "SMS", source_web: "வலை",
        farmer_tagline: "உங்கள் பயிர் பட்டியல்கள், தொகுதி ஆர்டர்களை நிர்வகிக்கவும் அல்லது SMS மூலம் சேர்க்கவும்.",
        buyer_tagline: "உங்களுக்கு அருகிலுள்ள விவசாயிகளின் புதிய அறுவடையைப் பாருங்கள்.",
        how_to_list_title: "SMS மூலம் எப்படிப் பட்டியலிடுவது",
        how_to_list_body: "இந்த வடிவத்தில் SMS அனுப்பவும்:",
        example_label: "உதாரணம்:",
        your_listings_title: "உங்கள் செயலில் உள்ள பட்டியல்கள்",
        your_registered_phone: "உங்கள் பதிவு செய்யப்பட்ட தொலைபேசி:",
        your_no_listings: "பட்டியல்கள் இல்லை. '+ புதிய பயிரைச் சேர்' அழுத்தவும் அல்லது SMS அனுப்பவும்!",
        loading: "ஏற்றுகிறது...",
        alert_login_first: "ஆர்டர் செய்ய முதலில் உள்நுழையவும்.",
        alert_welcome: "மீண்டும் வரவேற்கிறோம், ",
        alert_register_ok: "கணக்கு உருவாக்கப்பட்டது! இப்போது உள்நுழையலாம்.",
        add_listing: "+ புதிய பயிரைச் சேர்",
        new_listing_title: "புதிய பயிர் பட்டியல் சேர்க்க",
        edit_listing_title: "பயிர் பட்டியலைத் திருத்து",
        crop_name: "பயிர் பெயர்",
        quantity_kg: "அளவு (கிலோ)",
        price_per_kg_label: "ஒரு கிலோ விலை ($)",
        zip_code: "அஞ்சல் குறியீடு",
        save: "பட்டியலைச் சேமி",
        cancel: "ரத்து செய்",
        edit: "திருத்து",
        delete: "நீக்கு",
        chat: "உரையாடல்",
        chat_with_farmer: "விவசாயியுடன் உரையாடு",
        chat_title: "பயிர் உரையாடல்",
        send: "அனுப்பு",
        type_message: "செய்தியை உள்ளிடவும்...",
        no_messages: "செய்திகள் எதுவும் இல்லை. உரையாடலைத் தொடங்குங்கள்!",
        no_buyer_chats: "இந்த பயிரில் இன்னும் வாங்குபவர் செய்திகள் இல்லை.",
        confirm_delete: "இந்த பட்டியலை நிச்சயமாக நீக்க விரும்புகிறீர்களா?",
        listing_saved: "பட்டியல் வெற்றிகரமாக சேமிக்கப்பட்டது!",
        listing_deleted: "பட்டியல் வெற்றிகரமாக நீக்கப்பட்டது!",
        select_buyer: "உரையாட வாங்குபவரைத் தேர்ந்தெடுக்கவும்:",
        incoming_orders: "வந்த தொகுதி கோரிக்கைகள்",
        request_batch_title: "பயிர் தொகுதி கோரிக்கை",
        request_qty: "வாங்க வேண்டிய அளவு (கிலோ)",
        total_price_est: "மொத்த மதிப்பிடப்பட்ட விலை",
        available_stock: "இருப்பு அளவு",
        order_notes: "குறிப்புகள் / விநியோக வழிமுறைகள் (விருப்பத்தேர்வு)",
        submit_request: "கோரிக்கையை அனுப்பு",
        accept: "ஏற்றுக்கொள்",
        decline: "நிராகரி",
        status_pending: "நிலுவையில் உள்ளது",
        status_accepted: "ஏற்றுக்கொள்ளப்பட்டது",
        status_rejected: "நிராகரிக்கப்பட்டது",
        order_accepted_msg: "தொகுதி கோரிக்கை ஏற்றுக்கொள்ளப்பட்டது! இருப்பு புதுப்பிக்கப்பட்டது.",
        order_rejected_msg: "தொகுதி கோரிக்கை நிராகரிக்கப்பட்டது.",
        sold_out: "விற்றுத் தீர்ந்தது (Sold Out)",
        no_orders_yet: "தொகுதி கோரிக்கைகள் எதுவும் வரவில்லை.",
        my_orders: "எனது ஆர்டர்கள்",
        confirm_accept_order: "இந்த கோரிக்கையை ஏற்று இருப்பைக் குறைக்க விரும்புகிறீர்களா?",
        confirm_reject_order: "இந்த கோரிக்கையை நிராகரிக்க விரும்புகிறீர்களா?",
        you: "நீங்கள்"
      }
    };

    let currentLang = localStorage.getItem("cc_lang") || "en";
    let currentUser = JSON.parse(localStorage.getItem("cc_user") || "null");

    // Chat & sync state
    let activeChatListing = null;
    let activeChatPartnerPhone = null;
    let activeChatPartnerName = null;
    let chatPollTimer = null;
    let syncPollTimer = null;

    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem("cc_lang", lang);
      document.documentElement.lang = lang;
      applyTranslations();
    }

    function t(key) {
      return (I18N[currentLang] && I18N[currentLang][key]) || (I18N.en && I18N.en[key]) || key;
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

      if (currentUser) {
        if (currentUser.role === "BUYER") {
          renderBuyerListings(window._lastListings || []);
        } else {
          renderFarmerListings(window._lastFarmerListings || [], window._lastInboxCounts || {});
          renderFarmerOrders(window._lastFarmerOrders || []);
        }
      }
    }

    // ============ Auth & Routing ============
    function showView() {
      document.getElementById("publicView").classList.add("d-none");
      document.getElementById("farmerView").classList.add("d-none");
      document.getElementById("buyerView").classList.add("d-none");
      document.getElementById("navAuthBtns").classList.add("d-none");
      document.getElementById("navUserArea").classList.add("d-none");
      document.getElementById("navMyOrdersBtn").classList.add("d-none");

      stopSyncPolling();

      if (!currentUser) {
        document.getElementById("publicView").classList.remove("d-none");
        document.getElementById("navAuthBtns").classList.remove("d-none");
        return;
      }

      document.getElementById("navUserArea").classList.remove("d-none");
      document.getElementById("navUserArea").classList.add("d-flex");
      document.getElementById("navUserName").textContent = currentUser.name;
      document.getElementById("navUserBadge").textContent = currentUser.role === "FARMER" ? t("farmer_label") : t("buyer_label");

      if (currentUser.role === "FARMER") {
        document.getElementById("farmerView").classList.remove("d-none");
        document.getElementById("farmerName").textContent = currentUser.name;
        document.getElementById("farmerPhone").textContent = currentUser.phone;
        fetchFarmerListings();
        fetchFarmerOrders();
      } else {
        document.getElementById("buyerView").classList.remove("d-none");
        document.getElementById("buyerName").textContent = currentUser.name;
        document.getElementById("navMyOrdersBtn").classList.remove("d-none");
        fetchListings();
      }

      startSyncPolling();
    }

    function logout() {
      currentUser = null;
      localStorage.removeItem("cc_user");
      stopChatPolling();
      stopSyncPolling();
      showView();
    }

    function setAuthTab(tab) {
      new bootstrap.Tab(document.querySelector(`#${tab}-tab`)).show();
    }

    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
        ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }

    // ============ Real-time Sync Polling ============
    function startSyncPolling() {
      stopSyncPolling();
      syncPollTimer = setInterval(() => {
        if (!currentUser) return;
        if (currentUser.role === "BUYER") {
          fetchListings();
        } else if (currentUser.role === "FARMER") {
          fetchFarmerListings();
          fetchFarmerOrders();
        }
      }, 3000);
    }

    function stopSyncPolling() {
      if (syncPollTimer) {
        clearInterval(syncPollTimer);
        syncPollTimer = null;
      }
    }

    // ============ Buyer View API Calls ============
    async function fetchListings() {
      const searchEl = document.getElementById("searchInput");
      const zipEl = document.getElementById("zipInput");
      const crop = searchEl ? searchEl.value : "";
      const zip = zipEl ? zipEl.value : "";
      try {
        const res = await fetch(`/api/listings?crop=${encodeURIComponent(crop)}&zip_code=${encodeURIComponent(zip)}`);
        if (!res.ok) return;
        const data = await res.json();
        const str = JSON.stringify(data);
        if (window._lastListingsStr !== str) {
          window._lastListingsStr = str;
          window._lastListings = data;
          renderBuyerListings(data);
        }
      } catch (err) {
        console.error("fetchListings error:", err);
      }
    }

    function renderBuyerListings(data) {
      const container = document.getElementById("listingsContainer");
      const noEl = document.getElementById("noListings");
      container.innerHTML = "";
      if (!data || data.length === 0) {
        noEl.classList.remove("d-none");
        return;
      }
      noEl.classList.add("d-none");
      data.forEach(item => {
        const sourceLabel = item.source === "SMS" ? t("source_sms") : (item.source === "WEB" ? t("source_web") : item.source);
        container.innerHTML += `
          <div class="col-md-6 col-lg-4">
            <div class="card card-listing h-100 shadow-sm border-0">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h5 class="fw-bold text-success mb-0">${esc(item.crop_name)}</h5>
                  <span class="badge bg-success-subtle text-success border border-success-subtle">${item.quantity_kg} ${t("kg_left")}</span>
                </div>
                <p class="text-muted small mb-2">
                  <i class="bi bi-geo-alt-fill text-danger me-1"></i> ${t("zip")}: <strong>${esc(item.zip_code)}</strong> &nbsp;|&nbsp; 
                  <i class="bi bi-person-fill text-primary me-1"></i> ${t("seller")}: <strong>${esc(item.farmer_name)}</strong>
                </p>
                <div class="d-flex justify-content-between align-items-baseline mb-3">
                  <span class="fs-4 fw-bold text-dark">$${item.price_per_kg}<small class="fs-6 text-muted">${t("price_per_kg")}</small></span>
                  <span class="badge bg-secondary-subtle text-secondary small">${t("source_listing")}: ${sourceLabel}</span>
                </div>
                <div class="d-grid gap-2">
                  <button class="btn btn-outline-success btn-sm" onclick="openBuyerChat(${item.id}, '${esc(item.crop_name)}', '${esc(item.farmer_phone)}', '${esc(item.farmer_name)}')">
                    <i class="bi bi-chat-dots-fill me-1"></i> ${t("chat_with_farmer")}
                  </button>
                  <button class="btn btn-success btn-sm" onclick='openOrderModal(${JSON.stringify(item)})'>
                    <i class="bi bi-cart-check-fill me-1"></i> ${t("request_batch")}
                  </button>
                </div>
              </div>
            </div>
          </div>`;
      });
    }

    // ============ Batch Request (Order) Handlers ============
    function openOrderModal(item) {
      if (!currentUser) {
        alert(t("alert_login_first"));
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }
      document.getElementById("orderListingId").value = item.id;
      document.getElementById("orderPricePerKg").value = item.price_per_kg;
      document.getElementById("orderCropName").textContent = item.crop_name;
      document.getElementById("orderPriceBadge").textContent = `$${item.price_per_kg}/kg`;
      document.getElementById("orderFarmerName").textContent = item.farmer_name;
      document.getElementById("orderFarmerPhone").textContent = item.farmer_phone;
      document.getElementById("orderAvailableQty").textContent = item.quantity_kg;
      
      const qtyInput = document.getElementById("orderQuantityInput");
      qtyInput.max = item.quantity_kg;
      qtyInput.value = item.quantity_kg;
      document.getElementById("orderNotesInput").value = "";

      updateOrderTotal();
      new bootstrap.Modal(document.getElementById("orderModal")).show();
    }

    function updateOrderTotal() {
      const qty = parseInt(document.getElementById("orderQuantityInput").value, 10) || 0;
      const price = parseInt(document.getElementById("orderPricePerKg").value, 10) || 0;
      const total = qty * price;
      document.getElementById("orderTotalPriceEst").textContent = `$${total}`;
    }

    async function handleSubmitOrder(e) {
      e.preventDefault();
      if (!currentUser || currentUser.role !== "BUYER") return;

      const listing_id = parseInt(document.getElementById("orderListingId").value, 10);
      const quantity_kg = parseInt(document.getElementById("orderQuantityInput").value, 10);
      const notes = document.getElementById("orderNotesInput").value;

      try {
        const res = await fetch("/api/order", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            listing_id,
            buyer_phone: currentUser.phone,
            quantity_kg,
            notes
          })
        });

        const data = await res.json();
        if (res.ok) {
          bootstrap.Modal.getInstance(document.getElementById("orderModal")).hide();
          alert(data.message || "Batch request submitted successfully!");
          fetchListings();
        } else {
          alert(data.detail || "Error submitting batch request");
        }
      } catch (err) {
        console.error("Order submit error:", err);
      }
    }

    // ============ Farmer Orders & Accept/Reject Handlers ============
    async function fetchFarmerOrders() {
      if (!currentUser || currentUser.role !== "FARMER") return;
      try {
        const res = await fetch(`/api/farmer/orders?farmer_phone=${encodeURIComponent(currentUser.phone)}`);
        if (!res.ok) return;
        const orders = await res.json();
        const str = JSON.stringify(orders);
        if (window._lastFarmerOrdersStr !== str) {
          window._lastFarmerOrdersStr = str;
          window._lastFarmerOrders = orders;
          renderFarmerOrders(orders);
        }
      } catch (err) {
        console.error("fetchFarmerOrders error:", err);
      }
    }

    function renderFarmerOrders(orders) {
      const container = document.getElementById("farmerOrdersContainer");
      const badge = document.getElementById("pendingOrdersBadge");

      const pendingCount = (orders || []).filter(o => o.status === "PENDING").length;
      badge.textContent = `${pendingCount} ${t("status_pending")}`;
      if (pendingCount > 0) {
        badge.className = "badge bg-warning text-dark border";
      } else {
        badge.className = "badge bg-light text-secondary border";
      }

      if (!orders || orders.length === 0) {
        container.innerHTML = `<div class="text-center py-4 text-muted"><i class="bi bi-inbox fs-2 d-block mb-1"></i>${t("no_orders_yet")}</div>`;
        return;
      }

      container.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col">${t("crop_name")}</th>
                <th scope="col">${t("buyer_label")}</th>
                <th scope="col">${t("quantity_kg")}</th>
                <th scope="col">Total Price</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${orders.map(o => {
                let statusBadge = "";
                if (o.status === "PENDING") statusBadge = `<span class="badge bg-warning text-dark border">${t("status_pending")}</span>`;
                else if (o.status === "ACCEPTED") statusBadge = `<span class="badge bg-success">${t("status_accepted")}</span>`;
                else statusBadge = `<span class="badge bg-danger">${t("status_rejected")}</span>`;

                const actions = o.status === "PENDING" ? `
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-success fw-semibold" onclick="handleAcceptOrder(${o.id})">
                      <i class="bi bi-check-circle-fill me-1"></i> ${t("accept")}
                    </button>
                    <button class="btn btn-outline-danger" onclick="handleRejectOrder(${o.id})">
                      <i class="bi bi-x-circle-fill me-1"></i> ${t("decline")}
                    </button>
                    <button class="btn btn-outline-primary" title="${t("chat")}" onclick="openFarmerChat(${o.listing_id}, '${esc(o.crop_name)}')">
                      <i class="bi bi-chat-dots-fill"></i>
                    </button>
                  </div>` : `
                  <button class="btn btn-sm btn-outline-secondary" onclick="openFarmerChat(${o.listing_id}, '${esc(o.crop_name)}')">
                    <i class="bi bi-chat-dots-fill me-1"></i> ${t("chat")}
                  </button>`;

                return `
                <tr>
                  <td>
                    <strong class="text-success">${esc(o.crop_name)}</strong>
                    <small class="text-muted d-block" style="font-size:0.75rem;">Order #${o.id}</small>
                  </td>
                  <td>
                    <strong>${esc(o.buyer_name)}</strong>
                    <small class="text-muted d-block" style="font-size:0.75rem;">${esc(o.buyer_phone)}</small>
                  </td>
                  <td><strong>${o.quantity_kg} kg</strong></td>
                  <td><strong>$${o.total_price}</strong> <small class="text-muted">($${o.price_per_kg}/kg)</small></td>
                  <td>${statusBadge}</td>
                  <td class="text-end">${actions}</td>
                </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>`;
    }

    async function handleAcceptOrder(orderId) {
      if (!confirm(t("confirm_accept_order"))) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/accept?farmer_phone=${encodeURIComponent(currentUser.phone)}`, {
          method: "POST"
        });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || t("order_accepted_msg"));
          window._lastFarmerOrdersStr = "";
          window._lastFarmerStateStr = "";
          fetchFarmerOrders();
          fetchFarmerListings();
        } else {
          alert(data.detail || "Error accepting order");
        }
      } catch (err) {
        console.error("Accept order error:", err);
      }
    }

    async function handleRejectOrder(orderId) {
      if (!confirm(t("confirm_reject_order"))) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/reject?farmer_phone=${encodeURIComponent(currentUser.phone)}`, {
          method: "POST"
        });
        const data = await res.json();
        if (res.ok) {
          alert(data.message || t("order_rejected_msg"));
          window._lastFarmerOrdersStr = "";
          fetchFarmerOrders();
        } else {
          alert(data.detail || "Error declining order");
        }
      } catch (err) {
        console.error("Reject order error:", err);
      }
    }

    // ============ Buyer My Orders Modal ============
    async function openMyOrdersModal() {
      if (!currentUser || currentUser.role !== "BUYER") return;
      const listEl = document.getElementById("buyerOrdersList");
      listEl.innerHTML = `<p class="text-muted p-4 text-center my-auto">${t("loading")}</p>`;
      new bootstrap.Modal(document.getElementById("myOrdersModal")).show();

      try {
        const res = await fetch(`/api/buyer/orders?buyer_phone=${encodeURIComponent(currentUser.phone)}`);
        if (!res.ok) return;
        const orders = await res.json();

        if (orders.length === 0) {
          listEl.innerHTML = `<div class="text-center py-5 text-muted"><i class="bi bi-inbox fs-2 d-block mb-1"></i>You haven't requested any crop batches yet.</div>`;
          return;
        }

        listEl.innerHTML = `
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th scope="col">${t("crop_name")}</th>
                  <th scope="col">${t("seller")}</th>
                  <th scope="col">${t("quantity_kg")}</th>
                  <th scope="col">Total Price</th>
                  <th scope="col">Status</th>
                  <th scope="col" class="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                ${orders.map(o => {
                  let statusBadge = "";
                  if (o.status === "PENDING") statusBadge = `<span class="badge bg-warning text-dark border">${t("status_pending")}</span>`;
                  else if (o.status === "ACCEPTED") statusBadge = `<span class="badge bg-success">${t("status_accepted")}</span>`;
                  else statusBadge = `<span class="badge bg-danger">${t("status_rejected")}</span>`;

                  return `
                  <tr>
                    <td><strong>${esc(o.crop_name)}</strong></td>
                    <td>${esc(o.farmer_name)}</td>
                    <td><strong>${o.quantity_kg} kg</strong></td>
                    <td>$${o.total_price}</td>
                    <td>${statusBadge}</td>
                    <td class="text-end">
                      <button class="btn btn-sm btn-outline-success" onclick="openBuyerChat(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.farmer_phone)}', '${esc(o.farmer_name)}')">
                        <i class="bi bi-chat-dots-fill me-1"></i> ${t("chat")}
                      </button>
                    </td>
                  </tr>`;
                }).join("")}
              </tbody>
            </table>
          </div>`;
      } catch (err) {
        console.error("Fetch buyer orders error:", err);
      }
    }

    // ============ Farmer View API Calls & CRUD ============
    async function fetchFarmerListings() {
      if (!currentUser || currentUser.role !== "FARMER") return;
      try {
        const [resListings, resCounts] = await Promise.all([
          fetch(`/api/listings`),
          fetch(`/api/farmer/inbox_counts?farmer_phone=${encodeURIComponent(currentUser.phone)}`)
        ]);
        if (!resListings.ok) return;
        const all = await resListings.json();
        const counts = resCounts.ok ? await resCounts.json() : {};
        const mine = all.filter(l => l.farmer_phone === currentUser.phone);
        const stateStr = JSON.stringify({ mine, counts });
        if (window._lastFarmerStateStr !== stateStr) {
          window._lastFarmerStateStr = stateStr;
          window._lastFarmerListings = mine;
          window._lastInboxCounts = counts;
          renderFarmerListings(mine, counts);
        }
      } catch (err) {
        console.error("fetchFarmerListings error:", err);
      }
    }

    function renderFarmerListings(data, inboxCounts) {
      const el = document.getElementById("farmerListings");
      if (!data || data.length === 0) {
        el.innerHTML = `<div class="text-center py-4 text-muted"><i class="bi bi-inbox fs-1 d-block mb-2"></i>${t("your_no_listings")}</div>`;
        return;
      }
      const counts = inboxCounts || window._lastInboxCounts || {};
      el.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col">${t("crop_name")}</th>
                <th scope="col">${t("quantity_kg")}</th>
                <th scope="col">${t("price_per_kg_label")}</th>
                <th scope="col">${t("zip_code")}</th>
                <th scope="col">${t("source_listing")}</th>
                <th scope="col" class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              ${data.map(l => {
                const sourceBadge = l.source === 'SMS' ? 'bg-warning-subtle text-warning-emphasis' : 'bg-info-subtle text-info-emphasis';
                const sourceLabel = l.source === 'SMS' ? t("source_sms") : (l.source === 'WEB' ? t("source_web") : l.source);
                const buyerCount = counts[String(l.id)] || 0;
                const chatBadge = buyerCount > 0 ? `<span class="badge bg-danger rounded-pill ms-1">${buyerCount}</span>` : '';
                return `
                <tr>
                  <td><strong class="text-success">${esc(l.crop_name)}</strong></td>
                  <td>${l.quantity_kg} kg</td>
                  <td>$${l.price_per_kg}</td>
                  <td><span class="badge bg-light text-dark border">${esc(l.zip_code)}</span></td>
                  <td><span class="badge ${sourceBadge}">${sourceLabel}</span></td>
                  <td class="text-end">
                    <div class="btn-group btn-group-sm">
                      <button class="btn btn-outline-success" title="${t("chat")}" onclick="openFarmerChat(${l.id}, '${esc(l.crop_name)}')">
                        <i class="bi bi-chat-dots-fill"></i> ${chatBadge}
                      </button>
                      <button class="btn btn-outline-primary" title="${t("edit")}" onclick='openEditListingModal(${JSON.stringify(l)})'>
                        <i class="bi bi-pencil-fill"></i>
                      </button>
                      <button class="btn btn-outline-danger" title="${t("delete")}" onclick="handleDeleteListing(${l.id})">
                        <i class="bi bi-trash-fill"></i>
                      </button>
                    </div>
                  </td>
                </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>`;
    }

    function openCreateListingModal() {
      document.getElementById("listingId").value = "";
      document.getElementById("listingCrop").value = "";
      document.getElementById("listingQty").value = "";
      document.getElementById("listingPrice").value = "";
      document.getElementById("listingZip").value = currentUser ? currentUser.zip_code : "";
      document.getElementById("listingModalTitle").textContent = t("new_listing_title");
      new bootstrap.Modal(document.getElementById("listingModal")).show();
    }

    function openEditListingModal(item) {
      document.getElementById("listingId").value = item.id;
      document.getElementById("listingCrop").value = item.crop_name;
      document.getElementById("listingQty").value = item.quantity_kg;
      document.getElementById("listingPrice").value = item.price_per_kg;
      document.getElementById("listingZip").value = item.zip_code;
      document.getElementById("listingModalTitle").textContent = t("edit_listing_title");
      new bootstrap.Modal(document.getElementById("listingModal")).show();
    }

    async function handleSaveListing(e) {
      e.preventDefault();
      if (!currentUser || currentUser.role !== "FARMER") return;

      const id = document.getElementById("listingId").value;
      const crop_name = document.getElementById("listingCrop").value;
      const quantity_kg = parseInt(document.getElementById("listingQty").value, 10);
      const price_per_kg = parseInt(document.getElementById("listingPrice").value, 10);
      const zip_code = document.getElementById("listingZip").value;

      let res;
      if (id) {
        res = await fetch(`/api/listings/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            crop_name, quantity_kg, price_per_kg, zip_code,
            farmer_phone: currentUser.phone
          })
        });
      } else {
        res = await fetch(`/api/listings`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            crop_name, quantity_kg, price_per_kg, zip_code,
            farmer_phone: currentUser.phone
          })
        });
      }

      const data = await res.json();
      if (res.ok) {
        bootstrap.Modal.getInstance(document.getElementById("listingModal")).hide();
        window._lastFarmerStateStr = "";
        fetchFarmerListings();
      } else {
        alert(data.detail || "Error saving listing");
      }
    }

    async function handleDeleteListing(listingId) {
      if (!confirm(t("confirm_delete"))) return;
      const res = await fetch(`/api/listings/${listingId}?farmer_phone=${encodeURIComponent(currentUser.phone)}`, {
        method: "DELETE"
      });
      const data = await res.json();
      if (res.ok) {
        window._lastFarmerStateStr = "";
        window._lastListingsStr = "";
        fetchFarmerListings();
      } else {
        alert(data.detail || "Error deleting listing");
      }
    }

    // ============ Robust Chat System ============
    function openBuyerChat(listingId, cropName, farmerPhone, farmerName) {
      if (!currentUser) {
        alert(t("alert_login_first"));
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }

      activeChatListing = { id: listingId, crop_name: cropName, farmer_phone: farmerPhone, farmer_name: farmerName };
      activeChatPartnerPhone = farmerPhone;
      activeChatPartnerName = farmerName;

      document.getElementById("chatCropTitle").textContent = `${cropName} - ${t("chat_title")}`;
      document.getElementById("chatPartnerTitle").textContent = `${t("seller")}: ${farmerName} (${farmerPhone})`;
      document.getElementById("farmerBuyerBar").classList.add("d-none");
      document.getElementById("chatInputText").value = "";
      document.getElementById("chatInputText").disabled = false;
      document.getElementById("chatSendBtn").disabled = false;

      const modal = new bootstrap.Modal(document.getElementById("chatModal"));
      modal.show();

      fetchChatMessages();
      startChatPolling();
    }

    async function openFarmerChat(listingId, cropName) {
      if (!currentUser || currentUser.role !== "FARMER") return;

      activeChatListing = { id: listingId, crop_name: cropName, farmer_phone: currentUser.phone, farmer_name: currentUser.name };
      activeChatPartnerPhone = null;
      activeChatPartnerName = null;

      document.getElementById("chatCropTitle").textContent = `${cropName} - ${t("chat_title")}`;
      document.getElementById("chatPartnerTitle").textContent = `${t("your_listings_title")}`;
      document.getElementById("chatInputText").value = "";

      const modal = new bootstrap.Modal(document.getElementById("chatModal"));
      modal.show();

      await loadFarmerConversations(listingId);
      startChatPolling();
    }

    async function loadFarmerConversations(listingId) {
      const bar = document.getElementById("farmerBuyerBar");
      const pills = document.getElementById("farmerBuyerPills");
      const msgList = document.getElementById("chatMessagesList");

      try {
        const res = await fetch(`/api/listings/${listingId}/conversations?farmer_phone=${encodeURIComponent(currentUser.phone)}`);
        if (!res.ok) return;
        const convos = await res.json();

        if (convos.length === 0) {
          bar.classList.add("d-none");
          activeChatPartnerPhone = null;
          msgList.innerHTML = `<div class="text-center py-5 text-muted"><i class="bi bi-chat-square-text fs-1 d-block mb-2"></i>${t("no_buyer_chats")}</div>`;
          document.getElementById("chatInputText").disabled = true;
          document.getElementById("chatSendBtn").disabled = true;
          return;
        }

        bar.classList.remove("d-none");
        document.getElementById("chatInputText").disabled = false;
        document.getElementById("chatSendBtn").disabled = false;

        if (!activeChatPartnerPhone || !convos.some(c => c.buyer_phone === activeChatPartnerPhone)) {
          activeChatPartnerPhone = convos[0].buyer_phone;
          activeChatPartnerName = convos[0].buyer_name;
        }

        pills.innerHTML = convos.map(c => {
          const isActive = (c.buyer_phone === activeChatPartnerPhone);
          const btnClass = isActive ? "btn-success" : "btn-outline-secondary";
          return `
            <button class="btn btn-sm ${btnClass} buyer-tab-btn" onclick="selectFarmerBuyer('${esc(c.buyer_phone)}', '${esc(c.buyer_name)}')">
              <i class="bi bi-person-fill"></i> ${esc(c.buyer_name)} (${esc(c.buyer_phone)})
            </button>`;
        }).join("");

        document.getElementById("chatPartnerTitle").textContent = `Buyer: ${activeChatPartnerName} (${activeChatPartnerPhone})`;
        fetchChatMessages();
      } catch (err) {
        console.error("loadFarmerConversations error:", err);
      }
    }

    function selectFarmerBuyer(phone, name) {
      activeChatPartnerPhone = phone;
      activeChatPartnerName = name;
      if (activeChatListing) {
        loadFarmerConversations(activeChatListing.id);
      }
    }

    async function fetchChatMessages() {
      if (!activeChatListing || !currentUser) return;
      if (!activeChatPartnerPhone) return;

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
        container.innerHTML = `<p class="text-muted small text-center my-auto">${t("no_messages")}</p>`;
        return;
      }

      container.innerHTML = messages.map(m => {
        const isSelf = (m.from_phone === currentUser.phone);
        const alignClass = isSelf ? "align-self-end" : "align-self-start";
        const bubbleClass = isSelf ? "chat-msg-self" : "chat-msg-other";
        const senderName = isSelf ? t("you") : (m.from_name || m.from_phone);
        const timeStr = m.ts ? new Date(m.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "";

        return `
          <div class="chat-bubble p-2 rounded shadow-sm ${bubbleClass} ${alignClass}">
            <div class="d-flex justify-content-between align-items-center gap-2 mb-1">
              <small class="fw-bold ${isSelf ? 'text-white-50' : 'text-success'}">${esc(senderName)}</small>
              <small class="${isSelf ? 'text-white-50' : 'text-muted'}" style="font-size:0.7rem;">${timeStr}</small>
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
        if (currentUser.role === "FARMER" && activeChatListing) {
          fetchFarmerListings();
        }
      } else {
        const err = await res.json();
        alert(err.detail || "Error sending message");
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
      const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
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
        showView();
      } else {
        alert(data.detail);
      }
    }

    async function handleRegister(e) {
      e.preventDefault();
      const res = await fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
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
        alert(t("alert_register_ok"));
        setAuthTab("login");
      } else {
        alert(data.detail);
      }
    }

    // ============ Init ============
    setLang(currentLang);
    showView();
  </script>
</body>
</html>
"""