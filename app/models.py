from datetime import datetime
from typing import List, Optional

class Vehicle:
    def __init__(self, vin, manufacturer, model, fleet_id, owner, registration_status):
        self.vin = vin
        self.manufacturer = manufacturer
        self.model = model
        self.fleet_id = fleet_id
        self.owner = owner
        self.registration_status = registration_status
        self.created_at = datetime.utcnow()

class Telemetry:
    def __init__(self, vin, latitude, longitude, speed, engine_status,
                 fuel_level, odometer, diagnostic_codes, timestamp):
        self.vin = vin
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.engine_status = engine_status
        self.fuel_level = fuel_level
        self.odometer = odometer
        self.diagnostic_codes = diagnostic_codes or []
        self.timestamp = timestamp

class Alert:
    def __init__(self, alert_id, vin, alert_type, severity, description, timestamp):
        self.alert_id = alert_id
        self.vin = vin
        self.alert_type = alert_type
        self.severity = severity
        self.description = description
        self.timestamp = timestamp

