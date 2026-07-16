#!/usr/bin/env python3
"""
Premium Data API - Core Money Printer v2.1
Recurring subscriptions + Usage-based billing + production Stripe webhooks + Supabase
"""

import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
import stripe
from supabase import create_client, Client

load_dotenv()

app = FastAPI(
    title="Premium Data API - Max Profit Empire",
    description="Automated recurring + usage-based revenue engine",
    version="2.1.0"
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# In-memory usage for demo (use Supabase in production)
usage_store = {}  # customer_id -> {calls: int, last_reset: date}


class SubscribeRequest(BaseModel):
    tier: str = "pro"
    email: Optional[str] = None
    referral_code: Optional[str] = None


class UsageRequest(BaseModel):
    customer_id: str
    endpoint: str = "default"
    units: int = 1


def get_or_create_customer(stripe_customer_id: str, email: str = None) -> dict:
    if not supabase:
        return {"id": None, "stripe_customer_id": stripe_customer_id}
    res = supabase.table("customers").select("*").eq("stripe_customer_id", stripe_customer_id).execute()
    if res.data:
        return res.data[0]
    data = {"stripe_customer_id": stripe_customer_id, "email": email}
    res = supabase.table("customers").insert(data).execute()
    return res.data[0] if res.data else data


@app.get("/")
async def root():
    return {
        "service": "Premium Data API",
        "status": "live",
        "version": "2.1.0",
        "features": ["recurring_subscriptions", "usage_based_billing", "webhooks", "referrals"],
        "docs": "/docs"
    }


@app.post("/subscribe")
async def create_subscription(req: SubscribeRequest):
    if not stripe.api_key:
        raise HTTPException(400, "STRIPE_SECRET_KEY not configured")

    price_map = {
        "starter": 2900,
        "pro": 9900,
        "enterprise": 49900
    }
    amount = price_map.get(req.tier, 9900)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Premium Data Access - {req.tier.title()}",
                        "description": "Automated passive income tools + usage credits"
                    },
                    "unit_amount": amount,
                    "recurring": {"interval": "month"}
                },
                "quantity": 1
            }],
            success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/cancel",
            customer_email=req.email,
            metadata={
                "tier": req.tier,
                "referral_code": req.referral_code or ""
            }
        )
        return {
            "checkout_url": session.url,
            "session_id": session.id,
            "message": "Real recurring + usage-based revenue. Webhooks activate access."
        }
    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/usage")
async def record_usage(req: UsageRequest):
    """Usage-based billing endpoint. Charge extra after free tier."""
    key = req.customer_id
    if key not in usage_store:
        usage_store[key] = {"calls": 0, "overage": 0}

    usage_store[key]["calls"] += req.units

    free_limit = 1000
    if usage_store[key]["calls"] > free_limit:
        overage_units = usage_store[key]["calls"] - free_limit
        usage_store[key]["overage"] = overage_units
        return {
            "status": "overage",
            "total_calls": usage_store[key]["calls"],
            "overage_units": overage_units,
            "estimated_extra_charge_usd": round(overage_units * 0.01, 2),
            "message": "Usage recorded. Overage will be billed at end of period."
        }

    return {
        "status": "ok",
        "total_calls": usage_store[key]["calls"],
        "remaining_free": free_limit - usage_store[key]["calls"]
    }


@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not WEBHOOK_SECRET:
        raise HTTPException(400, "Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")

    event_type = event["type"]
    data = event["data"]["object"]
    print(f"[{datetime.utcnow().isoformat()}] Stripe event: {event_type}")

    if event_type == "checkout.session.completed":
        session = data
        stripe_customer_id = session.get("customer")
        email = session.get("customer_details", {}).get("email")
        amount = (session.get("amount_total") or 0) / 100.0
        tier = session.get("metadata", {}).get("tier", "pro")
        referral_code = session.get("metadata", {}).get("referral_code")

        if supabase and stripe_customer_id:
            customer = get_or_create_customer(stripe_customer_id, email)
            supabase.table("payments").insert({
                "stripe_customer_id": stripe_customer_id,
                "amount": amount,
                "status": "succeeded",
                "event_type": event_type
            }).execute()
            sub_id = session.get("subscription")
            if sub_id:
                supabase.table("subscriptions").upsert({
                    "stripe_subscription_id": sub_id,
                    "customer_id": customer.get("id"),
                    "tier": tier,
                    "status": "active"
                }, on_conflict="stripe_subscription_id").execute()
            if referral_code:
                print(f"Referral credit pending for code: {referral_code}")
            print(f"✅ Customer {stripe_customer_id} activated. Revenue: ${amount:.2f}")

    elif event_type == "customer.subscription.updated":
        if data.get("status") == "active" and supabase:
            supabase.table("subscriptions").update({"status": "active"}).eq("stripe_subscription_id", data["id"]).execute()

    elif event_type == "customer.subscription.deleted":
        if supabase:
            supabase.table("subscriptions").update({"status": "canceled"}).eq("stripe_subscription_id", data["id"]).execute()

    elif event_type == "invoice.payment_succeeded":
        amount = (data.get("amount_paid") or 0) / 100.0
        print(f"Invoice paid: ${amount:.2f}")

    return {"status": "success", "event": event_type}


@app.get("/access/{stripe_customer_id}")
async def check_access(stripe_customer_id: str):
    if not supabase:
        return {"has_access": False, "reason": "Supabase not configured"}
    res = supabase.table("subscriptions") \
        .select("*, customers!inner(stripe_customer_id)") \
        .eq("customers.stripe_customer_id", stripe_customer_id) \
        .eq("status", "active") \
        .execute()
    has_access = len(res.data) > 0
    return {"has_access": has_access, "subscriptions": res.data if has_access else []}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "stripe_configured": bool(stripe.api_key),
        "supabase_configured": bool(supabase),
        "usage_based_billing": True,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Premium Data API v2.1 starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
