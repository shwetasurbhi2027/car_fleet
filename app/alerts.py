import uuid
from datetime import datetime
from .database import alerts

SPEED_LIMIT = 120  # km/h
LOW_FUEL_THRESHOLD = 15.0  # percentage

def check_alerts(telemetry):
    generated = []
    if telemetry.speed > SPEED_LIMIT:
        alert = create_alert(telemetry.vin, "Speed Violation", "High",
                             f"Speed {telemetry.speed:.1f} km/h exceeds limit", telemetry.timestamp)
        generated.append(alert)
    if telemetry.fuel_level < LOW_FUEL_THRESHOLD:
        alert = create_alert(telemetry.vin, "Low Fuel/Battery", "Medium",
                             f"Fuel/Battery low: {telemetry.fuel_level:.1f}%", telemetry.timestamp)
        generated.append(alert)
    return generated

def create_alert(vin, alert_type, severity, description, timestamp=None):
    alert_id = str(uuid.uuid4())
    alert = {
        "alert_id": alert_id,
        "vin": vin,
        "alert_type": alert_type,
        "severity": severity,
        "description": description,
        "timestamp": timestamp or datetime.utcnow(),
    }
    alerts[alert_id] = alert
    return alert

