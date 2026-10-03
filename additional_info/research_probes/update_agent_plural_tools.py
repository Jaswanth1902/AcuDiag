import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def update_agent_plural_tools():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    tools_to_authorize = [
        "pinelabs_plural__create_order",
        "pinelabs_plural__create_payment_link",
        "pinelabs_plural__get_order_status",
        "pinelabs_plural__get_payout_analytics",
        "pinelabs_plural__initiate_refund",
        "gstn__generate_einvoice_irn",
        "gstn__generate_eway_bill"
    ]
    
    payload = {
        "authorized_tools": tools_to_authorize
    }
    
    res = b._request("PATCH", f"/agents/{agent_id}", payload)
    print("=== PATCH authorized_tools result ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    update_agent_plural_tools()
