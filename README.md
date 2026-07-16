# Max Profit Passive Income Empire

**Fully automated multi-stream passive income system.**  
Zero daily input after one-time setup.

## Live Income Streams

| Stream              | Type                          | Automation Level     | Status     |
|---------------------|-------------------------------|----------------------|------------|
| Premium Data API    | Recurring SaaS + Usage        | Full                 | Production |
| Domain Scanner      | Asset flipping & leasing      | Full                 | Production |
| AI Avatar Service   | High-margin digital product   | Full                 | Production |
| AmbientEnergy       | Smart-home energy data        | Full                 | New        |
| ThoughtLedger       | Emotional trend data          | Full                 | New        |
| EchoBrand           | Ambient brand intelligence    | Full                 | New        |
| GaitGold            | Walking biometrics            | Full                 | New        |

## Quick Start

1. Clone: `git clone https://github.com/baphometsblade/max-profit-passive-empire`
2. Create Supabase project → run `supabase/schema.sql`
3. Add Stripe + Supabase keys to `.env`
4. Deploy `apps/api` to Railway
5. Point Stripe webhook to `/webhook`
6. (Optional) Deploy other microservices

After that the entire system runs with **zero daily input**.

## Architecture

```
apps/
  api/                 ← Core recurring + usage billing
  dashboard/           ← Live metrics
  domain_scanner/      ← Domain opportunities
  ai_avatar/           ← Digital product
  ambient_energy/      ← New: energy signatures
  thought_ledger/      ← New: emotional data
  echo_brand/          ← New: brand ambient intelligence
  gait_gold/           ← New: gait biometrics
frontend/              ← Sales landing page
supabase/              ← Database schema
docs/                  ← Deployment guide
```

## Philosophy

Every stream is designed so that:
- User gives permission once
- Background collection runs forever
- Data is anonymized and sold automatically
- You earn without lifting a finger again

This is the most complete automated passive income system built from the original out-of-the-box ideas.

Repo: https://github.com/baphometsblade/max-profit-passive-empire
