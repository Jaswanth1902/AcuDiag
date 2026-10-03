import sys
import json
from pathlib import Path

# Fix Windows console UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def main():
    bridge = PineLabsAgenticBridge()
    print("Checking connection...")
    summary = bridge.get_status_summary()
    print(f"Summary: Connected={summary.get('connected')}, Agents={summary.get('total_agents')}")
    
    approvals = bridge.list_approvals("pending")
    items = approvals.get("items", [])
    print(f"Pending Approvals Count: {len(items)}")
    for i, it in enumerate(items):
        print(f"[{i+1}] ID: {it.get('id')} | Agent: {it.get('agent_name')} | Status: {it.get('status')} | Title: {it.get('title')}")

if __name__ == "__main__":
    main()
