# CropConnect — Comprehensive Project Documentation

> **Project:** CropConnect — Direct Farm-to-Buyer Agri-Marketplace with Smart AI Logistics
> **Repository:** `https://github.com/saiganeshakula93-debug/cropconnect123.git`
> **Domain:** AgriTech / Marketplace / Last-Mile Logistics
> **Primary Goal:** Eliminate middlemen by directly connecting Farmers, FPOs, Bulk Buyers, and Consumers with AI-powered demand forecasting, fair pricing, and pooled 2-Opt route optimization.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Specifications](#2-project-specifications)
3. [Technology Stack & Languages](#3-technology-stack--languages)
4. [High-Level Architecture](#4-high-level-architecture)
5. [Complete Workflow (End-to-End)](#5-complete-workflow-end-to-end)
6. [Data Model & Persistence](#6-data-model--persistence)
7. [Module-by-Module Breakdown](#7-module-by-module-breakdown)
8. [Algorithms & Methods Used](#8-algorithms--methods-used)
9. [Working Principles](#9-working-principles)
10. [REST API Reference](#10-rest-api-reference)
11. [Frontend Architecture (SPA)](#11-frontend-architecture-spa)
12. [Twilio SMS Inbound Webhook](#12-twilio-sms-inbound-webhook)
13. [Multilingual Localization (i18n)](#13-multilingual-localization-i18n)
14. [Authentication & Role-Based Access](#14-authentication--role-based-access)
15. [Deployment & DevOps](#15-deployment--devops)
16. [Automated Test Suite](#16-automated-test-suite)
17. [Demo Login Accounts](#17-demo-login-accounts)
18. [Notable Technical Details](#18-notable-technical-details)

---

## 1. Executive Summary

CropConnect is a **unified digital agricultural marketplace** that bypasses the traditional multi-tier mandi (APMC) supply chain. It enables four distinct user roles to transact directly with transparent pricing in Indian Rupees (₹), AI-driven demand forecasting, and consolidated multi-stop logistics.

### Core Value Propositions

| Stakeholder | Traditional Chain | CropConnect Benefit |
|---|---|---|
| **Farmer / FPO** | Receives mandi distress rate (~₹18/kg tomato) | Earns **+45-50%** more (₹27-30/kg) |
| **Consumer / Bulk Buyer** | Pays supermarket retail (~₹42/kg) | Saves **25-30%** (₹28/kg) |
| **Supply Chain** | 3-4 middleman tiers, 25% post-harvest loss | **Zero** middleman cut, < 4.5% waste |
| **Logistics** | Individual trips, no optimization | **2-Opt pooled routing**, CO₂ reduction |

### Key Differentiators

- **SMS-first UX:** No smartphone needed — farmers can list via `SELL TOMATO 50KG 28/KG 500001`.
- **AI Demand Forecasting:** Recency-weighted regression + seasonal priors + perishability weighting.
- **2-Opt Route Optimization:** Solves the multi-drop Travelling Salesman Problem.
- **Multilingual (4 languages):** English, हिन्दी, తెలుగు, தமிழ்.
- **JSON-file database:** Zero-config persistence that survives restarts and works offline.

---

## 2. Project Specifications

### 2.1 Functional Requirements

1. **Multi-Role Authentication System**
   - Four roles: `FARMER`, `FPO`, `BULK_BUYER`, `CONSUMER`.
   - SHA-256 password hashing.
   - Lenient phone-number normalization (handles `+91` prefix and 10-digit formats).

2. **Direct Digital Marketplace**
   - CRUD operations on crop listings.
   - Search & filter by crop name, ZIP code, seller type.
   - Category chip filters (Tomatoes, Onions, Potatoes, Chillies, Fruits, Greens).
   - Transparent pricing: mandi baseline, direct price, retail benchmark all visible.
   - Minimum Order Quantity (MOQ) enforcement.
   - Bulk discount pricing (auto-applied for orders ≥ 50 KG).

3. **Order Lifecycle Management**
   - States: `PENDING` → `ACCEPTED` → `DISPATCHED` → `DELIVERED` (with `REJECTED` / `CANCELLED` branches).
   - Auto-inventory deduction on acceptance.
   - Auto-inventory restoration on cancellation.
   - Auto-message generation for every state transition.

4. **AI Demand Forecasting Engine**
   - Recency-weighted linear trend regression.
   - Crop-specific seasonal elasticity priors.
   - Shelf-life & spoilage risk scoring.
   - Supply-gap analysis (deficit/surplus detection).
   - Fair price advisor (₹/kg for both farmers and consumers).

5. **Smart Logistics & 2-Opt Route Optimization**
   - Nearest-neighbour seeding + 2-Opt local search.
   - Haversine geodesic distance with road circuity factor (1.25x).
   - Intelligent vehicle sizing (3-Wheeler / Pickup / Medium / Heavy Reefer).
   - Fuel cost & CO₂ savings calculation.
   - Trip dispatch and delivery confirmation.

6. **Supply Chain Transparency Analytics**
   - Side-by-side comparison: Traditional Mandi Chain vs CropConnect Direct.
   - Farmer income increase %, consumer savings %, waste reduction %.

7. **In-App Direct Chat**
   - Listing-scoped messaging between buyer and seller.
   - Auto-polling every 2.5 seconds for real-time feel.
   - Background sync polling every 4 seconds for listings & orders.

8. **Twilio SMS Inbound Webhook**
   - `PRICE <CROP>` — get AI fair price.
   - `SELL <CROP> <QTY>KG <PRICE>/KG [ZIP]` — list via SMS.
   - `ORDERS` — check pending orders.

9. **Multilingual SPA Frontend**
   - 4 languages: English, Hindi, Telugu, Tamil.
   - Full UI translation via `data-i18n` attribute system.
   - Persistent language preference (`localStorage`).

### 2.2 Non-Functional Requirements

| Requirement | Implementation |
|---|---|
| **Persistence** | JSON file-based DB (auto-saved on every mutation) |
| **Portability** | Pure Python 3.12; no native DB dependencies |
| **Scalability** | Stateless FastAPI; horizontal scaling ready |
| **Availability** | Health-checked at `/`; Railway auto-restart on failure (max 10 retries) |
| **CORS** | Wide-open (`allow_origins=["*"]`) for dev/demo |
| **Security** | SHA-256 password hashing; role-based access guards |
| **Localization** | All UI text + currency in ₹; 4 Indian languages |
| **Deployment** | Docker + Railway Nixpacks; PORT env variable |

---

## 3. Technology Stack & Languages

### 3.1 Backend

| Component | Technology | Version |
|---|---|---|
| **Primary Language** | Python | 3.12.7 |
| **Web Framework** | FastAPI | (latest) |
| **ASGI Server** | Uvicorn (with `[standard]` extras) | (latest) |
| **Data Validation** | Pydantic | (latest) |
| **Form Parsing** | python-multipart | (latest) |
| **Crypto** | hashlib (stdlib) — SHA-256 | stdlib |
| **Math** | math, datetime, re, json, os (stdlib) | stdlib |

### 3.2 Frontend (Embedded in `frontend.py`)

| Component | Technology |
|---|---|
| **Markup** | HTML5 |
| **Styling** | Custom CSS3 (warm, handcrafted design) + Bootstrap 5.3.2 |
| **Icons** | Bootstrap Icons 1.11.3 |
| **Typography** | Google Fonts (Plus Jakarta Sans + Outfit) |
| **Client Logic** | Vanilla JavaScript (ES6+, no framework) |
| **State Management** | `localStorage` + in-memory variables |
| **Polling** | `setInterval` (chat: 2.5s, sync: 4s) |

### 3.3 Data Layer

| Component | Technology |
|---|---|
| **Storage** | JSON files on disk (no SQL DB) |
| **Files** | `users.json`, `listings.json`, `orders.json`, `messages.json`, `trips.json` |
| **Concurrency** | Single-process (sufficient for demo/SIH scale) |

### 3.4 DevOps

| Component | Technology |
|---|---|
| **Containerization** | Docker (`python:3.12-slim` base) |
| **Cloud Platform** | Railway.app |
| **Build System** | Nixpacks (Railway default) |
| **Process Manager** | Railway restart policy (max 10 retries) |
| **Version Control** | Git + GitHub |

---

## 4. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT TIER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐    │
│  │  Web Browser │  │  SMS Gateway │  │  Twilio Webhook       │    │
│  │  (SPA UI)    │  │  (Feature    │  │  /sms/webhook         │    │
│  │              │  │   Phones)    │  │                       │    │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬───────────┘    │
└─────────┼─────────────────┼─────────────────────────┼──────────────┘
          │ HTTPS/JSON     │ SMS/Form                │ Twilio XML
          ▼                 ▼                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FASTAPI APPLICATION (main.py)                 │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Middleware: CORS (allow all for dev)                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐     │
│  │  Auth &    │ │ Marketplace│ │   Order    │ │  Direct    │     │
│  │  Users     │ │ & Listings │ │ Lifecycle  │ │  Chat      │     │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘     │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────────┐  │
│  │  AI Demand     │ │  Smart         │ │  Value Chain         │  │
│  │  Forecasting   │ │  Logistics     │ │  Analytics           │  │
│  │  Engine        │ │  2-Opt Solver  │ │                      │  │
│  └────────────────┘ └────────────────┘ └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PERSISTENCE LAYER (JSON File DB)                       │
│  users.json  │  listings.json  │  orders.json  │  messages.json  │  │
│                                                  trips.json       │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Frontend ↔ Backend:** All UI calls go through `/api/*` JSON endpoints.
2. **SMS ↔ Backend:** Twilio POSTs form-encoded data to `/sms/webhook`; backend returns TwiML XML.
3. **Backend ↔ Storage:** Every mutation triggers a synchronous JSON file rewrite.
4. **Background sync:** Frontend polls `/api/listings` and `/api/orders` every 4 seconds while a tab is active.

---

## 5. Complete Workflow (End-to-End)

### 5.1 User Onboarding Flow

```
┌──────────────────┐
│  Visitor arrives │
│  at /            │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│  Frontend SPA loads          │
│  (index.html embedded)       │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  User clicks "Register" or   │
│  "Log In" → Auth Modal       │
└────────┬─────────────────────┘
         │
         ├── Register ──► POST /api/register ──► users.json updated
         │
         └── Log In ────► POST /api/login ─────► SHA-256 password check
                          │
                          ▼
                   Returns user object
                   (excludes password)
                          │
                          ▼
                   localStorage.setItem("cc_user", ...)
                          │
                          ▼
                   updateNavUserState() ──► role badge + Seller Hub visible
```

### 5.2 Marketplace Browsing Flow

```
User lands on Marketplace tab
         │
         ▼
fetchListings() ──► GET /api/listings?crop=&zip_code=&seller_type=
         │
         ▼
Backend filters LISTINGS_DB:
  - quantity_kg > 0
  - crop name matches (case-insensitive substring)
  - zip code exact match
  - seller_type exact match
         │
         ▼
Returns active listings with fair pricing benchmarks
         │
         ▼
renderBuyerListings() ──► Bootstrap card grid with:
  - Crop emoji + name
  - Farmer/FPO badge
  - Price in ₹/kg + savings % vs retail
  - Quality grade + location + min order
  - Chat + Order buttons
```

### 5.3 Order Placement & Lifecycle Flow

```
┌────────────────────────────────────────────────────────────────┐
│  BUYER FLOW                                                    │
├────────────────────────────────────────────────────────────────┤
│  1. Click "Order Batch / Retail" on a listing card             │
│  2. openOrderModal(item) ──► orderModal pre-filled             │
│  3. User adjusts quantity + delivery address + lat/lon         │
│  4. updateOrderTotal() ──► live ₹ calculation + savings badge  │
│  5. Submit ──► POST /api/order                                 │
│     - Validates qty > 0                                        │
│     - Validates qty >= min_order_kg                            │
│     - Validates qty <= available stock                         │
│     - Auto-selects bulk price if qty >= 50                     │
│     - Inserts order with status PENDING                        │
│     - Auto-creates inbound message to seller                   │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  SELLER FLOW                                                    │
├────────────────────────────────────────────────────────────────┤
│  6. Seller sees PENDING order in "Orders & Requests" tab       │
│  7. Accept ──► POST /api/orders/{id}/accept                   │
│     - Verifies ownership (phone match)                         │
│     - Deducts quantity from listing.quantity_kg                │
│     - Marks listing SOLD_OUT if quantity_kg <= 0               │
│     - Sets order status = ACCEPTED                             │
│     - Sends confirmation message                               │
│  8. (Optional) Decline ──► POST /api/orders/{id}/reject        │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│  LOGISTICS DISPATCH FLOW                                        │
├────────────────────────────────────────────────────────────────┤
│  9. Seller clicks "Plan Delivery Route"                        │
│  10. autoLoadOrdersToLogistics() ──► loads all ACCEPTED orders │
│      into route textarea                                       │
│  11. runRouteOptimizer() ──► POST /api/logistics/optimize      │
│      - 2-Opt TSP solver                                        │
│      - Returns optimal sequence + vehicle recommendation       │
│  12. Click "Create & Dispatch Trip"                            │
│      ──► POST /api/logistics/dispatch                          │
│      - Creates trip record                                     │
│      - All included orders → status DISPATCHED                 │
│      - Sends dispatch SMS-style messages to buyers             │
│  13. After delivery, seller clicks "Mark Trip Delivered"        │
│      ──► POST /api/logistics/trips/{id}/deliver                │
│      - Trip + all orders → status DELIVERED                    │
└────────────────────────────────────────────────────────────────┘
```

### 5.4 AI Demand Forecasting Flow

```
User on AI Demand Forecast tab
         │
         ▼
Selects crop (TOMATO) + horizon (7/14/30 days)
         │
         ▼
GET /api/ai/demand-forecast?crop=TOMATO&days=7
         │
         ▼
┌────────────────────────────────────────────────────────────┐
│  BACKEND PROCESSING                                         │
├────────────────────────────────────────────────────────────┤
│  1. Lookup CROP_BENCHMARKS[TOMATO]:                        │
│     base_daily_kg=45, shelf_life=6, mandi_ref=18,          │
│     retail_ref=42, elasticity=1.25, season_factor=1.15     │
│                                                            │
│  2. _accepted_demand_by_day(TOMATO):                       │
│     - Walk ORDERS_DB                                       │
│     - Sum quantity_kg by created_at date                   │
│     - Exclude REJECTED, CANCELLED                          │
│                                                            │
│  3. If history >= 2 days:                                  │
│     - Recency-weighted linear regression                   │
│     - weights = 1.0 → 3.0 (linear ramp)                   │
│     - forecast = 0.75 * regression + 0.25 * seasonal       │
│     - trend = "rising"/"falling"/"stable"                  │
│     - confidence = 60 + (n*1.5) + (positive_days*3)        │
│     - method = "Recency-Weighted Linear Trend..."          │
│                                                            │
│  4. Else: fallback to benchmark prior                      │
│     - forecast = base_daily_kg * season_factor            │
│     - confidence = 68%                                     │
│                                                            │
│  5. Compute:                                               │
│     - total_forecast = forecast * days                     │
│     - recommended_stock = total_forecast * 1.15            │
│     - supply_gap = recommended_stock - current_supply      │
│     - fair_farmer_price = mandi_ref * 1.45                 │
│     - fair_consumer_price = retail_ref * 0.75              │
│     - spoilage_risk based on shelf_life                    │
│                                                            │
│  6. Generate daily_projection with sin() noise             │
└────────────────────────────────────────────────────────────┘
         │
         ▼
Frontend renders:
  - Trend badge (rising/falling/stable)
  - 4 metric cards (Demand, Supply, Gap, Target Stock)
  - SVG bar chart for daily demand
  - Farmer price (₹) + Consumer price (₹) recommendations
  - Natural-language recommendation message
```

### 5.5 SMS Inbound Flow (Feature-Phone Users)

```
Farmer sends SMS "SELL TOMATO 50KG 28/KG 500001" to Twilio number
         │
         ▼
Twilio POSTs to /sms/webhook (form-encoded: From, Body)
         │
         ▼
┌────────────────────────────────────────────────────────────┐
│  twilio_sms_webhook()                                       │
├────────────────────────────────────────────────────────────┤
│  1. find_user_by_phone(From) ──► verify registered          │
│     - If unknown: respond with registration prompt         │
│                                                            │
│  2. Parse Body:                                            │
│     - If starts with "PRICE": return AI price advisor     │
│     - If equals "ORDERS": return pending order summary    │
│     - If matches SELL regex: create new listing           │
│     - Else: send format help message                       │
│                                                            │
│  3. Return TwiML XML Response with <Message> body         │
└────────────────────────────────────────────────────────────┘
         │
         ▼
Twilio delivers SMS reply to farmer
```

---

## 6. Data Model & Persistence

### 6.1 Storage Strategy

The application uses a **JSON file-based database** with these properties:

- **Atomic-ish writes:** Every mutation rewrites the entire file (acceptable for the demo/SIH scale of 100s-1000s of records).
- **Auto-seeding:** On first load, if `users.json` / `listings.json` / `orders.json` are missing, seed data is written.
- **Schema migration:** On every load, missing fields are back-filled with defaults (e.g., adding `seller_type`, `mandi_price_per_kg` to legacy records).
- **No transactions:** Single-process write safety is sufficient for this use case.

### 6.2 Entity Schemas

#### User
```json
{
  "name": "string (full name or collective name)",
  "phone": "string (primary key, E.164 or 10-digit)",
  "zip_code": "string (6-digit Indian PIN)",
  "role": "FARMER | FPO | BULK_BUYER | CONSUMER",
  "password": "string (SHA-256 hex hash)"
}
```

#### Listing
```json
{
  "id": "int (auto-incrementing)",
  "farmer_name": "string",
  "farmer_phone": "string (FK to user)",
  "seller_type": "FARMER | FPO",
  "crop_name": "string (UPPERCASE, e.g. TOMATO)",
  "quantity_kg": "float (available stock)",
  "price_per_kg": "float (₹)",
  "mandi_price_per_kg": "float (₹, derived = price * 0.70)",
  "retail_market_price_per_kg": "float (₹, derived = price * 1.40)",
  "min_order_kg": "float (MOQ)",
  "bulk_price_per_kg": "float (₹ for 50+ KG orders)",
  "zip_code": "string",
  "location_name": "string (e.g. 'Shamshabad Farm Gate')",
  "lat": "float (origin latitude)",
  "lon": "float (origin longitude)",
  "quality_grade": "string (free-form description)",
  "harvest_date": "string (YYYY-MM-DD)",
  "shelf_life_days": "int",
  "source": "WEB | SMS",
  "status": "ACTIVE | SOLD_OUT"
}
```

#### Order
```json
{
  "id": "int",
  "listing_id": "int (FK)",
  "crop_name": "string (denormalized)",
  "farmer_phone": "string",
  "farmer_name": "string",
  "buyer_phone": "string",
  "buyer_name": "string",
  "buyer_role": "BULK_BUYER | CONSUMER",
  "quantity_kg": "float",
  "price_per_kg": "float (₹, bulk if applicable)",
  "total_price": "float (₹, quantity * price)",
  "status": "PENDING | ACCEPTED | REJECTED | DISPATCHED | DELIVERED | CANCELLED",
  "delivery_address": "string",
  "delivery_zip": "string",
  "delivery_lat": "float",
  "delivery_lon": "float",
  "notes": "string (optional)",
  "created_at": "string (ISO 8601 with timezone)",
  "updated_at": "string (ISO 8601 with timezone)"
}
```

#### Message
```json
{
  "id": "int",
  "listing_id": "int (FK to listing context)",
  "crop_name": "string (denormalized for quick display)",
  "from_phone": "string",
  "from_name": "string",
  "to_phone": "string",
  "to_name": "string",
  "body": "string (message text)",
  "ts": "string (ISO 8601 timestamp)"
}
```

#### Trip
```json
{
  "id": "int",
  "farmer_phone": "string",
  "farmer_name": "string",
  "origin_name": "string",
  "origin_lat": "float",
  "origin_lon": "float",
  "vehicle_type": "string",
  "vehicle_number": "string (e.g. 'TS-09-UB-8821')",
  "driver_name": "string",
  "driver_phone": "string",
  "stops": "List[{name, lat, lon, quantity_kg, order_id, address, phone}]",
  "order_ids": "List[int]",
  "total_distance_km": "float",
  "total_load_kg": "float",
  "estimated_travel_minutes": "int",
  "fuel_cost_est": "float (₹)",
  "co2_saved_kg": "float",
  "status": "DISPATCHED | DELIVERED",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

---

## 7. Module-by-Module Breakdown

### 7.1 `main.py` (~1,567 lines)

Organized into 12 logical sections:

| Section | Lines | Purpose |
|---|---|---|
| **Imports & App Setup** | 1-21 | FastAPI init, CORS middleware |
| **JSON DB Layer** | 23-413 | load/save functions, seed data for users/listings/orders/trips/messages |
| **Auth & Role Helpers** | 416-456 | `is_seller()`, `is_buyer()`, `find_user_by_phone()`, `require_seller()`, `require_buyer()` |
| **Pydantic Schemas** | 459-544 | Request/response validation models |
| **Auth Endpoints** | 550-591 | `/api/register`, `/api/login` |
| **Listings CRUD** | 594-701 | GET, POST, PUT, DELETE on `/api/listings` |
| **Order Endpoints** | 706-911 | Place order, list farmer/buyer orders, accept/reject/cancel |
| **Chat Endpoints** | 916-1020 | Listing-scoped messaging |
| **AI Demand Forecasting** | 1023-1166 | `_accepted_demand_by_day()`, `demand_forecast()` |
| **Smart Logistics** | 1169-1413 | Haversine, 2-Opt TSP, optimize/dispatch/deliver |
| **Value Distribution Analytics** | 1416-1467 | `get_value_distribution()` |
| **Twilio SMS Webhook** | 1470-1549 | `twilio_sms_webhook()` |
| **Frontend Serving** | 1552-1565 | Mounts `FRONTEND_HTML` at `/` |

### 7.2 `frontend.py` (~2,500 lines)

Single Python module containing the entire `FRONTEND_HTML` string constant.

| Section | Approx. Lines | Purpose |
|---|---|---|
| **HTML Head & CSS** | 1-340 | Custom warm-themed CSS + Bootstrap 5 |
| **Navbar & Hero** | 342-402 | Branding, language switcher, SMS helpline callout |
| **Tab Navigation** | 404-436 | 5 main tabs: Marketplace, Orders, AI, Logistics, Analytics |
| **Marketplace Tab** | 442-513 | Search, filters, category chips, listings grid |
| **Orders Tab** | 518-541 | Orders table with role-aware actions |
| **AI Forecast Tab** | 546-599 | Crop selector + horizon selector + results card |
| **Logistics Tab** | 604-669 | Origin/vehicle config + waypoint textarea + results + trips history |
| **Analytics Tab** | 674-700 | Value distribution comparison |
| **Modals** | 707-958 | Auth, Listing, Order, Chat modals |
| **Footer** | 960-977 | Branding + toll-free helpline |
| **i18n Dictionary** | 982-1203 | 4-language translation table (en, hi, te, ta) |
| **State & Helpers** | 1205-1269 | Language persistence, escape function, translation application |
| **Tab Switcher** | 1271-1286 | Show/hide tab content |
| **Nav User State** | 1295-1347 | Role badge, Seller Hub visibility, logout |
| **Marketplace JS** | 1380-1492 | Fetch, render listings cards |
| **Order Modal JS** | 1494-1579 | Open modal, calculate total, submit |
| **Orders Table JS** | 1581-1782 | Fetch, render, accept/reject/cancel handlers |
| **AI Forecast JS** | 1784-1899 | Run forecast, render bar chart, price cards |
| **Logistics JS** | 1901-2156 | Auto-import orders, parse waypoints, optimize, dispatch, mark delivered |
| **Analytics JS** | 2158-2269 | Fetch value distribution, render comparison cards |
| **Listing CRUD JS** | 2271-2343 | Open modal, save (create/update) |
| **Chat JS** | 2345-2463 | Open chat, fetch messages, send, poll every 2.5s |
| **Auth JS** | 2465-end | Login/register handlers, localStorage persistence |

### 7.3 `test_app.py` (~74 lines)

End-to-end test suite using FastAPI's `TestClient`. Validates 6 core flows:
1. Frontend serving
2. Listings retrieval
3. AI demand forecast
4. Value distribution analytics
5. Logistics route optimization
6. Twilio SMS webhook (both PRICE and SELL commands)

### 7.4 Data Files

| File | Records | Description |
|---|---|---|
| `users.json` | 10 users | Demo accounts + user-created registrations |
| `listings.json` | 7 listings | Tomato, Red Onion, Chilli, Potato, Banana, Cabbage, Carrot |
| `orders.json` | 3 orders | Sample orders in various states (PENDING, ACCEPTED) |
| `messages.json` | 14 messages | Sample chat history including auto-generated order messages |

---

## 8. Algorithms & Methods Used

### 8.1 Recency-Weighted Linear Regression (AI Forecasting)

**Purpose:** Predict next-day crop demand based on historical order volumes.

**Mathematical Formulation:**

Given n observed daily demand values `y₀, y₁, ..., y_{n-1}`:

1. **Weight Assignment (Linear Ramp):**
   ```
   w_i = 1.0 + (i / (n-1)) * 2.0    for i = 0, 1, ..., n-1
   ```
   Older days have weight 1.0; most recent day has weight 3.0.

2. **Weighted Means:**
   ```
   W = Σ w_i
   x̄ = Σ(i * w_i) / W
   ȳ = Σ(y_i * w_i) / W
   ```

3. **Weighted Slope & Intercept:**
   ```
   denom = Σ w_i * (i - x̄)²
   slope = Σ w_i * (i - x̄) * (y_i - ȳ) / denom
   intercept = ȳ - slope * x̄
   ```

4. **Forecast (Hybrid):**
   ```
   raw_daily = max(0, intercept + slope * n)
   forecast = 0.75 * raw_daily + 0.25 * (base_daily_kg * season_factor)
   ```
   The 75/25 mix balances recent history with crop-specific seasonal priors.

5. **Trend Classification:**
   ```
   threshold = max(0.05, ȳ * 0.03)
   trend = "rising" if slope > threshold
         | "falling" if slope < -threshold
         | "stable" otherwise
   ```

6. **Confidence Score:**
   ```
   confidence = min(95, 60 + n * 1.5 + min(20, positive_days * 3))
   ```
   More history → higher confidence; more non-zero days → higher confidence.

### 8.2 2-Opt Local Search (Route Optimization)

**Purpose:** Solve the multi-drop Travelling Salesman Problem (TSP) to find near-optimal delivery sequence.

**Algorithm Steps:**

1. **Nearest-Neighbour Seeding:**
   ```
   current = origin
   while unvisited:
       next = argmin(haversine(current, stop)) for stop in unvisited
       route.append(next)
       current = next
   ```

2. **2-Opt Local Improvement (Iterative):**
   ```
   improved = True
   while improved:
       improved = False
       for i in range(len(route) - 1):
           for j in range(i + 1, len(route)):
               new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
               if total_path_dist(new_route) < total_path_dist(route) - 0.01:
                   route = new_route
                   improved = True
                   break
   ```
   This reverses subsequences to eliminate "route crossings" until no improvement is found.

3. **Complexity:** O(n²) per iteration, O(n²) iterations in worst case → O(n⁴) overall. For n ≤ 20 stops (typical), this is sub-millisecond.

**Why 2-Opt?**
- Fast convergence for small n.
- Deterministic.
- Empirically gives 10-30% improvement over nearest-neighbour alone.
- Sufficient for last-mile delivery where n is small.

### 8.3 Haversine Distance with Road Circuity

**Purpose:** Compute realistic road distance between two GPS coordinates.

**Formula:**
```
R = 6371 km (Earth's radius)
φ₁, φ₂ = latitudes in radians
Δφ = (lat₂ - lat₁) in radians
Δλ = (lon₂ - lon₁) in radians

a = sin²(Δφ/2) + cos(φ₁) * cos(φ₂) * sin²(Δλ/2)
c = 2 * asin(√a)
crow_distance = R * c
road_distance = crow_distance * 1.25    # circuity factor
```

The **1.25x circuity factor** accounts for the fact that actual road distance is typically 25% longer than straight-line distance due to road networks, turns, and one-way streets.

### 8.4 Inventory Deduction Algorithm (Order Acceptance)

**Atomic-ish JSON file rewrite:**

```python
if order.status == "PENDING":
    listing = find(listings, listing.id == order.listing_id)
    if listing.quantity_kg < order.quantity_kg:
        raise 400  # Insufficient stock
    listing.quantity_kg -= order.quantity_kg
    if listing.quantity_kg <= 0:
        listing.status = "SOLD_OUT"
    order.status = "ACCEPTED"
save_listings()  # Full file rewrite
save_orders()    # Full file rewrite
```

If a buyer cancels an ACCEPTED order, the inventory is restored.

### 8.5 Vehicle Sizing Heuristic

```python
if total_load <= 80:
    vehicle = "Electric Cargo 3-Wheeler / 2-Wheeler Fleet"
    fuel_rate = ₹3.5/km
elif total_load <= 400:
    vehicle = "Mini Truck / Light Pickup (Tata Ace / Mahindra Bolero)"
    fuel_rate = ₹7.5/km
elif total_load <= 1200:
    vehicle = "Medium Commercial Vehicle (Ashok Leyland Dost / Eicher Pro)"
    fuel_rate = ₹12.0/km
else:
    vehicle = "Heavy Goods Carrier / Temperature-Controlled Reefer"
    fuel_rate = ₹18.0/km
```

Based on Indian commercial vehicle categories.

### 8.6 Phone Number Normalization

```python
def normalize_phone(phone):
    p = re.sub(r'[^\d+]', '', phone.strip())
    return p

def phones_match(p1, p2):
    n1, n2 = normalize_phone(p1), normalize_phone(p2)
    if n1 == n2: return True
    d1, d2 = re.sub(r'\D', '', n1), re.sub(r'\D', '', n2)
    if len(d1) >= 10 and len(d2) >= 10:
        return d1[-10:] == d2[-10:]  # Match last 10 digits (ignores +91)
    return False
```

Handles all common Indian phone formats: `+91-9876543210`, `9876543210`, `+919876543210`, etc.

### 8.7 Price Benchmarking (Fair Price Advisor)

```python
mandi_baseline = benchmark.mandi_ref       # e.g. ₹18/kg for tomato
farmer_price = mandi_baseline * 1.45       # ₹26.1/kg (+45% over mandi)
retail_baseline = benchmark.retail_ref     # e.g. ₹42/kg for tomato
consumer_price = retail_baseline * 0.75    # ₹31.5/kg (-25% vs retail)
```

Mathematically: a price somewhere between mandi and retail that benefits both parties.

### 8.8 Value Distribution Model

**Traditional Chain (per ₹100 consumer spend on Tomato):**
```
Farmer earns:    ₹18.0  (18%)
Village middle:  ₹4.5   (4.5%)
Mandi commiss:   ₹6.3   (6.3%)
Wholesaler:      ₹5.4   (5.4%)
Retailer:        ₹6.3   (6.3%)
Spoilage:        25%
─────────────────────
Consumer pays:   ₹42.0
```

**CropConnect Direct (per ₹100 consumer spend):**
```
Farmer earns:    ₹27.0  (+50% vs mandi)
Logistics cost:  ₹3.6   (8.6%)
Middleman cut:   ₹0.0   (0% — eliminated)
─────────────────────
Consumer pays:   ₹30.6  (-27% vs retail)
Spoilage:        4.5%
```

The math: `mandi * 1.50` for farmer realization; `logistics = mandi * 0.20`; `consumer_pays = farmer + logistics`.

---

## 9. Working Principles

### 9.1 Design Principles

1. **No-Friction Onboarding:** SMS-first design for feature-phone users.
2. **Transparent Pricing:** Every listing shows mandi rate, direct price, and retail benchmark.
3. **Direct Linkage:** Zero middleman cut — buyer pays farmer + logistics only.
4. **Smart Defaults:** Bulk auto-discount at 50 KG, vehicle auto-selection, price advisor.
5. **Resilience:** File-based DB means zero infrastructure dependencies; works offline.
6. **Localization:** UI and SMS replies in farmer's native language.
7. **Data Persistence:** Every mutation immediately flushed to disk.

### 9.2 Role-Based Workflow Differentiation

| Action | FARMER/FPO | BULK_BUYER/CONSUMER |
|---|---|---|
| View listings | ✓ | ✓ |
| Create listing | ✓ | ✗ |
| Edit/delete own listing | ✓ | ✗ |
| Place order | ✗ | ✓ |
| Accept/reject order | ✓ (own crops) | ✗ |
| Cancel order | ✗ | ✓ (own orders) |
| Dispatch trip | ✓ | ✗ |
| Mark delivered | ✓ | ✗ |
| Chat with other party | ✓ | ✓ |

### 9.3 Order State Machine

```
        ┌──────────┐
   ┌───►│ PENDING  │◄─── (Buyer places order)
   │    └────┬─────┘
   │         │
   │    ┌────┴─────────────┐
   │    │                  │
   │    ▼                  ▼
   │ ┌────────┐      ┌──────────┐
   │ │ACCEPTED│      │ REJECTED │ (Seller declines)
   │ └───┬────┘      └──────────┘
   │     │
   │     │ (Logistics dispatched)
   │     ▼
   │ ┌──────────┐
   │ │DISPATCHED│
   │ └────┬─────┘
   │      │ (Delivery confirmed)
   │      ▼
   │ ┌──────────┐
   │ │ DELIVERED│
   │ └──────────┘
   │
   │ (Buyer/Seller can CANCEL from PENDING or ACCEPTED)
   ▼
┌──────────┐
│CANCELLED │
└──────────┘
```

### 9.4 Concurrency Model

- **Single-process FastAPI** → no race conditions on JSON writes (Python GIL + synchronous request handling).
- **Stateless requests** → horizontal scaling possible behind a load balancer (though JSON files would need to be moved to a shared store like S3 or a real DB).
- **For SIH scale (single demo server):** the design is sufficient.

### 9.5 Error Handling Strategy

- All Pydantic schemas validate types at request entry.
- Business logic raises `HTTPException(status_code, detail)` for known errors.
- Frontend catches `res.ok === false` and displays `data.detail` via `alert()`.
- SMS webhook always returns valid TwiML XML (even on error) to prevent Twilio retries.

---

## 10. REST API Reference

### 10.1 Authentication

| Method | Path | Body | Returns |
|---|---|---|---|
| `POST` | `/api/register` | `{name, phone, zip_code, role, password}` | `{message, user}` |
| `POST` | `/api/login` | `{phone, password, role}` | `{message, user}` |

### 10.2 Listings

| Method | Path | Query/Body | Returns |
|---|---|---|---|
| `GET` | `/api/listings` | `?crop=&zip_code=&seller_type=&buyer_type=` | `[Listing]` |
| `POST` | `/api/listings` | `{farmer_phone, crop_name, quantity_kg, price_per_kg, min_order_kg, bulk_price_per_kg, zip_code, location_name, quality_grade, shelf_life_days}` | `{message, listing}` |
| `PUT` | `/api/listings/{id}` | `{farmer_phone, [fields to update]}` | `{message, listing}` |
| `DELETE` | `/api/listings/{id}?farmer_phone=` | — | `{message}` |

### 10.3 Orders

| Method | Path | Query/Body | Returns |
|---|---|---|---|
| `POST` | `/api/order` | `{listing_id, buyer_phone, quantity_kg, delivery_address, delivery_lat, delivery_lon, notes}` | `{status, message, order}` |
| `GET` | `/api/farmer/orders?farmer_phone=` | — | `[Order]` |
| `GET` | `/api/buyer/orders?buyer_phone=` | — | `[Order]` |
| `POST` | `/api/orders/{id}/accept?farmer_phone=` | — | `{message, order, remaining_kg}` |
| `POST` | `/api/orders/{id}/reject?farmer_phone=` | — | `{message, order}` |
| `POST` | `/api/orders/{id}/cancel?buyer_phone=` | — | `{message, order}` |

### 10.4 Chat

| Method | Path | Query/Body | Returns |
|---|---|---|---|
| `GET` | `/api/listings/{id}/messages?phone=&partner_phone=` | — | `[Message]` |
| `GET` | `/api/listings/{id}/conversations?farmer_phone=` | — | `[{buyer_phone, buyer_name, last_message, last_ts, msg_count}]` |
| `GET` | `/api/farmer/inbox_counts?farmer_phone=` | — | `{listing_id: count}` |
| `POST` | `/api/listings/{id}/messages` | `{from_phone, to_phone, body}` | `{message, msg}` |

### 10.5 AI Demand Forecasting

| Method | Path | Query | Returns |
|---|---|---|---|
| `GET` | `/api/ai/demand-forecast?crop=TOMATO&days=7` | — | Forecast JSON (see below) |

**Response shape:**
```json
{
  "crop": "TOMATO",
  "forecast_days": 7,
  "forecast_daily_kg": 52.3,
  "forecast_total_kg": 366.1,
  "current_supply_kg": 450.0,
  "recommended_stock_kg": 421.0,
  "supply_gap_kg": -29.0,
  "trend": "rising",
  "confidence_percent": 78.5,
  "method": "Recency-Weighted Linear Trend + Seasonal Prior",
  "history_days": 4,
  "fair_farmer_price_inr": 26.1,
  "fair_consumer_price_inr": 31.5,
  "mandi_benchmark_inr": 18.0,
  "retail_benchmark_inr": 42.0,
  "shelf_life_days": 6,
  "spoilage_risk": "HIGH",
  "recommendation": "Market is balanced. Target harvesting 421 KG...",
  "daily_projection": [
    {"day": "Fri 29 Aug", "demand_kg": 51.2},
    ...
  ]
}
```

### 10.6 Logistics

| Method | Path | Body | Returns |
|---|---|---|---|
| `POST` | `/api/logistics/optimize` | `{origin_name, origin_lat, origin_lon, stops: [{name, lat, lon, quantity_kg, address, phone, order_id}], vehicle_capacity_kg}` | Route optimization JSON |
| `POST` | `/api/logistics/dispatch` | `{farmer_phone, origin_*, vehicle_*, driver_*, stops, order_ids, metrics}` | `{message, trip}` |
| `GET` | `/api/logistics/trips?phone=` | — | `[Trip]` |
| `POST` | `/api/logistics/trips/{id}/deliver?phone=` | — | `{message, trip}` |

### 10.7 Analytics

| Method | Path | Query | Returns |
|---|---|---|---|
| `GET` | `/api/analytics/value-distribution?crop=TOMATO` | — | Value distribution JSON |

### 10.8 SMS Webhook

| Method | Path | Form Data | Returns |
|---|---|---|---|
| `POST` | `/sms/webhook` | `From=+91...&Body=SELL TOMATO 50KG 28/KG 500001` | TwiML XML |

### 10.9 Frontend

| Method | Path | Returns |
|---|---|---|
| `GET` | `/` | Full HTML SPA (string from `frontend.FRONTEND_HTML`) |

---

## 11. Frontend Architecture (SPA)

### 11.1 Design System

- **Color Palette:**
  - Primary Green: `#155e38` (deep forest), `#2d8a56` (light accent)
  - Accent Amber: `#d97706` (savings/callouts)
  - Earth: `#854d0e`
  - Warm Background: `#fbfbfa`
  - Text: `#1e293b` (slate-800), `#64748b` (slate-500 muted)

- **Typography:**
  - Headings: `Outfit` (geometric, modern)
  - Body: `Plus Jakarta Sans` (warm, humanist)

- **Visual Motifs:**
  - Rounded corners (`--radius-md: 16px`, `--radius-lg: 24px`)
  - Subtle shadows (`0 8px 24px -4px rgba(21, 94, 56, 0.08)`)
  - Glassmorphism navbar (`backdrop-filter: blur(12px)`)
  - Gradient hero (`linear-gradient(145deg, #155e38 0%, ...)`)

### 11.2 Component Library

- **Bootstrap 5.3.2** for grid, modals, dropdowns, forms
- **Bootstrap Icons 1.11.3** for all iconography
- **Custom card components** (`crop-card`, `metric-card`, `route-stop-card`)
- **Custom chat bubbles** (self vs other styling)
- **Bootstrap-styled badges** for status indicators

### 11.3 State Management

```javascript
// Persisted across sessions
localStorage.cc_lang   // "en" | "hi" | "te" | "ta"
localStorage.cc_user   // JSON.stringify({name, phone, zip_code, role})

// In-memory (lost on refresh)
currentLang
currentUser
currentActiveTab
activeChatListing
activeChatPartnerPhone
window._lastListings    // cache for re-rendering on language change
window._lastOrders      // cache for re-rendering on language change
```

### 11.4 Polling Architecture

- **Sync Poll (4s):** Refreshes listings and orders when those tabs are active.
- **Chat Poll (2.5s):** Refreshes chat messages when chat modal is open.
- Both timers are cleared on logout to prevent background network activity.

### 11.5 Tab Structure

| Tab ID | View Element | Data Source | Key Endpoints |
|---|---|---|---|
| `marketplace` | `#view-marketplace` | `window._lastListings` | `GET /api/listings` |
| `orders` | `#view-orders` | `window._lastOrders` | `GET /api/farmer/orders` or `/api/buyer/orders` |
| `ai` | `#view-ai` | Inline (rendered on demand) | `GET /api/ai/demand-forecast` |
| `logistics` | `#view-logistics` | Inline + `lastOptimizedData` | `POST /api/logistics/optimize`, `dispatch`, `trips` |
| `analytics` | `#view-analytics` | Inline | `GET /api/analytics/value-distribution` |

---

## 12. Twilio SMS Inbound Webhook

### 12.1 Supported Commands

| Command | Example | Response |
|---|---|---|
| `PRICE <CROP>` | `PRICE TOMATO` | AI fair price + mandi + retail benchmark |
| `SELL <CROP> <QTY>KG <PRICE>/KG [ZIP]` | `SELL CABBAGE 80KG 20/KG 500001` | Listing confirmation with quantity & price |
| `ORDERS` | `ORDERS` | Count + summary of pending orders |
| Other | `hello` | Format help message |

### 12.2 SMS Regex Pattern

```python
pattern = r'^SELL\s+([A-Za-z\s]+?)\s+(\d+(?:\.\d+)?)\s*KG\s+(\d+(?:\.\d+)?)(?:/KG)?(?:\s+(\d{5,6}))?$'
```

Matches:
- `SELL` keyword
- Crop name (letters/spaces, non-greedy)
- Quantity (integer or decimal) followed by `KG`
- Price (integer or decimal) optionally followed by `/KG`
- Optional 5-6 digit ZIP code

### 12.3 TwiML Response Format

All responses are XML:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Your response text here</Message>
</Response>
```

The backend sets `media_type="text/xml"` so Twilio parses it correctly.

### 12.4 SMS-Listed Listing Properties

When a listing is created via SMS, it inherits:
- `source: "SMS"` (shown in UI as "⚡ SMS Listed")
- `location_name: "Farm SMS ({zip})"`
- `lat: 17.3850, lon: 78.4867` (default Hyderabad center)
- `quality_grade: "Grade A Fresh"`
- `shelf_life_days: 7`
- `mandi_price_per_kg: price * 0.70`
- `bulk_price_per_kg: price * 0.90`

---

## 13. Multilingual Localization (i18n)

### 13.1 Supported Languages

| Code | Language | Script |
|---|---|---|
| `en` | English | Latin |
| `hi` | हिन्दी (Hindi) | Devanagari |
| `te` | తెలుగు (Telugu) | Telugu |
| `ta` | தமிழ் (Tamil) | Tamil |

### 13.2 Implementation Strategy

1. **Translation Table:** A nested JavaScript object `I18N[lang][key]`.
2. **Markup Annotation:** Elements that need translation carry `data-i18n="key"` (or `data-i18n-attr="placeholder"` for attribute values).
3. **Application:** `applyTranslations()` iterates `[data-i18n]` elements and replaces text/attribute from the dictionary.
4. **Fallback:** If a key is missing in the current language, falls back to English, then to the key itself.
5. **Persistence:** `localStorage.setItem("cc_lang", lang)` preserves choice across sessions.
6. **Dynamic Re-render:** When language changes, the listings and orders tables are re-rendered from cached data so that dynamically-injected strings get translated too.

### 13.3 Example Translation Entry

```javascript
I18N.en.kg_left = "KG Left";
I18N.hi.kg_left = "किलो शेष";
I18N.te.kg_left = "కేజీ మిగిలి ఉంది";
I18N.ta.kg_left = "கிலோ உள்ளது";
```

All currency strings are prefixed with ₹ (Indian Rupee symbol) consistently across languages.

---

## 14. Authentication & Role-Based Access

### 14.1 Password Hashing

```python
import hashlib

def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()
```

- SHA-256 hex digest (64 characters).
- No salt (demo simplicity; production should use bcrypt or argon2).

### 14.2 Role Constants

```python
SELLER_ROLES = {"FARMER", "FPO"}
BUYER_ROLES = {"BUYER", "BULK_BUYER", "CONSUMER"}

def is_seller(role): return str(role).strip().upper() in SELLER_ROLES
def is_buyer(role):  return str(role).strip().upper() in BUYER_ROLES
```

### 14.3 Authorization Pattern

```python
def require_seller(phone: str) -> dict:
    user = require_user(phone)  # Raises 403 if not found
    if not is_seller(user.get("role", "")):
        raise HTTPException(status_code=403, detail="This action is reserved for Farmers and FPOs only.")
    return user
```

Every mutating endpoint that needs auth calls `require_seller()` or `require_buyer()` first.

### 14.4 Session Management

- **No server-side sessions** — all auth state is client-side (`localStorage.cc_user`).
- **No JWT tokens** — phone + password are sent with every privileged request (acceptable for demo; production should add JWT).
- **Phone number is the de-facto session key** — relies on `phones_match()` for lenient comparison.

---

## 15. Deployment & DevOps

### 15.1 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start dev server
uvicorn main:app --reload --port 8000

# Or run directly
python main.py

# Run tests
python test_app.py
```

### 15.2 Railway Deployment

**Configuration Files:**

- **`Procfile`:** `web: python main.py`
- **`runtime.txt`:** `python-3.12.7`
- **`railway.json`:** Nixpacks builder, restart on failure (max 10 retries)
- **`Dockerfile`:** Python 3.12-slim, exposes port 8000

**Environment Variables:**
- `PORT` — Railway-injected; backend reads it via `os.environ.get("PORT", 8000)`

### 15.3 Docker Build

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["python", "main.py"]
```

The image is ~150 MB (slim base + minimal Python deps).

### 15.4 Git History

```
8523839 Enhance UI design to warm human-crafted style with Rupee (INR ₹) currency throughout
2e23ee6 Fix PORT parsing by launching via python main.py
55657b8 Configure Railway deployment with Dockerfile, Procfile, and requirements
e131ea7 update
98ee78e adding required features
24c1567 Add smart marketplace features: direct farmer-to-buyer flow, logistics optimization, and AI demand forecasting
9e162d5 Update requirements.txt
19bacd4 Add Railway deploy config
ab21743 Initial commit
```

---

## 16. Automated Test Suite

`test_app.py` uses FastAPI's `TestClient` to execute 6 end-to-end tests:

| # | Test | Endpoint | Validation |
|---|---|---|---|
| 1 | Frontend served | `GET /` | Status 200, "CropConnect" in HTML |
| 2 | Listings retrieved | `GET /api/listings` | Status 200, length > 0 |
| 3 | AI demand forecast | `GET /api/ai/demand-forecast?crop=TOMATO&days=7` | Returns 7-day projection, fair prices |
| 4 | Value distribution | `GET /api/analytics/value-distribution?crop=TOMATO` | Both chains present, percentages computed |
| 5 | Logistics optimizer | `POST /api/logistics/optimize` | 3 stops optimized, distance > 0, vehicle recommended |
| 6 | SMS webhook | `POST /sms/webhook` (PRICE + SELL) | Valid TwiML response for both commands |

**Run:**
```bash
python test_app.py
```

**Output:**
```
==========================================
ALL TEST SUITES PASSED SUCCESSFULLY (6/6)!
==========================================
```

---

## 17. Demo Login Accounts

| Role | Phone Number | Password | Name |
|---|---|---|---|
| **Farmer** | `+919876543210` | `password123` | Ramesh Kumar |
| **FPO Collective** | `+919876543220` | `password123` | Telangana Kisan FPO (Aggregator) |
| **Bulk Buyer** | `+919876543211` | `password123` | Suresh Wholesale & Retail Hub |
| **Consumer** | `+919876543230` | `password123` | Priya Sharma |

Additional accounts are auto-seeded (e.g., `+1234567890` for US testing).

---

## 18. Notable Technical Details

### 18.1 Pydantic Schema Validation

All request bodies are validated by Pydantic before the handler runs. This catches:
- Type mismatches (e.g., `quantity_kg` must be float)
- Missing required fields
- Invalid enum values (for role-based enums if added)

### 18.2 CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Wide-open CORS is intentional for demo purposes; production should restrict origins.

### 18.3 Auto-Migration on Read

Every `load_*()` function handles schema migration:
- If file doesn't exist → seed.
- If file is empty → seed.
- If records are missing new fields → backfill with defaults and rewrite.

This means the codebase can be updated to add new listing fields (e.g., `organic_certified`) without breaking existing user data.

### 18.4 XSS Protection in Frontend

The `esc()` function escapes HTML entities before injection:
```javascript
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
```

All user-generated content (crop names, messages, addresses) is passed through this function before rendering.

### 18.5 Auto-Generated System Messages

Whenever a state transition occurs (order placed, accepted, dispatched, delivered), a message is auto-appended to `MESSAGES_DB` so the buyer/seller sees it in their chat history:

```python
auto_msg = {
    "id": msg_id,
    "listing_id": listing["id"],
    "from_phone": buyer["phone"],
    "to_phone": listing["farmer_phone"],
    "body": f"📦 New Order #{new_order_id}...",
    "ts": now_iso
}
```

This creates a "transaction-as-chat" UX.

### 18.6 Demand Forecast Sinusoidal Noise

```python
for i in range(1, days + 1):
    noise = math.sin(i * 0.8) * (forecast_daily_kg * 0.08)
    proj_val = max(1.0, round(forecast_daily_kg + noise, 1))
```

Adds ±8% sinusoidal variation to the daily projection for visual realism in the bar chart.

### 18.7 Idempotent Trip Delivery

Marking a trip as delivered is idempotent (re-running it just keeps the same `DELIVERED` status). All included orders are also updated atomically.

### 18.8 Smart Polling Lifecycle

- `startSyncPolling()` is called on successful login.
- `stopSyncPolling()` is called on logout.
- `startChatPolling()` is called when chat modal opens.
- `stopChatPolling()` is called when chat modal closes.

This prevents unnecessary network traffic.

### 18.9 Crop-Specific Seasonal & Elasticity Priors

The `CROP_BENCHMARKS` dictionary encodes domain knowledge:

| Crop | base_daily_kg | shelf_life | elasticity | season_factor |
|---|---|---|---|---|
| TOMATO | 45 | 6 (HIGH spoilage) | 1.25 (very elastic) | 1.15 |
| RED ONION | 65 | 25 (LOW spoilage) | 0.85 (inelastic) | 1.05 |
| POTATO | 80 | 30 | 0.70 | 1.00 |
| CHILLI | 25 | 14 | 1.10 | 1.20 |
| BANANA | 40 | 5 (HIGH spoilage) | 1.15 | 1.10 |
| MANGO | 50 | 7 | 1.40 (very elastic) | 1.35 |
| RICE | 120 | 180 | 0.60 (very inelastic) | 1.00 |
| WHEAT | 100 | 180 | 0.65 | 1.00 |

- **Elasticity > 1:** Price-sensitive; small price changes cause larger demand swings.
- **Elasticity < 1:** Price-inelastic; staple crops.
- **season_factor > 1:** Seasonal uptick in demand.
- **shelf_life ≤ 6:** `spoilage_risk = "HIGH"` (must move fast).

### 18.10 Demo Optimization Trigger

A special seed record (in the original `main.py.bak`) and code patterns show the system was prototyped for the **Smart India Hackathon (SIH)** — a competition for solving Indian governance/industry problems with technology.

---

## Appendix A: Quick Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/saiganeshakula93-debug/cropconnect123.git
cd cropconnect123

# 2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python main.py
# or: uvicorn main:app --reload --port 8000

# 5. Open the app
# Browser: http://127.0.0.1:8000

# 6. Login with a demo account
# Farmer:    +919876543210 / password123
# Consumer:  +919876543230 / password123
```

## Appendix B: Project Structure

```
cropconnect/
├── main.py                          # FastAPI backend (~1,567 lines)
├── frontend.py                      # Embedded HTML/CSS/JS SPA (~2,500 lines)
├── test_app.py                      # End-to-end tests (~74 lines)
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker image definition
├── Procfile                         # Railway process file
├── railway.json                     # Railway deployment config
├── runtime.txt                      # Python version pin
├── .gitignore                       # Git ignore rules
├── README_SMART_FEATURES.md         # Feature overview
├── PROJECT_DOCUMENTATION.md         # This document
├── users.json                       # User database (seeded)
├── listings.json                    # Crop listings (seeded)
├── orders.json                      # Orders (seeded)
├── messages.json                    # Chat history (seeded)
└── SIH/                             # Smart India Hackathon materials
```

---

**End of Documentation**

*This document was generated on 2026-08-28 by analyzing the CropConnect codebase at `C:/Users/Dell/cropconnect/cropconnect`.*
