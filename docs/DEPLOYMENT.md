# Deployment Guide – Zero Input After Setup

## Recommended: Railway.app (easiest for FastAPI)

1. Create free account at railway.app
2. New Project → Deploy from GitHub (or upload folder)
3. Add environment variables from `.env.example`
4. Deploy
5. Copy the public URL (e.g. https://your-app.up.railway.app)

## Stripe Webhook Setup (Critical)

1. Stripe Dashboard → Developers → Webhooks → Add endpoint
2. Endpoint URL: `https://your-railway-url.com/webhook`
3. Select events:
   - checkout.session.completed
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - invoice.payment_succeeded
4. Copy Signing secret → put in `STRIPE_WEBHOOK_SECRET`

## Supabase

1. Create project
2. Run `supabase/schema.sql`
3. Copy Project URL + service_role key

## After Deployment

- The API accepts real payments automatically
- Webhooks grant/revoke access without any human action
- Dashboard shows live metrics
- Domain scanner can be run via Railway Cron or GitHub Actions daily

You now have real recurring passive income infrastructure.
No further daily work required.
