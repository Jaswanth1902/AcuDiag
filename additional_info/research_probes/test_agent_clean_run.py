import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_run_without_unconfigured_connectors():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    # Temporarily remove connector_ids
    patch_res = b._request("PATCH", f"/agents/{agent_id}", {
        "connector_ids": [],
        "authorized_tools": ["create_ticket", "search_issues"]
    })
    print("=== PATCH connector_ids: [] ===")
    print(json.dumps(patch_res, indent=2))
    
    # Run agent
    run_res = b._request("POST", f"/agents/{agent_id}/run", {
        "inputs": {
            "prompt": "Evaluate appliance noise complaint: Whirlpool 7kg spin cycle bearing rattle with SNR 18.2 dB and LRT ratio 3.12."
        }
    })
    print("=== POST /agents/{id}/run ===")
    print(json.dumps(run_res, indent=2))

if __name__ == "__main__":
    test_run_without_unconfigured_connectors()
