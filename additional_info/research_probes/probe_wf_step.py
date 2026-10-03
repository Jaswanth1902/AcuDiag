import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_step_schema():
    b = PineLabsAgenticBridge()
    res = b._request("POST", "/workflows", {"name": "test_wf", "definition": {"steps": [{}]}})
    print("=== POST /workflows with empty step ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    probe_step_schema()
