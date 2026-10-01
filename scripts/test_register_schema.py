import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def test_register_schema():
    b = PineLabsAgenticBridge()
    schema_payload = {
        "name": "AcousticDiagnosticReportV1",
        "version": "1.0.0",
        "description": "AcuDiag Acoustic DSP Telemetry, Neyman-Pearson LRT, and Anti-Spoofing Telemetry",
        "json_schema": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "AcousticDiagnosticReportV1",
            "type": "object",
            "required": [
                "session_id",
                "appliance_type",
                "snr_db",
                "lrt_ratio",
                "anti_spoofing_passed",
                "fault_detected",
                "confidence",
                "escrow_action"
            ],
            "properties": {
                "session_id": {"type": "string"},
                "appliance_type": {"enum": ["washing_machine", "refrigerator", "microwave", "air_conditioner"]},
                "snr_db": {"type": "number", "minimum": 0},
                "lrt_ratio": {"type": "number"},
                "anti_spoofing_passed": {"type": "boolean"},
                "fault_detected": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "escrow_action": {"enum": ["RELEASE_PAYOUT", "WITHHOLD_PAYOUT", "REJECT_NOISY", "REJECT_REPLAY_ATTACK", "SCHEDULE_AUDIT"]}
            },
            "additionalProperties": False
        }
    }
    res = b._request("POST", "/schemas", schema_payload)
    print("=== POST /schemas result ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test_register_schema()
