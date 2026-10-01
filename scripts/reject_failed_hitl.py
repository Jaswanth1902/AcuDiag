import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def reject_failed_hitl():
    b = PineLabsAgenticBridge()
    hitl_id = "5eee38bc-9187-4aba-9d4b-b4662fa9349f"
    
    payload = {
        "decision": "reject",
        "notes": "Inspector R. Sundaram (Quality Supervisor) - Acoustic test failed (LRT 3.12 > 2.45). Withholding payout to technician per Invariant 6. Secondary audit dispatch booked.",
        "csrf_token": b.csrf_token
    }
    
    res = b._request("POST", f"/approvals/{hitl_id}/decide", payload)
    print("=== POST /approvals/{id}/decide (Reject Withhold) ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    reject_failed_hitl()
