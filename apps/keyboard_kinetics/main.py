#!/usr/bin/env python3
"""
KeyboardKinetics - Out-of-the-box Passive Income Stream
Captures unique typing rhythm, pressure, and correction patterns.
Sells anonymized "idiolect" models to AI labs for more human-like chatbots.
Completely passive after keyboard extension install.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

app = FastAPI(title="KeyboardKinetics - Max Profit Empire", version="1.0.0")

class TypingFingerprint(BaseModel):
    features: Dict[str, Any]   # rhythm, dwell, flight, corrections, emoji patterns
    session_minutes: float
    consent: bool = True

earnings = {"total_usd": 0.0, "sessions": 0}

@app.post("/fingerprint")
async def submit_typing(fp: TypingFingerprint):
    if not fp.consent:
        raise HTTPException(400, "Consent required")
    
    value = 0.025 * min(fp.session_minutes / 10, 3)  # higher for longer sessions
    earnings["total_usd"] += value
    earnings["sessions"] += 1
    
    return {
        "status": "sold",
        "earnings_usd": round(value, 4),
        "total_kinetics_revenue": round(earnings["total_usd"], 4),
        "message": "Typing idiolect sold to AI labs. Fully passive."
    }

@app.get("/marketplace")
async def marketplace():
    return {
        "buyers": ["AI_labs", "LLM_companies", "chatbot_platforms", "voice_assistant_makers"],
        "products": ["Human-like typing models", "Idiolect fine-tuning data", "Authenticity detectors"],
        "pricing": "$0.02–$0.10 per session or $499–$4999/mo for bulk models",
        "sessions": earnings["sessions"]
    }

@app.get("/")
async def root():
    return {
        "service": "KeyboardKinetics",
        "description": "Passive income from unique typing biometrics sold to AI",
        "automation": "Keyboard extension once → continuous model sales"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
