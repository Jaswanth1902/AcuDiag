import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_runs():
    b = PineLabsAgenticBridge()
    wf_id = "e8f26cb5-e230-4220-b0e3-51350db719e8"
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    # Probe workflow run
    res_wf = b._request("POST", f"/workflows/{wf_id}/run", {"input": {"session_id": "TEST_SESSION_001"}})
    print("=== POST /workflows/{id}/run ===")
    print(json.dumps(res_wf, indent=2))
    
    # Probe agent run / execute
    res_agent = b._request("POST", f"/agents/{agent_id}/run", {"input": "Check diagnostic status"})
    print("=== POST /agents/{id}/run ===")
    print(json.dumps(res_agent, indent=2))

if __name__ == "__main__":
    probe_runs()
