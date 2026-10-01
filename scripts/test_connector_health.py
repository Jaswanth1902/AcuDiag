import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_connector_health():
    b = PineLabsAgenticBridge()
    plural_id = "a23bbfe2-f52a-4671-b26a-8822e266ebb5"
    res_health = b._request("POST", f"/connectors/{plural_id}/health", {"csrf_token": b.csrf_token})
    print("=== POST /connectors/{id}/health with CSRF ===")
    print(json.dumps(res_health, indent=2))

if __name__ == "__main__":
    test_connector_health()
