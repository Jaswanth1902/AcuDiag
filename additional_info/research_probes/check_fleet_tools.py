import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_agent_tools():
    b = PineLabsAgenticBridge()
    res = b.list_agents()
    for a in res.get("items", []):
        print(f"Agent: {a.get('name')} ({a.get('id')})")
        print(f"  Authorized Tools: {a.get('authorized_tools')}")
        print(f"  Connector IDs: {a.get('connector_ids')}\n")

if __name__ == "__main__":
    check_agent_tools()
