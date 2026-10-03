import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_wf():
    b = PineLabsAgenticBridge()
    wf_id = "0e6c1a37-2640-4ca4-8d42-c133c8559551"
    res = b._request("GET", f"/workflows/{wf_id}")
    print("=== GET /workflows/{id} ===")
    print(json.dumps(res, indent=2))
    
    # Clean up test workflow
    del_res = b._request("DELETE", f"/workflows/{wf_id}")
    print("=== DELETE /workflows/{id} ===")
    print(json.dumps(del_res, indent=2))

if __name__ == "__main__":
    check_wf()
