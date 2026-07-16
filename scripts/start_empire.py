#!/usr/bin/env python3
"""
One-command empire launcher (local development)
"""

import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).parent.parent

print("🚀 Starting Max Profit Passive Income Empire...")
print("Press Ctrl+C to stop all services.\n")

services = [
    (BASE / "apps/api/main.py", 8000, "Premium Data API"),
    (BASE / "apps/dashboard/main.py", 8001, "Profit Dashboard"),
]

procs = []
for script, port, name in services:
    print(f"Starting {name} on :{port}")
    p = subprocess.Popen([sys.executable, str(script)])
    procs.append(p)
    time.sleep(1.5)

print("\n✅ Empire is live")
print("  API:       http://localhost:8000")
print("  Dashboard: http://localhost:8001")
print("  Docs:      http://localhost:8000/docs")
print("\nRun domain scanner separately:")
print("  python apps/domain_scanner/main.py")
print("\nEverything after deployment runs with zero daily input.")

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    for p in procs:
        p.terminate()
