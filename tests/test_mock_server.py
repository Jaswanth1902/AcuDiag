"""
AcuDiag Mock Server Test Suite: Stream B (3-Rail Connectors & Chaos Engine)
Tests all endpoints using FastAPI TestClient.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add databank to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "databank", "03_Mock_Server")))

from mock_server import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "no_rider" in data["chaos_modes_supported"]


def test_delhivery_pincode_lookup():
    # Valid Bengaluru PIN
    res = client.get("/c/api/pin-codes/json/?filter_codes=560059")
    assert res.status_code == 200
    data = res.json()
    assert data["is_serviceable"] is True
    assert data["delivery_codes"][0]["postal_code"]["sort_code"] == "BLR/KEN"

    # Direct path lookup
    res2 = client.get("/api/cmu/pincode/560059")
    assert res2.status_code == 200
    assert res2.json()["is_serviceable"] is True


def test_delhivery_forward_manifestation():
    payload = {
        "order_id": "TEST_ORD_101",
        "pin_code": "560059",
        "item_description": "Godrej Drum Bearing 6205-2RS",
        "consignee_name": "Jaswanth Reddy",
        "consignee_phone": "+919876543210"
    }
    res = client.post("/api/cmu/create.json", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["waybill"].startswith("WAYBILL_DEL_")
    assert data["status"] == "Manifested"


def test_delhivery_reverse_pickup():
    payload = {
        "pickup_time": "18:00:00",
        "pickup_date": "2026-10-01",
        "pickup_location": "RVCE Hostel Block B, Mysore Road",
        "expected_package_count": 1
    }
    res = client.post("/fm/request/new/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Scheduled"
    assert data["doorstep_qc_enabled"] is True


def test_pine_labs_plural_escrow_lifecycle():
    # 1. Create Pre-Auth Order
    order_payload = {
        "merchant_id": "MERCHANT_ACUDIAG_TEST",
        "customer_id": "CUST_TEST_01",
        "amount_in_paisa": 125000,
        "currency": "INR",
        "pre_auth": True,
        "appliance_ticket_id": "TKT_999"
    }
    res = client.post("/api/pay/v1/orders", json=order_payload)
    assert res.status_code == 200
    order_data = res.json()
    order_id = order_data["order_id"]
    assert order_data["status"] == "PRE_AUTH_LOCKED"
    assert order_data["amount"] == 1250.0

    # 2. Attempt capture with FAILED diagnostic test -> must be BLOCKED
    fail_capture = {
        "acoustic_token": "TOKEN_FAIL",
        "diagnostic_pass": False,
        "snr_db": 18.0
    }
    res_fail = client.put(f"/api/pay/v1/orders/{order_id}/capture", json=fail_capture)
    assert res_fail.status_code == 400
    assert "ESCROW_RELEASE_BLOCKED" in res_fail.json()["detail"]["error"]

    # 3. Capture with PASSED diagnostic test -> must SETTLE
    pass_capture = {
        "acoustic_token": "TOKEN_PASS_HASH",
        "diagnostic_pass": True,
        "snr_db": 24.5
    }
    res_pass = client.put(f"/api/pay/v1/orders/{order_id}/capture", json=pass_capture)
    assert res_pass.status_code == 200
    assert res_pass.json()["status"] == "CAPTURED_SETTLED"
    assert res_pass.json()["payout_recipient"] == "TECH_WALLET_CREDITED"


def test_chaos_modes():
    # 1. No Rider (503)
    res_no_rider = client.get("/c/api/pin-codes/json/?chaos=no_rider")
    assert res_no_rider.status_code == 503
    assert res_no_rider.json()["detail"]["error"] == "NO_RIDER_AVAILABLE"

    # 2. Insufficient Funds (402)
    order_payload = {
        "merchant_id": "M", "customer_id": "C", "amount_in_paisa": 100,
        "appliance_ticket_id": "T"
    }
    res_low_bal = client.post("/api/pay/v1/orders?chaos=low_balance", json=order_payload)
    assert res_low_bal.status_code == 402
    assert res_low_bal.json()["detail"]["error"] == "INSUFFICIENT_FUNDS"

    # 3. Malformed buffer
    res_malformed = client.get("/c/api/pin-codes/json/?chaos=malformed")
    assert res_malformed.status_code == 200
    assert b"<<MALFORMED" in res_malformed.content


def test_future_capabilities():
    # Capability 1: Delhivery GeoNaksha
    geo_payload = {
        "pincode": "560059",
        "address_text": "Behind temple, 2nd green gate, 3rd floor, RVCE",
        "gate_code_required": True
    }
    res_geo = client.post("/api/v1/delhivery/geonaksha/validate", json=geo_payload)
    assert res_geo.status_code == 200
    assert res_geo.json()["capability"] == "DELHIVERY_GEONAKSHA_3D_DROP"
    assert res_geo.json()["spatial_confidence"] == 0.98

    # Capability 2: Pine Labs Conditional Escrow Trigger
    trig_payload = {
        "order_id": "PL_TEST_ORD",
        "neyman_pearson_lrt": 0.35,
        "lrt_threshold": 2.45,
        "anti_spoofing_passed": True
    }
    res_trig = client.post("/api/v1/pinelabs/escrow/conditional-trigger", json=trig_payload)
    assert res_trig.status_code == 200
    assert res_trig.json()["decision"] == "RELEASE_FUNDS"

    # Capability 3: Gnani VAD Bypass Stream
    res_vad = client.get("/api/v1/gnani/acoustic/vad-bypass-stream")
    assert res_vad.status_code == 200
    assert res_vad.json()["noise_suppression"] == "DISABLED"


def test_direct_capture_and_refund():
    # 1. Create order
    order_payload = {
        "merchant_id": "MERCHANT_TOPLEVEL_TEST",
        "customer_id": "CUST_TOPLEVEL_01",
        "amount_in_paisa": 125000,
        "currency": "INR",
        "pre_auth": True,
        "appliance_ticket_id": "TKT_TOPLEVEL_01"
    }
    res_order = client.post("/api/pay/v1/orders", json=order_payload)
    assert res_order.status_code == 200
    order_id = res_order.json()["order_id"]

    # 2. Test direct /capture with diagnostic_pass=False -> 400
    fail_res = client.post("/capture", json={
        "order_id": order_id,
        "diagnostic_pass": False,
        "acoustic_token": "TOKEN_FAIL_TL"
    })
    assert fail_res.status_code == 400
    assert "ESCROW_RELEASE_BLOCKED" in fail_res.json()["detail"]["error"]

    # 3. Test direct /capture with diagnostic_pass=True -> 200
    pass_res = client.post("/capture", json={
        "order_id": order_id,
        "diagnostic_pass": True,
        "acoustic_token": "TOKEN_PASS_TL"
    })
    assert pass_res.status_code == 200
    assert pass_res.json()["status"] == "CAPTURED_SETTLED"

    # 4. Test direct /refund on another order
    order2 = client.post("/api/pay/v1/orders", json=order_payload).json()["order_id"]
    ref_res = client.post("/refund", json={
        "order_id": order2,
        "reason": "FAILED_POST_REPAIR_TEST"
    })
    assert ref_res.status_code == 200
    assert ref_res.json()["status"] == "REFUNDED_TO_CUSTOMER"


def test_fastmcp_and_connector_discovery():
    # 1. Discovery Manifest
    res = client.get("/mcp/manifest.json")
    assert res.status_code == 200
    data = res.json()
    assert data["name_for_model"] == "acudiag_3rail_connector"
    assert len(data["connectors"]) == 3
    connector_ids = [c["id"] for c in data["connectors"]]
    assert "delhivery_acudiag" in connector_ids
    assert "pinelabs_plural" in connector_ids
    assert "gnani_acudiag" in connector_ids

    # 2. FastMCP Tools Listing
    tools_res = client.get("/mcp/tools")
    assert tools_res.status_code == 200
    tool_names = [t["name"] for t in tools_res.json()["tools"]]
    assert "delhivery_pincode_lookup" in tool_names
    assert "delhivery_manifest_cmu" in tool_names
    assert "pinelabs_create_escrow_order" in tool_names
    assert "pinelabs_capture_escrow" in tool_names

    # 3. Alternative manifest path for AgenticOrg hosted-mcp
    res_hosted = client.get("/.well-known/oauth-protected-resource/api/v1/marketplace-surface/hosted-mcp")
    assert res_hosted.status_code == 200
    assert res_hosted.json()["name_for_model"] == "acudiag_3rail_connector"


def test_cmu_pincode_query_param():
    # Test query param /api/cmu/pincode?filter_codes=560059
    res = client.get("/api/cmu/pincode?filter_codes=560059")
    assert res.status_code == 200
    assert res.json()["is_serviceable"] is True
    assert res.json()["pincode"] == "560059"


def test_sessions_incident_desk():
    # 1. List Sessions Summary
    res = client.get("/api/sessions")
    assert res.status_code == 200
    sessions = res.json()["sessions"]
    assert len(sessions) >= 6
    session_ids = [s["id"] for s in sessions]
    assert "SES_1042_PRIYA" in session_ids
    assert "SES_1043_VIKRAM" in session_ids
    assert "SES_1045_RAJESH" in session_ids

    # 2. Detail for Priya (Happy Path)
    res_priya = client.get("/api/sessions/SES_1042_PRIYA")
    assert res_priya.status_code == 200
    data_p = res_priya.json()
    assert data_p["customer_name"] == "Priya Sharma"
    assert data_p["state"] == "VERIFIED_SETTLED"
    assert data_p["cost"]["total"] == 1250
    assert len(data_p["messages"]) >= 7

    # 3. Detail for Rajesh (Replay Spoof Fraud Alert)
    res_rajesh = client.get("/api/sessions/SES_1045_RAJESH")
    assert res_rajesh.status_code == 200
    data_r = res_rajesh.json()
    assert data_r["alarm"] == "REPLAY_SPOOF_BLOCKED"
    assert "DAC" in data_r["alarm_text"]

    # 4. Interactive user message
    res_msg = client.post("/api/sessions/SES_1042_PRIYA/message", json={"text": "Thank you AcuDiag!", "sender": "user"})
    assert res_msg.status_code == 200
    assert res_msg.json()["status"] == "ok"
    updated = res_msg.json()["session"]
    assert any("Thank you AcuDiag!" in m.get("text", "") for m in updated["messages"])

    # 5. Technician channel message
    res_tech = client.post("/api/sessions/SES_1042_PRIYA/message", json={"text": "Old scrap core returned to Delhivery.", "sender": "tech", "channel": "technician"})
    assert res_tech.status_code == 200
    updated_tech = res_tech.json()["session"]
    assert any("Old scrap core returned" in m.get("text", "") for m in updated_tech["messages_technician"])

    # 6. Supervisor Override execution
    res_sup = client.post("/api/sessions/SES_1045_RAJESH/supervisor-override", json={"action": "UPHOLD_FRAUD_LOCK", "reason": "DAC audio playback confirmed."})
    assert res_sup.status_code == 200
    sup_data = res_sup.json()["session"]
    assert sup_data["state"] == "SUPERVISOR_UPHELD_FRAUD"
    assert sup_data["supervisor_docket"]["status"] == "UPHELD_FRAUD_LOCK"



