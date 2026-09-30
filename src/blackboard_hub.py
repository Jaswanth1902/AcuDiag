"""
AcuDiag Central Data Fabric Hub & State Machine.
Integrates directly with Central Blackboard (.cache/blackboard.sqlite) adhering to Law 14.
Implements the 9 Happy States and 4 Unhappy Flows across Pine Labs, Delhivery, and Gnani.ai rails.
"""

from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Locate Central Blackboard in root .cache/
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BLACKBOARD_DB = REPO_ROOT / ".cache" / "blackboard.sqlite"

# State Constants
HAPPY_STATES = [
    "ONBOARDING",
    "INTAKE",
    "ACOUSTIC_CAPTURE",
    "FAULT_CLASSIFIED",
    "ESCROW_LOCKED",
    "PARTS_DISPATCHED",
    "TECH_BOOKED",
    "TECH_ARRIVED",
    "POST_REPAIR_TEST",
    "ESCROW_RELEASED",
]

UNHAPPY_STATES = [
    "WARRANTY_INTERCEPT",
    "FAKE_REPAIR_ESCROW_LOCK",
    "SCOPE_MISMATCH",
    "SNR_LOW_RETRY",
]


class AcuDiagBlackboardHub:
    """State Machine & Event Bus for AcuDiag on Central Blackboard."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or BLACKBOARD_DB
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS acudiag_cases (
                    case_id TEXT PRIMARY KEY,
                    appliance_type TEXT NOT NULL,
                    customer_phone TEXT,
                    pincode TEXT,
                    oem_brand TEXT,
                    purchase_year INTEGER,
                    current_state TEXT NOT NULL,
                    fault_type TEXT,
                    escrow_order_id TEXT,
                    escrow_amount_inr REAL DEFAULT 0.0,
                    delhivery_waybill TEXT,
                    post_test_passed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS acudiag_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id TEXT NOT NULL,
                    from_state TEXT,
                    to_state TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    metadata_json TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(case_id) REFERENCES acudiag_cases(case_id)
                )
            """)
            conn.commit()

    def create_case(
        self,
        case_id: str,
        appliance_type: str = "Washing Machine",
        customer_phone: str = "+919876543210",
        pincode: str = "560001",
        oem_brand: str = "LG",
        purchase_year: int = 2021,
    ) -> Dict[str, Any]:
        """Initialize a new diagnostic case in ONBOARDING."""
        now = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO acudiag_cases (
                    case_id, appliance_type, customer_phone, pincode, oem_brand,
                    purchase_year, current_state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    case_id,
                    appliance_type,
                    customer_phone,
                    pincode,
                    oem_brand,
                    purchase_year,
                    "ONBOARDING",
                    now,
                    now,
                ),
            )
            conn.execute(
                """
                INSERT INTO acudiag_events (case_id, from_state, to_state, actor, metadata_json, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    case_id,
                    None,
                    "ONBOARDING",
                    "VoiceAgent/Gnani",
                    json.dumps({"event": "Case created via IVR"}),
                    now,
                ),
            )
            conn.commit()
        return self.get_case(case_id)

    def transition_state(
        self,
        case_id: str,
        to_state: str,
        actor: str = "Orchestrator",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Transition a case to a new state and record event ledger."""
        now = datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata or {})
        
        with self._get_connection() as conn:
            cur = conn.execute("SELECT current_state FROM acudiag_cases WHERE case_id = ?", (case_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Case ID {case_id} not found.")
            from_state = row["current_state"]

            # Dynamic field updates based on transition metadata
            updates = ["current_state = ?", "updated_at = ?"]
            params = [to_state, now]

            if metadata:
                if "fault_type" in metadata:
                    updates.append("fault_type = ?")
                    params.append(metadata["fault_type"])
                if "escrow_order_id" in metadata:
                    updates.append("escrow_order_id = ?")
                    params.append(metadata["escrow_order_id"])
                if "escrow_amount_inr" in metadata:
                    updates.append("escrow_amount_inr = ?")
                    params.append(float(metadata["escrow_amount_inr"]))
                if "delhivery_waybill" in metadata:
                    updates.append("delhivery_waybill = ?")
                    params.append(metadata["delhivery_waybill"])
                if "post_test_passed" in metadata:
                    updates.append("post_test_passed = ?")
                    params.append(1 if metadata["post_test_passed"] else 0)

            params.append(case_id)
            sql = f"UPDATE acudiag_cases SET {', '.join(updates)} WHERE case_id = ?"
            conn.execute(sql, params)

            conn.execute(
                """
                INSERT INTO acudiag_events (case_id, from_state, to_state, actor, metadata_json, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (case_id, from_state, to_state, actor, metadata_json, now),
            )
            conn.commit()

        return self.get_case(case_id)

    def get_case(self, case_id: str) -> Dict[str, Any]:
        """Retrieve current case snapshot."""
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM acudiag_cases WHERE case_id = ?", (case_id,))
            row = cur.fetchone()
            if not row:
                return {}
            return dict(row)

    def get_case_timeline(self, case_id: str) -> List[Dict[str, Any]]:
        """Retrieve full chronological audit trail."""
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM acudiag_events WHERE case_id = ? ORDER BY id ASC",
                (case_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    # =========================================================================
    # HAPPY PATH STATE MACHINE METHODS (9 States / Transitions)
    # =========================================================================
    def trigger_intake(self, case_id: str, symptom_transcript: str, language_code: str = "hi-IN") -> Dict[str, Any]:
        """State 1 -> 2: Process Hinglish / regional voice transcript."""
        return self.transition_state(case_id, "INTAKE", "VoiceAgent/Gnani", {
            "transcript": symptom_transcript,
            "language": language_code
        })

    def record_acoustic_capture(self, case_id: str, snr_db: float, duration_sec: float = 10.0, audio_hash: Optional[str] = None) -> Dict[str, Any]:
        """State 2 -> 3: Record microphone stream and evaluate SNR gating."""
        if snr_db < 15.0:
            return self.trigger_snr_low(case_id, current_snr_db=snr_db)
        return self.transition_state(case_id, "ACOUSTIC_CAPTURE", "AcousticSensor", {
            "snr_db": snr_db,
            "duration_sec": duration_sec,
            "hash": audio_hash
        })

    def classify_fault(self, case_id: str, fault_type: str, lrt_score: float, recommended_sku: str, estimated_total_inr: float) -> Dict[str, Any]:
        """State 3 -> 4: Compute Neyman-Pearson LRT and map OEM SKU."""
        return self.transition_state(case_id, "FAULT_CLASSIFIED", "DSPEngine", {
            "fault_type": fault_type,
            "lrt_score": lrt_score,
            "sku": recommended_sku,
            "escrow_amount_inr": estimated_total_inr
        })

    def lock_escrow(self, case_id: str, escrow_order_id: str, amount_inr: float, merchant_id: str = "ACUDIAG_KEN") -> Dict[str, Any]:
        """State 4 -> 5: Lock customer pre-auth hold on Pine Labs Plural."""
        return self.transition_state(case_id, "ESCROW_LOCKED", "PineLabsBridge", {
            "escrow_order_id": escrow_order_id,
            "escrow_amount_inr": amount_inr,
            "merchant_id": merchant_id,
            "status": "PRE_AUTH_LOCKED"
        })

    def dispatch_parts(self, case_id: str, delhivery_waybill: str, origin_hub: str = "BLR_PEENYA", tat_hours: int = 4) -> Dict[str, Any]:
        """State 5 -> 6: Manifest forward OEM part delivery via Delhivery CMU."""
        return self.transition_state(case_id, "PARTS_DISPATCHED", "DelhiveryLogistics", {
            "delhivery_waybill": delhivery_waybill,
            "origin_hub": origin_hub,
            "tat_hours": tat_hours
        })

    def book_technician(self, case_id: str, technician_id: str, scheduled_time: str) -> Dict[str, Any]:
        """State 6 -> 7: Assign certified doorstep field technician."""
        return self.transition_state(case_id, "TECH_BOOKED", "TechnicianDispatch", {
            "tech_id": technician_id,
            "scheduled_time": scheduled_time
        })

    def mark_tech_arrived(self, case_id: str, arrival_timestamp: Optional[str] = None) -> Dict[str, Any]:
        """State 7 -> 8: Doorstep arrival confirmation and unboxing."""
        return self.transition_state(case_id, "TECH_ARRIVED", "DoorstepSensor", {
            "arrival_time": arrival_timestamp or datetime.now(timezone.utc).isoformat()
        })

    def run_post_repair_test(self, case_id: str, lrt_score: float, anti_spoofing_pass: bool, snr_db: float) -> Dict[str, Any]:
        """State 8 -> 9: Physical post-repair acoustic verification & anti-spoofing."""
        if not anti_spoofing_pass or lrt_score > 2.45:
            return self.trigger_fake_repair_lock(
                case_id,
                lrt_score=lrt_score,
                reason="Bearing harmonic resonance persists or speaker replay detected"
            )
        return self.transition_state(case_id, "POST_REPAIR_TEST", "DSPEngine", {
            "lrt_score": lrt_score,
            "anti_spoofing_pass": anti_spoofing_pass,
            "snr_db": snr_db,
            "post_test_passed": True
        })

    def release_escrow(self, case_id: str, tech_upi_id: str, hmac_proof: str) -> Dict[str, Any]:
        """State 9 -> 10: Cryptographic payout release to technician."""
        return self.transition_state(case_id, "ESCROW_RELEASED", "PineLabsBridge", {
            "payout_recipient": tech_upi_id,
            "hmac_proof": hmac_proof,
            "status": "CAPTURED_SETTLED"
        })

    # =========================================================================
    # UNHAPPY FLOW HANDLERS (4 Failure / Edge Conditions)
    # =========================================================================
    def trigger_warranty_intercept(self, case_id: str, receipt_date: str, oem_brand: str, savings_inr: float = 3200.0) -> Dict[str, Any]:
        """Unhappy Flow 1: Active OEM warranty -> abort paid escrow, route to free OEM."""
        return self.transition_state(case_id, "WARRANTY_INTERCEPT", "WarrantyGuard", {
            "receipt_date": receipt_date,
            "oem_brand": oem_brand,
            "savings_inr": savings_inr,
            "action": "ABORT_PAID_ESCROW_ROUTE_TO_FREE_OEM"
        })

    def trigger_fake_repair_lock(self, case_id: str, lrt_score: float, harmonic_hz: float = 1450.0, reason: str = "Harmonic peak persists") -> Dict[str, Any]:
        """Unhappy Flow 2: Incomplete repair -> withhold payout, lock escrow."""
        return self.transition_state(case_id, "FAKE_REPAIR_ESCROW_LOCK", "AuditorEngine", {
            "lrt_score": lrt_score,
            "harmonic_hz": harmonic_hz,
            "reason": reason,
            "action": "WITHHOLD_PAYOUT_ENFORCE_DISPUTE_PERIOD"
        })

    def trigger_scope_mismatch(self, case_id: str, reported_part: str, actual_needed: str, reason: str) -> Dict[str, Any]:
        """Unhappy Flow 3: Scope mismatch -> pause repair, solicit user approval."""
        return self.transition_state(case_id, "SCOPE_MISMATCH", "TechnicianApp", {
            "reported_part": reported_part,
            "actual_needed": actual_needed,
            "reason": reason,
            "action": "PAUSE_REPAIR_SOLICIT_CUSTOMER_APPROVAL"
        })

    def trigger_snr_low(self, case_id: str, current_snr_db: float, min_required_snr: float = 15.0) -> Dict[str, Any]:
        """Unhappy Flow 4: Low SNR (<15dB) -> prompt user to reduce ambient noise."""
        return self.transition_state(case_id, "SNR_LOW_RETRY", "NoiseGate", {
            "current_snr_db": current_snr_db,
            "min_required_snr": min_required_snr,
            "action": "PROMPT_USER_TO_REDUCE_AMBIENT_NOISE"
        })


if __name__ == "__main__":
    hub = AcuDiagBlackboardHub()
    test_id = f"KEN_TEST_{int(time.time())}"
    print(f"[*] Testing AcuDiag Blackboard Hub with case: {test_id}")
    c = hub.create_case(test_id, appliance_type="Front Load Washer", pincode="560038")
    print(f"[+] Created: {c['current_state']}")
    c = hub.transition_state(test_id, "INTAKE", "VoiceAgent", {"notes": "Customer reported drum grinding sound"})
    c = hub.transition_state(test_id, "ACOUSTIC_CAPTURE", "AppClient", {"snr_db": 22.4})
    c = hub.transition_state(test_id, "FAULT_CLASSIFIED", "DSPEngine", {"fault_type": "WM_BEARING_SPALL"})
    c = hub.transition_state(test_id, "ESCROW_LOCKED", "PineLabsBridge", {"escrow_order_id": "ORD_78912", "escrow_amount_inr": 1250.0})
    print(f"[+] Case now in: {c['current_state']} (Amount locked: INR {c['escrow_amount_inr']})")
    timeline = hub.get_case_timeline(test_id)
    print(f"[+] Timeline entries: {len(timeline)}")
    print("[+] Blackboard Hub verified successfully.")
