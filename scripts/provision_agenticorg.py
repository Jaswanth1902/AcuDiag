"""
Provision AcuDiag Connectors, Knowledge Base, and Agent on Pine Labs AgenticOrg.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def run():
    print("=" * 70)
    print(">> PINELABS AGENTICORG: ACUDIAG FLEET PROVISIONING")
    print("=" * 70)
    
    bridge = PineLabsAgenticBridge()
    print(f"[*] Target Tenant ID: {bridge.tenant_id}")
    print(f"[*] User Account: {bridge.user_id}")
    print("[*] Executing provision_full_acudiag_stack()...")
    
    res = bridge.provision_full_acudiag_stack(mock_server_url="http://127.0.0.1:8000")
    for k, v in res.items():
        status = v.get("status", "SUCCESS")
        print(f"  + [{k}]: status={status}")
        if "remote_response" in v and "error" in v["remote_response"]:
            print(f"    - Remote Note: {v['remote_response']['error']}")

    print("\n[*] Fetching AgenticOrg Fleet Summary...")
    summary = bridge.get_status_summary()
    print(json.dumps(summary, indent=2))
    print("=" * 70)
    print(">> AGENTICORG PROVISIONING RUN COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    run()
