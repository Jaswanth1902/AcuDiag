import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def decide_hitl():
    b = PineLabsAgenticBridge()
    hitl_id = "212b8414-fe67-4566-ad8e-57d5e0c91231"
    
    payload = {
        "decision": "approve",
        "notes": "Inspector R. Sundaram (Quality Supervisor) - Acoustic trace verified, LRT 0.82 within nominal tolerance. Escrow payment capture authorized.",
        "csrf_token": b.csrf_token
    }
    
    res = b._request("POST", f"/approvals/{hitl_id}/decide", payload)
    print("=== POST /approvals/{id}/decide (HITL Item) ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    decide_hitl()
