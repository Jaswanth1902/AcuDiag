import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_tools_endpoint():
    b = PineLabsAgenticBridge()
    endpoints = ["/tools", "/marketplace-surface/tools", "/integrations"]
    for ep in endpoints:
        res = b._request("GET", ep)
        print(f"=== GET {ep} ===")
        print(json.dumps(res, indent=2)[:300])

if __name__ == "__main__":
    check_tools_endpoint()
