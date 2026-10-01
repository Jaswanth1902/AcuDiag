import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def delete_test_wf():
    b = PineLabsAgenticBridge()
    wf_id = "0e6c1a37-2640-4ca4-8d42-c133c8559551"
    # Send csrf_token in query and body
    res = b._request("DELETE", f"/workflows/{wf_id}?csrf_token={b.csrf_token}", {"csrf_token": b.csrf_token})
    print("=== DELETE with query and body ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    delete_test_wf()
