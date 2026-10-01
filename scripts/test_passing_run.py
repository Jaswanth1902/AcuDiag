import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_passing_eval_run():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    agent_payload = {
        "inputs": {
            "prompt": "Evaluate appliance acoustic repair verification: Samsung 6.5kg washing machine baseline test. SNR is 26.5 dB (>15 dB). Anti-Spoofing passed (genuine mechanical vibration detected at 50Hz motor harmonics). Post-repair Neyman-Pearson LRT ratio is 0.82 (threshold <= 2.45). Escrow pre-auth order PL_ORD_98124 currently locked. Determine final diagnostic verdict, escrow release action, and payment capture instructions."
        }
    }
    res_agent = b._request("POST", f"/agents/{agent_id}/run", agent_payload)
    print("=== POST /agents/{id}/run (PASSING CASE) ===")
    print(json.dumps(res_agent, indent=2))

if __name__ == "__main__":
    test_passing_eval_run()
