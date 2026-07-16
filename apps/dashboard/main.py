#!/usr/bin/env python3
"""
Profit Dashboard - Real-time visibility into the empire
"""

import os
from datetime import datetime
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

app = FastAPI(title="Profit Dashboard - Max Profit Empire")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
async def dashboard():
    if not supabase:
        return {
            "status": "dashboard_online",
            "message": "Supabase not configured - showing placeholder metrics",
            "metrics": {
                "total_revenue_usd": 0,
                "mrr_usd": 0,
                "active_subscriptions": 0,
                "total_customers": 0
            }
        }

    payments = supabase.table("payments").select("amount").eq("status", "succeeded").execute()
    total_revenue = sum(p["amount"] or 0 for p in payments.data)

    subs = supabase.table("subscriptions").select("id", count="exact").eq("status", "active").execute()
    active_subs = subs.count or 0

    customers = supabase.table("customers").select("id", count="exact").execute()
    total_customers = customers.count or 0

    mrr = active_subs * 99

    return {
        "status": "live",
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "total_revenue_usd": round(total_revenue, 2),
            "mrr_usd": mrr,
            "active_subscriptions": active_subs,
            "total_customers": total_customers
        },
        "message": "Fully automated. Zero daily input required."
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "supabase": bool(supabase),
        "time": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
