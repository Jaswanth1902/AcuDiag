import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_schemas_post():
    b = PineLabsAgenticBridge()
    res = b._request("POST", "/schemas", {})
    print("=== POST /schemas empty probe ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    probe_schemas_post()
