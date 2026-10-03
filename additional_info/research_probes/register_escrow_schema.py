import os
import sys
import json
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.pinelabs_agentic_bridge import PineLabsAgenticBridge

def register_escrow_schema():
    b = PineLabsAgenticBridge()
    schema_payload = {
        "name": "AcuDiagEscrowContractV1",
        "version": "1.0.0",
        "description": "Pine Labs Plural Escrow & Warranty Split Contract with Idempotency Key",
        "json_schema": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "AcuDiagEscrowContractV1",
            "type": "object",
            "required": [
                "contract_id",
                "order_id",
                "customer_phone",
                "technician_id",
                "pre_auth_amount_paise",
                "escrow_state",
                "idempotency_key"
            ],
            "properties": {
                "contract_id": {"type": "string"},
                "order_id": {"type": "string"},
                "customer_phone": {"type": "string"},
                "technician_id": {"type": "string"},
                "pre_auth_amount_paise": {"type": "integer", "minimum": 0},
                "escrow_state": {
                    "enum": [
                        "PRE_AUTH_PENDING",
                        "PRE_AUTH_LOCKED",
                        "RELEASED_CAPTURED",
                        "VOIDED_REFUNDED",
                        "DISPUTED_AUDIT"
                    ]
                },
                "idempotency_key": {"type": "string"},
                "acoustic_evidence_id": {"type": "string"},
                "payout_split": {
                    "type": "object",
                    "properties": {
                        "technician_labor_paise": {"type": "integer"},
                        "oem_parts_paise": {"type": "integer"},
                        "platform_fee_paise": {"type": "integer"},
                        "gst_tax_paise": {"type": "integer"}
                    }
                }
            },
            "additionalProperties": False
        }
    }
    res = b._request("POST", "/schemas", schema_payload)
    print("=== POST /schemas (Escrow Contract) result ===")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    register_escrow_schema()
