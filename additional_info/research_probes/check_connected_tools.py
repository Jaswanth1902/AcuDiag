import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_connected_tools():
    b = PineLabsAgenticBridge()
    res = b.list_connectors()
    for item in res.get("items", []):
        name = item.get("name")
        c_id = item.get("id")
        tools = item.get("tool_functions", [])
        print(f"Connector: {name} (ID: {c_id}) -> Tools: {tools}")

if __name__ == "__main__":
    check_connected_tools()
