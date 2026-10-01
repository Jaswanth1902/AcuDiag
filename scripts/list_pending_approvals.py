import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def list_pending_approvals():
    b = PineLabsAgenticBridge()
    for status in ["pending", "all", "approved", "rejected"]:
        res = b._request("GET", f"/approvals?status={status}")
        print(f"=== Status {status}: total = {res.get('total', 0)} ===")
        if res.get("items"):
            print(json.dumps(res["items"], indent=2))

if __name__ == "__main__":
    list_pending_approvals()
