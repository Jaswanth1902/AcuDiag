import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def tune_confidence_floor():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    payload = {
        "confidence_floor": 0.65,
        "hitl_condition": "confidence < 0.65"
    }
    patch_res = b._request("PATCH", f"/agents/{agent_id}", payload)
    print("=== PATCH confidence_floor: 0.65 ===")
    print(json.dumps(patch_res, indent=2))
    
    # Run the passing case again
    agent_payload = {
        "inputs": {
            "prompt": "Evaluate appliance acoustic repair verification: Samsung 6.5kg washing machine baseline test. SNR is 26.5 dB (>15 dB). Anti-Spoofing passed (genuine mechanical vibration detected at 50Hz motor harmonics). Post-repair Neyman-Pearson LRT ratio is 0.82 (threshold <= 2.45). Escrow pre-auth order PL_ORD_98124 currently locked. Determine final diagnostic verdict, escrow release action, and payment capture instructions."
        }
    }
    run_res = b._request("POST", f"/agents/{agent_id}/run", agent_payload)
    print("=== POST /agents/{id}/run (CONFIDENCE 0.65) ===")
    print(json.dumps(run_res, indent=2))

if __name__ == "__main__":
    tune_confidence_floor()
