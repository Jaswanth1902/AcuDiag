import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def list_connector_ids():
    b = PineLabsAgenticBridge()
    res = b.list_connectors()
    items = res.get("items", [])
    print(f"Total connectors: {len(items)}")
    for item in items:
        print(f"ID: {item.get('id')} | connector_id: {item.get('connector_id')} | name: {item.get('name')}")

if __name__ == "__main__":
    list_connector_ids()
