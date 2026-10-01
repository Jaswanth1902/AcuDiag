import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def probe_step_structure():
    b = PineLabsAgenticBridge()
    workflow_payload = {
        "name": "AcuDiag_End_to_End_Lifecycle",
        "description": "Autonomous Appliance Diagnostic, Escrow Pre-Auth, Logistics, and LRT Verification Workflow",
        "domain": "ops",
        "trigger_type": "event",
        "definition": {
            "entrypoint": "voice_intake",
            "steps": [
                {
                    "id": "voice_intake",
                    "name": "Gnani Voice Intake",
                    "type": "agent_execution",
                    "agent_id": "c56edea9-8cd1-4e31-bf93-48e024d445d5",
                    "action": "transcribe_and_extract_symptoms",
                    "next": "snr_acoustic_gate"
                },
                {
                    "id": "snr_acoustic_gate",
                    "name": "Acoustic SNR & Anti-Spoofing Gate",
                    "type": "evaluation",
                    "condition": "snr_db >= 15.0 and anti_spoofing == true",
                    "on_failure": "reject_and_request_re-recording",
                    "next": "pre_auth_lock"
                },
                {
                    "id": "pre_auth_lock",
                    "name": "Pine Labs Plural Escrow Pre-Authorization",
                    "type": "connector_call",
                    "connector_id": "a23bbfe2-f52a-4671-b26a-8822e266ebb5",
                    "action": "create_order_pre_auth",
                    "on_decline": "whatsapp_payment_fallback",
                    "next": "dispatch_technician"
                },
                {
                    "id": "dispatch_technician",
                    "name": "Delhivery Express Dispatch",
                    "type": "connector_call",
                    "connector_id": "delhivery_acudiag",
                    "action": "book_technician_pickup",
                    "next": "post_repair_lrt_verification"
                },
                {
                    "id": "post_repair_lrt_verification",
                    "name": "Post-Repair Neyman-Pearson LRT Check",
                    "type": "evaluation",
                    "condition": "lrt_ratio <= 2.45 and anti_spoofing == true",
                    "on_failure": "hitl_supervisor_docket_escalation",
                    "next": "release_escrow_capture"
                },
                {
                    "id": "release_escrow_capture",
                    "name": "Pine Labs Plural Payout Release & Tax Split",
                    "type": "connector_call",
                    "connector_id": "a23bbfe2-f52a-4671-b26a-8822e266ebb5",
                    "action": "capture_payment_and_release",
                    "next": "audit_event_logged"
                },
                {
                    "id": "audit_event_logged",
                    "name": "Immutable Audit Seal",
                    "type": "terminal",
                    "action": "record_grantex_audit_package"
                }
            ]
        }
    }
    res = b._request("POST", "/workflows", workflow_payload)
    print("=== POST /workflows (AcuDiag Lifecycle) result ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    probe_step_structure()
