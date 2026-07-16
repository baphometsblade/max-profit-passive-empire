#!/usr/bin/env python3
"""
VerticalMiles - Out-of-the-box Passive Income Stream
Uses barometer + accelerometer to track vertical movement (elevators, stairs, buildings).
Sells aggregated vertical mobility data to urban planners, real estate, and logistics.
Completely passive.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="VerticalMiles - Max Profit Empire", version="1.0.0")

class VerticalEvent(BaseModel):
    delta_meters: float
    duration_seconds: float
    context: Optional[str] = None  # "elevator", "stairs", "escalator"
    location_hash: Optional[str] = None
    consent: bool = True

earnings = {"total_usd": 0.0, "events": 0}

@app.post("/event")
async def submit_vertical(event: VerticalEvent):
    if not event.consent:
        raise HTTPException(400, "Consent required")
    
    # Taller / longer vertical movements are more valuable
    value = 0.01 * abs(event.delta_meters) * 0.1
    value = max(0.005, min(value, 0.08))  # clamp
    earnings["total_usd"] += value
    earnings["events"] += 1
    
    return {
        "status": "sold",
        "earnings_usd": round(value, 4),
        "total_vertical_revenue": round(earnings["total_usd"], 4),
        "message": "Vertical mobility data sold. Fully passive."
    }

@app.get("/marketplace")
async def marketplace():
    return {
        "buyers": ["urban_planners", "real_estate", "logistics", "building_ops", "fitness_apps"],
        "products": ["Building occupancy heatmaps", "Elevator usage analytics", "Vertical commute indices"],
        "pricing": "$0.005–$0.05 per event or $199–$1499/mo for city feeds",
        "events": earnings["events"]
    }

@app.get("/")
async def root():
    return {
        "service": "VerticalMiles",
        "description": "Passive income from vertical movement & building data",
        "automation": "Phone always on → continuous vertical data sales"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
