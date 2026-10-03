import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_connector_config():
    b = PineLabsAgenticBridge()
    plural_id = "a23bbfe2-f52a-4671-b26a-8822e266ebb5"
    
    # Check GET connector details
    res_get = b._request("GET", f"/connectors/{plural_id}")
    print("=== GET /connectors/{id} ===")
    print(json.dumps(res_get, indent=2))
    
    # Check credentials / health endpoint
    res_health = b._request("POST", f"/connectors/{plural_id}/health")
    print("=== POST /connectors/{id}/health ===")
    print(json.dumps(res_health, indent=2))

if __name__ == "__main__":
    probe_connector_config()
