import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_decide_approval():
    b = PineLabsAgenticBridge()
    # Governance approval ID
    gov_app_id = "8a2cc5eb-e8f6-489f-9a83-6270bdb2d7ce"
    
    # Try POST /approvals/{id}/decide or PATCH /approvals/{id}
    payload = {
        "decision": "approve",
        "notes": "Approved by Domain Lead Jaswanth Reddy for AcuDiag operational baseline.",
        "csrf_token": b.csrf_token
    }
    
    # Try POST /approvals/{id}/decide
    res = b._request("POST", f"/approvals/{gov_app_id}/decide", payload)
    print("=== POST /approvals/{id}/decide ===")
    print(json.dumps(res, indent=2))
    
    if "error" in res and res.get("status") == 404:
        # Try POST /approvals/{id}/decision
        res2 = b._request("POST", f"/approvals/{gov_app_id}/decision", payload)
        print("=== POST /approvals/{id}/decision ===")
        print(json.dumps(res2, indent=2))

if __name__ == "__main__":
    test_decide_approval()
