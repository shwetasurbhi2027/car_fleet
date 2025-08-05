# Connected Car Fleet Management System

This application manages vehicle fleets, processes real-time telemetry, and provides basic analytics/alerts.

## Main Features
- Vehicle CRUD
- Telemetry upload and querying
- Alerts on speed violations/low fuel
- Fleet-level analytics

## API docs: 
Launch server and visit http://localhost:8000/docs

## Requirements
- Python 3.9+
- FastAPI, Uvicorn

## Run
pip install -r requirements.txt
uvicorn app.main:app --reload

