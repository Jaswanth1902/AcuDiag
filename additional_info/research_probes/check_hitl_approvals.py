import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_approvals():
    b = PineLabsAgenticBridge()
    res = b.list_approvals()
    print("=== GET /approvals ===")
    print(json.dumps(res, indent=2))
    
    # Also check audit logs
    audit_res = b.list_audit_logs(limit=3)
    print("=== GET /audit ===")
    print(json.dumps(audit_res, indent=2))

if __name__ == "__main__":
    check_approvals()
