import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_workflows():
    b = PineLabsAgenticBridge()
    # Try a minimal POST to inspect validation errors
    res = b._request("POST", "/workflows", {})
    print("=== POST /workflows response ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    probe_workflows()
