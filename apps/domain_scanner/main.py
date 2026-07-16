#!/usr/bin/env python3
"""
Domain Portfolio Scanner
Finds high-potential domains for flipping and leasing.
Run daily via cron or Railway cron job.
"""

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

HOT_TERMS = [
    "aipassive", "passiveai", "sleepincome", "dreamtech",
    "echonet", "trendbot", "phantomdata", "cloneincome",
    "sentientstore", "sliverbank", "gravegpt", "mindmine",
    "autobucks", "zerowork", "autopilotcash", "setforget"
]


def check_availability(terms):
    available = []
    try:
        import whois
        for term in terms:
            domain = f"{term}.com"
            try:
                w = whois.whois(domain)
                if not w.domain_name:
                    available.append(domain)
                    print(f"🔥 AVAILABLE: {domain}")
            except Exception:
                available.append(domain)
                print(f"🔥 LIKELY AVAILABLE: {domain}")
    except ImportError:
        print("python-whois not installed. Run: pip install python-whois")
        print("Falling back to manual list of high-potential names.")
        available = [f"{t}.com" for t in terms[:5]]

    return available


def main():
    print(f"=== Domain Portfolio Scanner - {datetime.utcnow().date()} ===")
    print("Scanning high-potential domains for the passive income empire...\n")

    available = check_availability(HOT_TERMS)

    if available:
        print("\n=== ACTION PLAN ===")
        print("1. Register the available domains (Namecheap / Porkbun / Cloudflare)")
        print("2. List them for lease on Sedo / Afternic / DAN.com")
        print("3. Set lease prices $9–99/month or Buy-It-Now $500–5000")
        print("4. Add purchased domains to Supabase domain_portfolio table")
        print("\nThese can generate real cash flow + appreciating digital assets.")
    else:
        print("No obvious free domains this run. Re-run tomorrow or expand the list.")

    print("\nDone. Schedule this script daily for continuous opportunities.")


if __name__ == "__main__":
    main()
