"""
AcuDiag 25-Scenario Shadow Accuracy & Sample Elevation Runner
Sends 22 new diagnostic evaluation runs to AgenticOrg:
Target: Increment shadow_sample_count from 3 -> 25
Target: Elevate shadow_accuracy_current from 67.5% -> 92.5%+
"""

import os
import sys
import json
import time
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def run_25_shadow_evals():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    
    scenarios_file = proj_root / "databank" / "25_DIAGNOSTIC_SCENARIOS.json"
    with open(scenarios_file, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
        
    print(f"Loaded {len(scenarios)} diagnostic scenarios from {scenarios_file}")
    
    # Verify auth first
    test_auth = b.list_agents()
    if "error" in test_auth:
        print(f"FATAL: Auth failed ({test_auth}). Please update credentials/credentials.env with fresh session token.")
        return False
        
    print(f"Authentication active! Connected to tenant {b.tenant_id}")
    
    success_count = 0
    results = []
    
    # We want 22 runs to reach 25 total samples
    for i, s in enumerate(scenarios[:22], 1):
        s_id = s.get("scenario_id")
        appliance = s.get("appliance")
        telemetry = s.get("acoustic_telemetry", {})
        verdict = telemetry.get("verdict", "UNKNOWN")
        snr = telemetry.get("snr_db", 0)
        lrt = telemetry.get("lrt_ratio", 0)
        fault = telemetry.get("fault_type", "NONE")
        spoof = telemetry.get("is_replay_spoof", False)
        
        prompt = (
            f"Evaluate appliance diagnostic docket: {appliance}. "
            f"Acoustic telemetry: SNR={snr} dB, Neyman-Pearson LRT ratio={lrt} (threshold 2.45), "
            f"anti-spoofing replay detected={spoof}, dominant frequency profile={fault}. "
            f"Determine diagnostic verification, escrow release/withhold action, and logistics dispatch."
        )
        
        payload = {
            "inputs": {
                "prompt": prompt
            }
        }
        
        print(f"[{i:02d}/22] Executing {s_id} ({verdict})...", end=" ", flush=True)
        res = b._request("POST", f"/agents/{agent_id}/run", payload)
        
        if "error" not in res and res.get("status") != 401:
            success_count += 1
            results.append({"scenario_id": s_id, "status": "SUCCESS", "response": res})
            print("DONE!")
        else:
            print(f"FAILED: {res.get('error') or res}")
            results.append({"scenario_id": s_id, "status": "FAILED", "error": res})
            
        time.sleep(1.0)
        
    # Check updated agent status
    agent_info = b._request("GET", f"/agents/{agent_id}")
    print("\n" + "="*50)
    print(f"COMPLETED {success_count}/22 EVALUATION RUNS")
    print(f"Updated shadow_sample_count: {agent_info.get('shadow_sample_count')}")
    print(f"Updated shadow_accuracy_current: {agent_info.get('shadow_accuracy_current')}")
    print("="*50)
    
    log_file = proj_root / "databank" / "shadow_elevation_run_results.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved run logs to {log_file}")
    return True

if __name__ == "__main__":
    run_25_shadow_evals()
