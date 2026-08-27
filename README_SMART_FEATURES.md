# CropConnect - Direct Agri Marketplace & Smart Logistics

CropConnect is a unified digital agricultural marketplace that connects **Farmers and FPOs** directly with **Consumers and Bulk Buyers**, backed by **AI Demand Forecasting** and **Smart Logistics 2-Opt Route Optimization**.

---

## 🌟 Key Features & Expected Solution Capabilities

### 1. Direct Digital Marketplace
- **4 Distinct User Roles**:
  - `FARMER` (Individual Smallholders)
  - `FPO` (Farmer Producer Organizations & Collectives)
  - `BULK_BUYER` (Wholesalers, Supermarkets, Restaurants)
  - `CONSUMER` (Direct Household & Retail Buyers)
- **Minimum Order Quantity (MOQ)** & **Bulk Discount Pricing** tiers.
- **Fair Price Transparency**: Real-time comparison between Mandi distress rates, CropConnect direct rates, and Supermarket retail prices.
- **Twilio SMS Inbound Webhook**:
  - List crops via SMS: `SELL TOMATO 50KG 28/KG 500001`
  - Check fair price & AI forecast: `PRICE TOMATO`
  - Query active orders: `ORDERS`
- **Direct Per-Listing Chat**: Real-time buyer-seller negotiation.

### 2. AI-Assisted Multi-Factor Demand Forecasting
- **API**: `GET /api/ai/demand-forecast?crop=TOMATO&days=7`
- Combines recency-weighted linear trend regression with crop-specific seasonal elasticity priors and shelf-life indices.
- Outputs:
  - 7, 14, and 30-day projected demand volume (KG)
  - Dynamic trajectory projection curve (visual SVG chart)
  - Marketplace supply deficit/surplus gap analysis
  - Dynamic **AI Fair Price Advisor** for optimal farmer realization and consumer savings
  - Spoilage risk advisory for perishables

### 3. Smart Logistics & 2-Opt Multi-Stop Route Optimization
- **API**: `POST /api/logistics/optimize`
- **API**: `POST /api/logistics/dispatch`
- **1-Click Auto-Import**: Load all accepted customer orders directly into the delivery route optimizer.
- **2-Opt Trajectory Optimization**: Solves the multi-drop TSP to minimize road distance and transit time.
- **Intelligent Vehicle Sizing**:
  - Electric Cargo 3-Wheeler (< 80 kg)
  - Light Pickup / Mini Truck (80 - 400 kg)
  - Medium Commercial Vehicle (400 - 1200 kg)
  - Heavy Reefer Carrier (> 1200 kg)
- **Cost & Carbon Reduction**: Calculates estimated fuel savings and CO2 emissions reduction.
- **Trip Dispatch & Manifest**: Assigns driver, tracking number, and transitions orders to `DISPATCHED` -> `DELIVERED`.

### 4. Supply Chain Transparency & Value Distribution
- **API**: `GET /api/analytics/value-distribution?crop=TOMATO`
- Side-by-side comparison of the **Traditional Multi-Tier Mandi Chain** vs **CropConnect Direct Marketplace**.
- Quantifies:
  - **+45% to +50%** higher income for farmers
  - **25% to 30%** price discount for consumers
  - **Zero** middleman commission loss
  - **< 4.5%** post-harvest food waste (down from ~25%)

### 5. Multilingual Localization (4 Languages)
- Full UI and messaging support in:
  - 🇬🇧 **English (EN)**
  - 🇮🇳 **हिन्दी (Hindi)**
  - 🇮🇳 **తెలుగు (Telugu)**
  - 🇮🇳 **தமிழ் (Tamil)**

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Open in Browser
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## 👥 Demo Login Accounts

| Role | Phone Number | Password |
| :--- | :--- | :--- |
| **Farmer** | `+919876543210` | `password123` |
| **FPO Collective** | `+919876543220` | `password123` |
| **Bulk Buyer** | `+919876543211` | `password123` |
| **Consumer** | `+919876543230` | `password123` |

---

## 🧪 Automated Testing
Run the comprehensive test suite:
```bash
python test_app.py
```
