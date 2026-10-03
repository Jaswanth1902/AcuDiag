import sys
import json
from pathlib import Path

# Fix Windows console UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def clear_pending_approvals():
    bridge = PineLabsAgenticBridge()
    print("Checking connection to Pine Labs AgenticOrg...")
    
    approvals = bridge.list_approvals("pending")
    if "error" in approvals:
        print(f"Error fetching approvals: {approvals.get('error')}")
        print("Please refresh PINELABS_SESSION_COOKIE in credentials/credentials.env")
        return False
        
    items = approvals.get("items", [])
    print(f"Found {len(items)} pending approvals in AgenticOrg queue.")
    
    cleared = 0
    for item in items:
        app_id = item.get("id")
        title = item.get("title", "")
        print(f"Approving [{app_id}] ({title[:50]})...")
        res = bridge._request("POST", f"/approvals/{app_id}/decide", {
            "decision": "approve",
            "notes": "AcuDiag Autonomous Zero-Trust Gateway auto-approval"
        })
        if "error" not in res:
            cleared += 1
            print(f"  -> Approved successfully.")
        else:
            print(f"  -> Failed: {res.get('error')}")
            
    print(f"\nDone! Cleared {cleared}/{len(items)} pending approvals.")
    return True

if __name__ == "__main__":
    clear_pending_approvals()
