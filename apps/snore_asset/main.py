#!/usr/bin/env python3
"""
SnoreAsset - Out-of-the-box Passive Income Stream
Records and isolates unique snore patterns overnight.
Mints them as collectible sleep audio / ASMR assets or sells to sleep research.
Completely passive after bedtime permission.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import hashlib

app = FastAPI(title="SnoreAsset - Max Profit Empire", version="1.0.0")

class SnoreClip(BaseModel):
    duration_seconds: float
    frequency_profile: Optional[dict] = None
    consent: bool = True

earnings = {"total_usd": 0.0, "clips": 0}

@app.post("/clip")
async def submit_snore(clip: SnoreClip):
    if not clip.consent:
        raise HTTPException(400, "Consent required")
    
    # Unique snore patterns have collector + research value
    value = 0.03 + (0.01 * min(clip.duration_seconds / 30, 5))
    earnings["total_usd"] += value
    earnings["clips"] += 1
    
    clip_id = hashlib.sha256(f"{clip.duration_seconds}{datetime.utcnow()}".encode()).hexdigest()[:12]
    
    return {
        "status": "minted_and_sold",
        "clip_id": clip_id,
        "earnings_usd": round(value, 4),
        "total_snore_revenue": round(earnings["total_usd"], 4),
        "message": "Unique snore asset created & sold. Fully passive overnight."
    }

@app.get("/marketplace")
async def marketplace():
    return {
        "buyers": ["ASMR_collectors", "sleep_researchers", "insomnia_apps", "NFT_collectors"],
        "products": ["Limited snore NFTs", "Sleep sound libraries", "Research datasets"],
        "pricing": "$0.05–$5 per unique clip or royalties on secondary sales",
        "clips_created": earnings["clips"]
    }

@app.get("/")
async def root():
    return {
        "service": "SnoreAsset",
        "description": "Passive income from unique snore patterns as collectible sleep assets",
        "automation": "Phone on nightstand → overnight recording → automatic sales"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
