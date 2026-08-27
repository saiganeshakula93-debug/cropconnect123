import main
from fastapi.testclient import TestClient

client = TestClient(main.app)

def run_tests():
    print("--- 1. Testing Frontend ---")
    res = client.get("/")
    assert res.status_code == 200
    assert "CropConnect" in res.text
    print("[PASS] Frontend served correctly")

    print("\n--- 2. Testing Listings ---")
    res = client.get("/api/listings")
    assert res.status_code == 200
    listings = res.json()
    assert len(listings) > 0
    print(f"[PASS] Listings retrieved: {len(listings)} active items")

    print("\n--- 3. Testing AI Demand Forecasting ---")
    res = client.get("/api/ai/demand-forecast?crop=TOMATO&days=7")
    assert res.status_code == 200
    f = res.json()
    assert f["crop"] == "TOMATO"
    assert "forecast_total_kg" in f
    assert "fair_farmer_price_inr" in f
    assert len(f["daily_projection"]) == 7
    print(f"[PASS] AI Demand Forecast for {f['crop']}: {f['forecast_total_kg']} KG / 7 days, Recommended Rate: Rs {f['fair_farmer_price_inr']}/kg")

    print("\n--- 4. Testing Supply Chain Value Distribution ---")
    res = client.get("/api/analytics/value-distribution?crop=TOMATO")
    assert res.status_code == 200
    v = res.json()
    assert "traditional_chain" in v and "cropconnect_direct_chain" in v
    print(f"[PASS] Value Distribution: Farmer gain +{v['benefits']['farmer_income_increase_percent']}%, Consumer save -{v['benefits']['consumer_price_savings_percent']}%")

    print("\n--- 5. Testing Logistics Route Optimizer ---")
    payload = {
        "origin_name": "Shamshabad Agri Hub",
        "origin_lat": 17.2500,
        "origin_lon": 78.4200,
        "vehicle_capacity_kg": 800,
        "stops": [
            {"name": "Wholesale Mart Begumpet", "lat": 17.4435, "lon": 78.4738, "quantity_kg": 150, "address": "Secunderabad"},
            {"name": "Green Valley Banjara Hills", "lat": 17.4156, "lon": 78.4350, "quantity_kg": 25, "address": "Road 12"},
            {"name": "Kukatpally Supermarket", "lat": 17.4933, "lon": 78.3995, "quantity_kg": 200, "address": "Main Road"}
        ]
    }
    res = client.post("/api/logistics/optimize", json=payload)
    assert res.status_code == 200
    r = res.json()
    assert len(r["route"]) == 3
    assert r["total_distance_km"] > 0
    assert "recommended_vehicle" in r
    print(f"[PASS] Route 2-Opt Optimizer: Total Distance = {r['total_distance_km']} km, Time = {r['estimated_travel_minutes']} mins, Vehicle = {r['recommended_vehicle']}")

    print("\n--- 6. Testing Twilio SMS Webhook ---")
    res = client.post("/sms/webhook", data={"From": "+919876543210", "Body": "PRICE TOMATO"})
    assert res.status_code == 200
    assert "AI Price Advisor" in res.text
    print("[PASS] SMS Price Advisor Inquiry Verified")

    res = client.post("/sms/webhook", data={"From": "+919876543210", "Body": "SELL CABBAGE 80KG 20/KG 500001"})
    assert res.status_code == 200
    assert "Successfully listed" in res.text
    print("[PASS] SMS Listing Command Verified")

    print("\n==========================================")
    print("ALL TEST SUITES PASSED SUCCESSFULLY (6/6)!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
