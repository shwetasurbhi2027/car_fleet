
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class VehicleCreate(BaseModel):
    vin: str
    manufacturer: str
    model: str
    fleet_id: str
    owner: str
    registration_status: str

class TelemetryIn(BaseModel):
    vin: str
    latitude: float
    longitude: float
    speed: float
    engine_status: str
    fuel_level: float
    odometer: float
    diagnostic_codes: Optional[List[str]] = []
    timestamp: datetime

class AlertOut(BaseModel):
    alert_id: str
    vin: str
    alert_type: str
    severity: str
    description: str
    timestamp: datetime
