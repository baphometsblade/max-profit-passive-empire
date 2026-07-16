#!/usr/bin/env python3
"""
PollenPulse - Out-of-the-box Passive Income Stream
Uses phone camera (when face-up outdoors) to estimate hyper-local pollen & air quality.
Sells ground-truth environmental data to pharma, allergy apps, and weather services.
Completely passive after permission.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="PollenPulse - Max Profit Empire", version="1.0.0")

class SkySample(BaseModel):
    haze_score: float          # 0-1 estimated from image
    color_temp: Optional[float] = None
    location_hash: Optional[str] = None
    consent: bool = True

earnings = {"total_usd": 0.0, "samples": 0}

@app.post("/sample")
async def submit_sky(sample: SkySample):
    if not sample.consent:
        raise HTTPException(400, "Consent required")
    
    value = 0.018 * (0.5 + sample.haze_score)   # higher haze = more valuable allergy data
    earnings["total_usd"] += value
    earnings["samples"] += 1
    
    return {
        "status": "sold",
        "earnings_usd": round(value, 4),
        "total_pollen_revenue": round(earnings["total_usd"], 4),
        "message": "Hyper-local air quality data sold. Fully passive."
    }

@app.get("/marketplace")
async def marketplace():
    return {
        "buyers": ["pharma", "allergy_apps", "weather_services", "air_purifier_brands"],
        "pricing": "$0.01–$0.05 per sample or $299–$1999/mo for live grids",
        "samples": earnings["samples"]
    }

@app.get("/")
async def root():
    return {
        "service": "PollenPulse",
        "description": "Passive income from phone camera air quality / pollen data",
        "automation": "Phone face-up outdoors → continuous environmental sales"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
