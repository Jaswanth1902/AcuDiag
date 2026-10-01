import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_connector_registry():
    b = PineLabsAgenticBridge()
    res = b._request("GET", "/connectors/registry")
    if "error" in res:
        print("Error:", res)
    else:
        print(f"Registry keys: {list(res.keys())}")
        if "items" in res:
            print(f"Total registry items: {len(res['items'])}")
            print("Sample connectors in registry:")
            for item in res["items"][:10]:
                print(f"  {item.get('name')} ({item.get('id')}) - Tools: {item.get('tools', [])[:3]}")
        else:
            print(json.dumps(res, indent=2)[:500])

if __name__ == "__main__":
    check_connector_registry()
