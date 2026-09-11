# CropConnect - Smart Marketplace

This version adds the requested solution features:

1. Direct digital marketplace
   - Farmers/FPOs can list crops.
   - Buyers can search listings and place batch orders.
   - Existing chat and order workflow is preserved.

2. Logistics support
   - New API: `POST /api/logistics/optimize`
   - Plans a delivery sequence using nearest-neighbour distance optimization.
   - Calculates total distance, estimated travel time, load utilization and suggested vehicle type.
   - The UI is available after login under **Smart Market & Logistics**.

3. AI-assisted demand forecasting
   - New API: `GET /api/ai/demand-forecast?crop=TOMATO&days=7`
   - Uses existing order history plus current marketplace supply.
   - Applies a recency-weighted linear trend model.
   - Returns forecast quantity, trend, confidence, supply gap and a stocking recommendation.
   - The UI is available after login under **Smart Market & Logistics**.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:

`http://127.0.0.1:8000`

### Route optimizer input

Enter one delivery stop per line:

`Buyer A, 17.4065, 78.4772, 100`

Format:

`Name, Latitude, Longitude, QuantityKG`

Note: the route optimizer uses geographic distance and an estimated speed. It does not provide live traffic or turn-by-turn road routing.
