import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def check_run_and_agent_run():
    b = PineLabsAgenticBridge()
    wf_id = "e8f26cb5-e230-4220-b0e3-51350db719e8"
    run_id = "e883aee7-0811-4e87-9e46-67cdc3c369d3"
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    # Check workflow run status
    res_wf_run = b._request("GET", f"/workflows/runs/{run_id}")
    print("=== GET /workflows/runs/{run_id} ===")
    print(json.dumps(res_wf_run, indent=2))
    
    # Try agent run with inputs dict
    agent_payload = {
        "inputs": {
            "prompt": "Evaluate appliance noise complaint: Whirlpool 7kg spin cycle bearing rattle with SNR 18.2 dB and LRT ratio 3.12."
        }
    }
    res_agent = b._request("POST", f"/agents/{agent_id}/run", agent_payload)
    print("=== POST /agents/{id}/run ===")
    print(json.dumps(res_agent, indent=2))

if __name__ == "__main__":
    check_run_and_agent_run()
