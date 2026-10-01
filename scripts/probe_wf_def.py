import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_workflow_definition():
    b = PineLabsAgenticBridge()
    # Test with name and dummy definition
    res = b._request("POST", "/workflows", {"name": "test_wf", "definition": {}})
    print("=== POST /workflows with empty definition ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    probe_workflow_definition()
