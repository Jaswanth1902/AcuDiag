"""
Tests for AcuDiag Central Data Fabric Hub & State Machine.
Verifies the 9 Happy States and 4 Unhappy Flows across SQLite WAL mode.
"""

import os
import sys
import time
from pathlib import Path
import pytest

# Add project root and src to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from blackboard_hub import AcuDiagBlackboardHub, HAPPY_STATES, UNHAPPY_STATES

@pytest.fixture
def hub(tmp_path):
    """Fixture providing an isolated SQLite database instance."""
    db_file = tmp_path / "test_blackboard.sqlite"
    return AcuDiagBlackboardHub(db_path=db_file)

def test_happy_flow_end_to_end(hub):
    case_id = f"CASE_HAPPY_{int(time.time())}"
    
    # 1. State: ONBOARDING
    case = hub.create_case(case_id, appliance_type="Front Load Washer", customer_phone="+919876543210", pincode="560059")
    assert case["current_state"] == "ONBOARDING"
    assert case["appliance_type"] == "Front Load Washer"

    # 2. State: INTAKE (Hinglish voice description)
    case = hub.trigger_intake(case_id, "Washing machine se drum grinding awaz aa rahi hai")
    assert case["current_state"] == "INTAKE"

    # 3. State: ACOUSTIC_CAPTURE (SNR check pass >= 15 dB)
    case = hub.record_acoustic_capture(case_id, snr_db=22.4, duration_sec=10.0, audio_hash="HASH_AUDIO_123")
    assert case["current_state"] == "ACOUSTIC_CAPTURE"

    # 4. State: FAULT_CLASSIFIED (Neyman-Pearson LRT detection)
    case = hub.classify_fault(case_id, fault_type="WM_BEARING_SPALL", lrt_score=5.82, recommended_sku="BEAR-6205-2RS", estimated_total_inr=1250.0)
    assert case["current_state"] == "FAULT_CLASSIFIED"
    assert case["fault_type"] == "WM_BEARING_SPALL"
    assert case["escrow_amount_inr"] == 1250.0

    # 5. State: ESCROW_LOCKED (Pine Labs pre-auth hold)
    case = hub.lock_escrow(case_id, escrow_order_id="PL_ORD_9821A", amount_inr=1250.0)
    assert case["current_state"] == "ESCROW_LOCKED"
    assert case["escrow_order_id"] == "PL_ORD_9821A"

    # 6. State: PARTS_DISPATCHED (Delhivery CMU forward manifestation)
    case = hub.dispatch_parts(case_id, delhivery_waybill="DEL_WAYBILL_8819", origin_hub="BLR_PEENYA")
    assert case["current_state"] == "PARTS_DISPATCHED"
    assert case["delhivery_waybill"] == "DEL_WAYBILL_8819"

    # 7. State: TECH_BOOKED (Doorstep technician assignment)
    case = hub.book_technician(case_id, technician_id="TECH_KUMAR_01", scheduled_time="Tomorrow 11:00 AM")
    assert case["current_state"] == "TECH_BOOKED"

    # 8. State: TECH_ARRIVED (Doorstep arrival & unboxing)
    case = hub.mark_tech_arrived(case_id)
    assert case["current_state"] == "TECH_ARRIVED"

    # 9. State: POST_REPAIR_TEST (Acoustic verification pass: LRT <= 2.45, Anti-spoofing true)
    case = hub.run_post_repair_test(case_id, lrt_score=0.42, anti_spoofing_pass=True, snr_db=23.1)
    assert case["current_state"] == "POST_REPAIR_TEST"
    assert case["post_test_passed"] == 1

    # 10. State: ESCROW_RELEASED (Payout settlement)
    case = hub.release_escrow(case_id, tech_upi_id="tech.kumar@okhdfcbank", hmac_proof="PROOF_HMAC_SHA256")
    assert case["current_state"] == "ESCROW_RELEASED"

    # Audit timeline verification
    timeline = hub.get_case_timeline(case_id)
    assert len(timeline) == 10
    states = [t["to_state"] for t in timeline]
    assert states == HAPPY_STATES


def test_unhappy_flow_1_warranty_intercept(hub):
    case_id = f"CASE_WARRANTY_{int(time.time())}"
    hub.create_case(case_id, appliance_type="Refrigerator", oem_brand="Godrej", purchase_year=2025)
    case = hub.trigger_warranty_intercept(case_id, receipt_date="2025-11-10", oem_brand="Godrej", savings_inr=3200.0)
    assert case["current_state"] == "WARRANTY_INTERCEPT"
    timeline = hub.get_case_timeline(case_id)
    assert timeline[-1]["to_state"] == "WARRANTY_INTERCEPT"


def test_unhappy_flow_2_fake_repair_escrow_lock(hub):
    case_id = f"CASE_FAKE_REPAIR_{int(time.time())}"
    hub.create_case(case_id)
    hub.trigger_intake(case_id, "Screeching washer")
    hub.lock_escrow(case_id, "PL_ORD_FAKE", 1250.0)
    
    # Technician claims repair done, but LRT = 6.45 (> 2.45)
    case = hub.run_post_repair_test(case_id, lrt_score=6.45, anti_spoofing_pass=True, snr_db=21.0)
    assert case["current_state"] == "FAKE_REPAIR_ESCROW_LOCK"
    assert case["post_test_passed"] == 0


def test_unhappy_flow_3_scope_mismatch(hub):
    case_id = f"CASE_SCOPE_{int(time.time())}"
    hub.create_case(case_id)
    case = hub.trigger_scope_mismatch(
        case_id,
        reported_part="BEAR-6205-2RS",
        actual_needed="MOTOR-STATOR-FL",
        reason="Stator coil burn requires complete drive motor replacement"
    )
    assert case["current_state"] == "SCOPE_MISMATCH"


def test_unhappy_flow_4_snr_low_retry(hub):
    case_id = f"CASE_SNR_{int(time.time())}"
    hub.create_case(case_id)
    hub.trigger_intake(case_id, "Whistling kitchen noise test")
    
    # Record audio with low SNR (9.2 dB < 15.0 dB)
    case = hub.record_acoustic_capture(case_id, snr_db=9.2)
    assert case["current_state"] == "SNR_LOW_RETRY"
