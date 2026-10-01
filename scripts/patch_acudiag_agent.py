import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def patch_acudiag_agent():
    b = PineLabsAgenticBridge()
    agent_id = "c56edea9-8cd1-4e31-bf93-48e024d445d5"
    plural_id = "a23bbfe2-f52a-4671-b26a-8822e266ebb5"
    gstn_id = "f633016f-b50c-47f2-a441-e7fec642d0fd"
    schema_id = "8d691dd3-9238-450b-b46b-fc40e5e8c8a4"
    
    payload = {
        "connector_ids": [plural_id, gstn_id],
        "output_schema": schema_id,
        "designation": "Autonomous Appliance Reliability & Escrow Orchestrator",
        "specialization": "Acoustic DSP, Neyman-Pearson LRT, Multi-Party Escrow",
        "employee_name": "AcuDiag AI",
        "description": "Zero-trust physical verification and escrow automation for consumer appliances",
        "status": "shadow"
    }
    res = b._request("PATCH", f"/agents/{agent_id}", payload)
    print("=== PATCH /agents/{id} result ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    patch_acudiag_agent()
