"""
AcuDiag Enterprise Mock Server for The Ken Round 3 Build Track
Implements exact production schemas for Delhivery, Pine Labs Escrow, and the 3 Future Capabilities.
Features dynamic Chaos Injection (no rider, low balance, timeout, malformed replies)
as mandated by Adhavan RK and The Ken jury.
"""

import os
import sys
from pathlib import Path

proj_root = Path(__file__).resolve().parent.parent.parent
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

import time
import uuid
import hmac
import hashlib
from typing import Dict, Optional, Any
from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    import sessions_store
except ImportError:
    import importlib.util
    _sessions_path = os.path.join(os.path.dirname(__file__), "sessions_store.py")
    _spec = importlib.util.spec_from_file_location("sessions_store", _sessions_path)
    sessions_store = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(sessions_store)

PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "public"))

app = FastAPI(
    title="AcuDiag 3-Rail Mock Server",
    description="Official Mock Connector Server for Delhivery, Pine Labs, and Future Capabilities",
    version="1.0.0"
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: https://fonts.googleapis.com https://fonts.gstatic.com; "
        "font-src 'self' data: https://fonts.gstatic.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "connect-src 'self' *"
    )
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/", response_class=HTMLResponse)
@app.get("/cockpit", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def serve_cockpit_hud():
    index_file = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file, media_type="text/html")
    return HTMLResponse("<h1>AcuDiag Mock Server Live</h1><p>Index HTML not found</p>", status_code=200)

if os.path.exists(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

# In-memory database of shipments, orders, and logs
DATABASE = {
    "shipments": {},
    "orders": {},
    "audit_logs": []
}

# --- CHAOS INJECTION MIDDLEWARE HELPER ---
def check_chaos(chaos_type: Optional[str]):
    if not chaos_type:
        return
    chaos = chaos_type.lower()
    if chaos == "no_rider":
        raise HTTPException(status_code=503, detail={"error": "NO_RIDER_AVAILABLE", "message": "No logistics rider or field technician available in this PIN code cluster."})
    elif chaos == "low_balance":
        raise HTTPException(status_code=402, detail={"error": "INSUFFICIENT_FUNDS", "message": "Pre-auth authorization declined: Insufficient customer card balance."})
    elif chaos == "timeout":
        time.sleep(4.0)
        raise HTTPException(status_code=504, detail={"error": "GATEWAY_TIMEOUT", "message": "Upstream bank switch timed out."})
    elif chaos == "malformed":
        return Response(content="<<MALFORMED_NON_JSON_CORRUPT_BUFFER>>", media_type="text/plain")


# ==============================================================================
# RAIL 1: DELHIVERY OFFICIAL ENDPOINTS (Same request & response fields as docs)
# ==============================================================================

@app.get("/api/cmu/pincode")
@app.get("/api/cmu/pincode/{pincode}")
@app.get("/c/api/pin-codes/json/")
@app.get("/api/pin-codes/json/")
async def check_pincode(pincode: Optional[str] = None, filter_codes: Optional[str] = Query(None), chaos: Optional[str] = Query(None)):
    """Delhivery PIN Code Serviceability & TAT Lookup (Supports both path and query filters)"""
    res = check_chaos(chaos)
    if res: return res

    target_pin = filter_codes if filter_codes else (pincode if pincode else "560059")
    # 560059 is Bengaluru / RVCE hub
    is_serviceable = (target_pin.startswith("560") or target_pin.startswith("110") or target_pin.startswith("400"))
    
    return {
        "delivery_codes": [
            {
                "postal_code": {
                    "pin": int(target_pin) if target_pin.isdigit() else 560059,
                    "is_serviceable": is_serviceable,
                    "prepaid": "Y",
                    "cod": "N",
                    "pickup": "Y",
                    "repl": "Y",
                    "cash": "N",
                    "sort_code": "BLR/KEN" if target_pin.startswith("560") else "DEL/CENTRAL",
                    "hub_name": "BLR_KENGERI_GW" if target_pin.startswith("560") else "DEL_CENTRAL_GW",
                    "tat_hours": 4 if target_pin.startswith("560") else 24
                }
            }
        ],
        "pincode": target_pin,
        "is_serviceable": is_serviceable
    }

class DelhiveryDispatchPayload(BaseModel):
    order_id: str
    pin_code: str
    item_description: str
    consignee_name: str
    consignee_phone: str

@app.post("/api/cmu/create")
@app.post("/api/cmu/create.json")
async def create_shipment(payload: DelhiveryDispatchPayload, chaos: Optional[str] = Query(None)):
    """Delhivery Surface Forward & Reverse Waybill Creation"""
    res = check_chaos(chaos)
    if res: return res

    # Idempotency check
    for existing_wb, ship_data in DATABASE["shipments"].items():
        if ship_data.get("order_id") == payload.order_id:
            return {
                "success": True,
                "packages": [{
                    "status": "Success",
                    "client": "ACUDIAG_TECH",
                    "sort_code": "BLR/KEN",
                    "waybill": existing_wb,
                    "refnum": payload.order_id,
                    "serviceable": True
                }],
                "waybill": existing_wb,
                "status": "Manifested",
                "pickup_scheduled_time": "Within 2 Hours",
                "tracking_url": f"https://delhivery.mock/track/{existing_wb}",
                "idempotent": True
            }

    waybill = f"WAYBILL_DEL_{uuid.uuid4().hex[:10].upper()}"
    record = {
        "waybill": waybill,
        "order_id": payload.order_id,
        "pin_code": payload.pin_code,
        "item": payload.item_description,
        "status": "MANIFESTED",
        "timestamp": time.time()
    }
    DATABASE["shipments"][waybill] = record
    return {
        "success": True,
        "packages": [
            {
                "status": "Success",
                "client": "ACUDIAG_TECH",
                "sort_code": "BLR/KEN",
                "waybill": waybill,
                "refnum": payload.order_id,
                "serviceable": True
            }
        ],
        "waybill": waybill,
        "status": "Manifested",
        "pickup_scheduled_time": "Within 2 Hours",
        "tracking_url": f"https://delhivery.mock/track/{waybill}"
    }

class ReversePickupRequest(BaseModel):
    pickup_time: str = "18:00:00"
    pickup_date: str = "2026-10-01"
    pickup_location: str
    expected_package_count: int = 1
    waybill: Optional[str] = None

@app.post("/fm/request/new/")
@app.post("/api/pickup-request/create")
async def create_reverse_pickup(payload: ReversePickupRequest, chaos: Optional[str] = Query(None)):
    """Delhivery Reverse Pickup Request with Doorstep QC Checklist"""
    res = check_chaos(chaos)
    if res: return res

    pr_id = int(time.time() * 1000) % 10000000
    return {
        "pr_id": pr_id,
        "pickup_date": payload.pickup_date,
        "pickup_time": payload.pickup_time,
        "pickup_location": payload.pickup_location,
        "status": "Scheduled",
        "rider_assigned": "Ramesh K (+919845012345)",
        "doorstep_qc_enabled": True
    }


@app.get("/api/v1/packages/json/")
async def track_shipment(waybill: str, chaos: Optional[str] = Query(None)):
    """Delhivery Live Tracking Status"""
    res = check_chaos(chaos)
    if res: return res

    if waybill not in DATABASE["shipments"]:
        # Return realistic default in-transit status
        return {
            "ShipmentData": [{
                "Shipment": {
                    "AWB": waybill,
                    "Status": {"Status": "In-Transit", "StatusLocation": "Bengaluru Hub", "Instructions": "Out for delivery to technician"}
                }
            }]
        }
    return {
        "ShipmentData": [{
            "Shipment": {
                "AWB": waybill,
                "Status": {"Status": DATABASE["shipments"][waybill]["status"], "StatusLocation": "Kengeri Delivery Center"}
            }
        }]
    }


# ==============================================================================
# RAIL 2: PINE LABS PLURAL ESCROW ENDPOINTS
# ==============================================================================

class PineLabsOrderPayload(BaseModel):
    merchant_id: str
    customer_id: str
    amount_in_paisa: int
    currency: str = "INR"
    pre_auth: bool = True
    appliance_ticket_id: str

@app.post("/api/pay/v1/orders")
async def create_plural_order(payload: PineLabsOrderPayload, chaos: Optional[str] = Query(None)):
    """Pine Labs Plural Pre-Auth Order Creation (Locks Funds in Escrow)"""
    res = check_chaos(chaos)
    if res: return res

    # Idempotency check: if order already exists for this appliance ticket, return existing
    for existing_id, ord_data in DATABASE["orders"].items():
        if ord_data.get("ticket_id") == payload.appliance_ticket_id:
            return {
                "order_id": existing_id,
                "status": ord_data["status"],
                "amount": ord_data["amount_in_paisa"] / 100.0,
                "escrow_hold_state": "ACTIVE_HOLD" if ord_data["status"] == "PRE_AUTH_LOCKED" else ord_data["status"],
                "message": "Idempotent response: Funds already held in escrow.",
                "idempotent": True
            }

    order_id = f"PL_ORD_{uuid.uuid4().hex[:8].upper()}"
    order_record = {
        "order_id": order_id,
        "amount_in_paisa": payload.amount_in_paisa,
        "currency": payload.currency,
        "status": "PRE_AUTH_LOCKED",
        "pre_auth": payload.pre_auth,
        "ticket_id": payload.appliance_ticket_id,
        "locked_at": time.time()
    }
    DATABASE["orders"][order_id] = order_record
    return {
        "order_id": order_id,
        "status": "PRE_AUTH_LOCKED",
        "amount": payload.amount_in_paisa / 100.0,
        "escrow_hold_state": "ACTIVE_HOLD",
        "message": "Funds successfully held in escrow. Requires acoustic Neyman-Pearson PASS for release."
    }

class CaptureRequest(BaseModel):
    acoustic_token: str
    diagnostic_pass: bool
    snr_db: float

@app.put("/api/pay/v1/orders/{order_id}/capture")
@app.post("/api/pay/v1/orders/{order_id}/capture")
async def capture_escrow_order(order_id: str, payload: CaptureRequest, chaos: Optional[str] = Query(None)):
    """Conditional Release Trigger: Releases Escrow ONLY on verified diagnostic pass"""
    res = check_chaos(chaos)
    if res: return res

    if not payload.diagnostic_pass:
        raise HTTPException(
            status_code=400,
            detail={"error": "ESCROW_RELEASE_BLOCKED", "message": "Diagnostic acoustic test failed. Technician cannot be paid for an incomplete repair."}
        )
    
    if order_id not in DATABASE["orders"]:
        raise HTTPException(status_code=404, detail="Order not found")

    DATABASE["orders"][order_id]["status"] = "CAPTURED_SETTLED"
    DATABASE["orders"][order_id]["captured_at"] = time.time()
    return {
        "order_id": order_id,
        "status": "CAPTURED_SETTLED",
        "settled_amount": DATABASE["orders"][order_id]["amount_in_paisa"] / 100.0,
        "acoustic_token_verified": payload.acoustic_token,
        "payout_recipient": "TECH_WALLET_CREDITED",
        "timestamp": time.time()
    }

class DirectCapturePayload(BaseModel):
    order_id: str
    acoustic_token: Optional[str] = "ACU_PASS_SHA256_DEFAULT"
    diagnostic_pass: bool = True
    snr_db: Optional[float] = 22.0

@app.post("/capture")
@app.put("/capture")
async def direct_capture(payload: DirectCapturePayload, chaos: Optional[str] = Query(None)):
    """Top-Level Escrow Capture Endpoint"""
    req = CaptureRequest(
        acoustic_token=payload.acoustic_token or "ACU_PASS_SHA256_DEFAULT",
        diagnostic_pass=payload.diagnostic_pass,
        snr_db=payload.snr_db or 22.0
    )
    return await capture_escrow_order(payload.order_id, req, chaos=chaos)

@app.post("/api/pay/v1/orders/{order_id}/refund")
async def refund_escrow_order(order_id: str, reason: str = "FAILED_POST_REPAIR_TEST"):
    """Dispute Resolution: Instant Escrow Refund to Customer"""
    if order_id not in DATABASE["orders"]:
        raise HTTPException(status_code=404, detail="Order not found")
    DATABASE["orders"][order_id]["status"] = "REFUNDED"
    return {
        "order_id": order_id,
        "status": "REFUNDED_TO_CUSTOMER",
        "reason": reason,
        "refund_timestamp": time.time()
    }

class DirectRefundPayload(BaseModel):
    order_id: str
    reason: Optional[str] = "FAILED_POST_REPAIR_TEST"

@app.post("/refund")
async def direct_refund(payload: DirectRefundPayload, chaos: Optional[str] = Query(None)):
    """Top-Level Escrow Refund Endpoint"""
    res = check_chaos(chaos)
    if res: return res
    return await refund_escrow_order(payload.order_id, reason=payload.reason or "FAILED_POST_REPAIR_TEST")



# ==============================================================================
# RAIL 3: UP TO 3 CAPABILITIES PARTNERS DON'T OFFER TODAY (Mandated by Ken)
# ==============================================================================

# Capability 1: Delhivery Origin-Auth Routing & GeoNaksha Hyper-Local Drop
class OriginAuthPayload(BaseModel):
    oem_gstin: str
    part_serial_number: str
    destination_pin: str

@app.post("/api/v1/delhivery/origin-auth/route")
async def origin_auth_routing(payload: OriginAuthPayload):
    """
    Capability 1 (Delhivery): Verifies GSTIN origin to guarantee 100% genuine OEM parts
    and prevent counterfeit imitation parts from entering technician dispatch.
    """
    is_valid_oem = payload.oem_gstin.startswith("29AAAC") or payload.oem_gstin.startswith("07AAAC")
    return {
        "capability": "DELHIVERY_ORIGIN_AUTH_ROUTING",
        "is_genuine_oem": is_valid_oem,
        "oem_brand": "Samsung Electronics India" if is_valid_oem else "UNVERIFIED_THIRD_PARTY",
        "quarantine_flag": not is_valid_oem,
        "authorized_part_waybill": f"OEM_AUTH_{uuid.uuid4().hex[:8].upper()}" if is_valid_oem else None
    }

class GeoNakshaPayload(BaseModel):
    pincode: str
    address_text: str
    gate_code_required: bool = True

@app.post("/api/v1/delhivery/geonaksha/validate")
async def geonaksha_validate(payload: GeoNakshaPayload):
    """
    Capability 1 Alias (Delhivery GeoNaksha): 3D Hyper-Local Spatial Coordinate Validation
    resolving gated community tower, floor, and security gate drop coordinates.
    """
    return {
        "capability": "DELHIVERY_GEONAKSHA_3D_DROP",
        "pincode": payload.pincode,
        "spatial_confidence": 0.98,
        "building_cluster": "RVCE_HOSTEL_BLOCK_B",
        "gate_clearance_token": f"GATE_OTP_{uuid.uuid4().hex[:6].upper()}",
        "precise_lat_lng": [12.9237, 77.4987]
    }


# Capability 2: Pine Labs Cryptographic Acoustic Release Trigger
class AcousticEscrowTriggerPayload(BaseModel):
    order_id: str
    neyman_pearson_lrt: float
    lrt_threshold: float
    anti_spoofing_passed: bool

@app.post("/api/v1/pinelabs/escrow/conditional-trigger")
async def acoustic_conditional_trigger(payload: AcousticEscrowTriggerPayload):
    """
    Capability 2 (Pine Labs): Direct sub-millisecond cryptographic hardware trigger
    binding acoustic test pass to escrow release without human middleman.
    """
    authorized = (payload.neyman_pearson_lrt <= payload.lrt_threshold) and payload.anti_spoofing_passed
    return {
        "capability": "PINE_LABS_CONDITIONAL_ACOUSTIC_RELEASE",
        "authorized": authorized,
        "decision": "RELEASE_FUNDS" if authorized else "HOLD_ESCROW_ALERT_FRAUD",
        "crypto_signature": hashlib.sha256(f"{payload.order_id}:{payload.neyman_pearson_lrt}".encode()).hexdigest()
    }

# Capability 3: Gnani Unfiltered VAD Diagnostic Stream
@app.get("/api/v1/gnani/acoustic/vad-bypass-stream")
async def gnani_vad_bypass():
    """
    Capability 3 (Gnani): Unfiltered broadband acoustic pass-through bypassing conversational
    speech VAD noise-suppressors during machine diagnostics.
    """
    return {
        "capability": "GNANI_VAD_BYPASS_STREAM",
        "noise_suppression": "DISABLED",
        "frequency_bandwidth": "20Hz - 8000Hz (Full Acoustic Spectrum)",
        "intended_use": "Appliance Mechanical Vibration Diagnostics"
    }


# ==============================================================================
# RAIL 4: GNANI OFFICIAL SPEECH ENDPOINTS (Exact api.vachana.ai signatures)
# ==============================================================================

@app.post("/stt/v3")
async def gnani_stt_transcribe(request: Request, chaos: Optional[str] = Query(None)):
    """Gnani Prisma v2.5 Speech-to-Text Transcription Endpoint (Exact api.vachana.ai/stt/v3)"""
    res = check_chaos(chaos)
    if res: return res

    # Handle both multipart and json
    form = {}
    try:
        form = await request.form()
    except Exception:
        pass
    
    lang = form.get("language_code", "hi-IN")
    req_id = f"req_gnani_{uuid.uuid4().hex[:10]}"
    
    # Return grounded appliance fault transcript
    transcript = "मेरी गोदरेज वॉशिंग मशीन स्पिन साइकिल में बहुत तेज़ खड़-खड़ आवाज़ कर रही है।"
    if "en" in lang:
        transcript = "My Godrej washing machine is making a loud rattling noise during the spin cycle."
    elif "kn" in lang:
        transcript = "ನನ್ನ ಗೋದ್ರೇಜ್ ವಾಷಿಂಗ್ ಮೆಷಿನ್ ಸ್ಪಿನ್ ಸೈಕಲ್‌ನಲ್ಲಿ ಭಾರಿ ಶಬ್ದ ಮಾಡುತ್ತಿದೆ."

    return {
        "success": True,
        "request_id": req_id,
        "timestamp": time.strftime("%Y%m%d_%H%M%S.000"),
        "transcript": transcript,
        "language_code": lang,
        "model": "gnani-prisma-v2.5"
    }

class GnaniTTSPayload(BaseModel):
    text: str
    voice: Optional[str] = "Nalini"
    model: Optional[str] = "timbre-v2.5"
    language: Optional[str] = "hi-IN"
    speed: Optional[float] = 1.0
    audio_config: Optional[Dict[str, Any]] = None

@app.post("/api/v1/tts/inference")
async def gnani_tts_synthesize(payload: GnaniTTSPayload, chaos: Optional[str] = Query(None)):
    """Gnani Timbre v2.5 Text-to-Speech Synthesis Endpoint (Exact api.vachana.ai/api/v1/tts/inference)"""
    res = check_chaos(chaos)
    if res: return res

    # Return synthetic WAV header + PCM buffer
    sample_rate = 24000
    duration_sec = 2.0
    num_samples = int(sample_rate * duration_sec)
    header = b"RIFF" + (36 + num_samples * 2).to_bytes(4, "little") + b"WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00" + sample_rate.to_bytes(4, "little") + (sample_rate * 2).to_bytes(4, "little") + b"\x02\x00\x10\x00data" + (num_samples * 2).to_bytes(4, "little")
    pcm_data = b"\x00\x00" * num_samples
    
    return Response(content=header + pcm_data, media_type="audio/wav")


# ==============================================================================
# AUDIT & SYSTEM STATUS
# ==============================================================================
@app.get("/health")
async def health():
    return {
        "status": "HEALTHY",
        "active_shipments": len(DATABASE["shipments"]),
        "active_escrow_orders": len(DATABASE["orders"]),
        "chaos_modes_supported": ["no_rider", "low_balance", "timeout", "malformed"]
    }


# ==============================================================================
# REAL USER COMMS: WHATSAPP WEBHOOK ENDPOINT (Twilio / Meta Format)
# ==============================================================================
@app.api_route("/api/whatsapp/webhook", methods=["GET", "POST"])
async def whatsapp_webhook(request: Request):
    """
    Unified Real User Comms: WhatsApp Webhook Endpoint (Twilio & Meta/Baileys formats).
    Dispatches to real-time DSP, Gnani STT, Anti-Spoofing, and Pine Labs AgenticOrg.
    Synchronizes every message with sessions_store for live Cockpit HUD mirroring.
    """
    from src.whatsapp_agentic_bridge import whatsapp_webhook as agentic_whatsapp_webhook
    return await agentic_whatsapp_webhook(request)

# ==============================================================================
# ENTERPRISE MULTI-SESSION INCIDENT DESK ENDPOINTS
# ==============================================================================
@app.get("/api/sessions")
async def list_sessions():
    """Returns summary list of all active customer sessions for the Incident Desk queue."""
    return {"sessions": sessions_store.get_all_sessions_summary()}

@app.get("/api/sessions/{session_id}")
async def get_session_detail(session_id: str):
    """Returns complete session envelope, audit trail, and raw telemetry."""
    session = sessions_store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

class MessagePayload(BaseModel):
    text: str
    sender: Optional[str] = "user"
    channel: Optional[str] = "customer"

@app.post("/api/sessions/{session_id}/message")
async def post_session_message(session_id: str, payload: MessagePayload):
    """Appends customer or technician message, runs reactive agent loop, and updates state."""
    session = sessions_store.add_user_message(session_id, payload.text, payload.sender, payload.channel)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "ok", "session": session}

class SupervisorOverridePayload(BaseModel):
    action: str
    reason: Optional[str] = ""

@app.post("/api/sessions/{session_id}/supervisor-override")
async def supervisor_override(session_id: str, payload: SupervisorOverridePayload):
    """Executes Human-in-the-Loop Quality Supervisor override and logs to central ledger."""
    session = sessions_store.execute_supervisor_override(session_id, payload.action, payload.reason)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "ok", "session": session}

@app.post("/api/sessions/reset")
async def reset_sessions():
    """Resets all working sessions to clean initial baseline."""
    sessions_store.reset_all_sessions()
    return {"status": "ok", "message": "All sessions reset to baseline"}

# ==============================================================================
# FASTMCP & AGENTICORG REST CONNECTOR DISCOVERY
# ==============================================================================
@app.get("/mcp/manifest.json")
@app.get("/.well-known/oauth-protected-resource/api/v1/marketplace-surface/hosted-mcp")
@app.get("/connector/manifest")
async def mcp_connector_manifest():
    """AgenticOrg Auto-Discovery Manifest for AcuDiag 3-Rail Connectors"""
    return {
        "schema_version": "v1",
        "name_for_model": "acudiag_3rail_connector",
        "name_for_human": "AcuDiag 3-Rail Orchestration Hub",
        "description_for_model": "Unified API connector linking Gnani.ai Indic Voice, Delhivery CMU Logistics, and Pine Labs Plural Escrow for autonomous appliance diagnostic and repair lifecycle.",
        "description_for_human": "AcuDiag Enterprise Connectors for The Ken Round 3.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": "/openapi.json"
        },
        "connectors": [
            {
                "id": "delhivery_acudiag",
                "name": "Delhivery Express & CMU Logistics",
                "description": "Forward OEM part manifestation, reverse pickup QC, and pincode TAT verification",
                "endpoints": ["/api/cmu/pincode", "/api/cmu/create.json", "/fm/request/new/", "/api/v1/packages/json/"]
            },
            {
                "id": "pinelabs_plural",
                "name": "Pine Labs Plural Escrow",
                "description": "Pre-auth escrow hold, conditional post-repair capture, and automated dispute refund",
                "endpoints": ["/api/pay/v1/orders", "/api/pay/v1/orders/{order_id}/capture", "/capture", "/refund"]
            },
            {
                "id": "gnani_acudiag",
                "name": "Gnani.ai Indic Speech Engine",
                "description": "Prisma v2.5 Speech-to-Text and Timbre v2.5 Text-to-Speech with Hinglish support",
                "endpoints": ["/stt/v3", "/api/v1/tts/inference"]
            }
        ],
        "tools": [
            {
                "name": "delhivery_pincode_lookup",
                "description": "Check logistics serviceability and TAT for destination pincode",
                "inputSchema": {
                    "type": "object",
                    "properties": {"pincode": {"type": "string"}},
                    "required": ["pincode"]
                }
            },
            {
                "name": "delhivery_manifest_cmu",
                "description": "Manifest OEM part dispatch via Delhivery Express surface network",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "pin_code": {"type": "string"},
                        "item_description": {"type": "string"},
                        "consignee_name": {"type": "string"},
                        "consignee_phone": {"type": "string"}
                    },
                    "required": ["order_id", "pin_code", "item_description", "consignee_name", "consignee_phone"]
                }
            },
            {
                "name": "delhivery_reverse_pickup",
                "description": "Create doorstep reverse pickup request for defective scrap component",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pickup_location": {"type": "string"},
                        "waybill": {"type": "string"}
                    },
                    "required": ["pickup_location"]
                }
            },
            {
                "name": "pinelabs_create_escrow_order",
                "description": "Pre-authorize and lock repair funds in Pine Labs Plural escrow",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "merchant_id": {"type": "string"},
                        "customer_id": {"type": "string"},
                        "amount_in_paisa": {"type": "integer"},
                        "appliance_ticket_id": {"type": "string"}
                    },
                    "required": ["merchant_id", "customer_id", "amount_in_paisa", "appliance_ticket_id"]
                }
            },
            {
                "name": "pinelabs_capture_escrow",
                "description": "Release held escrow funds upon cryptographic acoustic diagnostic pass",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "acoustic_token": {"type": "string"},
                        "diagnostic_pass": {"type": "boolean"},
                        "snr_db": {"type": "number"}
                    },
                    "required": ["order_id", "diagnostic_pass"]
                }
            }
        ]
    }

@app.get("/mcp/tools")
@app.get("/api/v1/mcp/tools")
async def list_mcp_tools():
    """FastMCP Tool Listing Endpoint"""
    manifest = await mcp_connector_manifest()
    return {"tools": manifest["tools"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


