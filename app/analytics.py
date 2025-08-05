from datetime import datetime, timedelta

from .database import vehicles, telemetry_data, alerts

def get_fleet_analytics():
    now = datetime.utcnow()
    one_day_ago = now - timedelta(hours=24)

    # Active = received telemetry in 24h; Inactive otherwise
    active, inactive = 0, 0
    avg_fuel = 0.0
    fuel_count = 0
    distance_24h = 0.0

    for v in vehicles.values():
        telemetries = [t for t in telemetry_data[v.vin] if t.timestamp >= one_day_ago]
        if telemetries:
            active += 1
            avg_fuel += sum(t.fuel_level for t in telemetries)
            fuel_count += len(telemetries)
            # Calculate distance
            distances = sorted(telemetries, key=lambda x: x.timestamp)
            if distances:
                distance_24h += distances[-1].odometer - distances[0].odometer
        else:
            inactive += 1

    avg_fuel = avg_fuel / fuel_count if fuel_count > 0 else 0

    # Alert summary
    alert_summary = {}
    for a in alerts.values():
        key = (a["alert_type"], a["severity"])
        alert_summary[key] = alert_summary.get(key, 0) + 1

    summary_results = [{"type": k[0], "severity": k[1], "count": v} for k, v in alert_summary.items()]
    return {
        "active": active,
        "inactive": inactive,
        "avg_fuel": avg_fuel,
        "distance_24h": distance_24h,
        "alert_summary": summary_results,
    }

