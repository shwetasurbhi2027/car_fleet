from fastapi import FastAPI, HTTPException
from datetime import datetime
from app import models, database, schemas, alerts, analytics

app = FastAPI(
    title="Connected Car Fleet Management API",
    description="Manage vehicles, telemetry, and alerts",
    version="1.0"
)

# VEHICLE MANAGEMENT

@app.post("/vehicles", response_model=schemas.VehicleCreate)
def create_vehicle(vehicle: schemas.VehicleCreate):
    if vehicle.vin in database.vehicles:
        raise HTTPException(status_code=400, detail="VIN already exists")
    v = models.Vehicle(**vehicle.dict())
    database.vehicles[vehicle.vin] = v
    return vehicle

@app.get("/vehicles", response_model=list[schemas.VehicleCreate])
def list_vehicles():
    return [schemas.VehicleCreate(**vars(v)) for v in database.vehicles.values()]

@app.get("/vehicles/{vin}", response_model=schemas.VehicleCreate)
def get_vehicle(vin: str):
    v = database.vehicles.get(vin)
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return schemas.VehicleCreate(**vars(v))

@app.delete("/vehicles/{vin}", status_code=204)
def delete_vehicle(vin: str):
    if vin not in database.vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    del database.vehicles[vin]
    if vin in database.telemetry_data:
        del database.telemetry_data[vin]
    return

# TELEMETRY DATA

@app.post("/telemetry", status_code=201)
def post_telemetry(telemetry: schemas.TelemetryIn):
    if telemetry.vin not in database.vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    t = models.Telemetry(**telemetry.dict())
    database.telemetry_data[t.vin].append(t)
    # Alert detection
    generated_alerts = alerts.check_alerts(t)
    return {"msg": "Telemetry data added", "alerts_generated": [a["alert_id"] for a in generated_alerts]}

@app.get("/telemetry/{vin}", response_model=list[schemas.TelemetryIn])
def get_telemetry(vin: str):
    if vin not in database.vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return [vars(t) for t in database.telemetry_data[vin]]

@app.get("/telemetry/{vin}/latest", response_model=schemas.TelemetryIn)
def get_latest_telemetry(vin: str):
    if vin not in database.vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    telemetry = database.telemetry_data[vin]
    if not telemetry:
        raise HTTPException(status_code=404, detail="No telemetry data")
    latest = max(telemetry, key=lambda x: x.timestamp)
    return vars(latest)

# ALERTS

@app.get("/alerts")
def all_alerts():
    return list(database.alerts.values())

@app.get("/alerts/{alert_id}", response_model=schemas.AlertOut)
def get_alert(alert_id: str):
    alert = database.alerts.get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

# ANALYTICS

@app.get("/analytics")
def fleet_analytics():
    return analytics.get_fleet_analytics()

