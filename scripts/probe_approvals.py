import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_approvals():
    b = PineLabsAgenticBridge()
    # Test GET approvals
    get_res = b._request("GET", "/approvals")
    print("=== GET /approvals ===")
    print(json.dumps(get_res, indent=2))
    
    # Test POST /approvals empty probe
    post_res = b._request("POST", "/approvals", {})
    print("=== POST /approvals empty probe ===")
    print(json.dumps(post_res, indent=2))

if __name__ == "__main__":
    probe_approvals()
