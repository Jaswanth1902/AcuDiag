import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def list_all_tools():
    b = PineLabsAgenticBridge()
    res = b._request("GET", "/tools")
    tools = res.get("tools", [])
    print(f"Total tools available: {len(tools)}")
    print("Sample tools:")
    print(json.dumps(tools[:30], indent=2))
    
    # Filter for pine, payment, invoice, logistics, tally, zoho, etc.
    relevant_tools = [t for t in tools if any(k in t.lower() for k in ["pine", "plural", "pay", "order", "invoice", "tally", "zoho", "gstn", "delhivery", "logistics", "ticket"])]
    print(f"\nRelevant tools for AcuDiag ({len(relevant_tools)}):")
    print(json.dumps(relevant_tools, indent=2))

if __name__ == "__main__":
    list_all_tools()
