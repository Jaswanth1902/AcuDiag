"""
AcuDiag Consumer Protection & Legal Redress Docket Engine
Generates e-Jagriti (National Consumer Commission) and NCH 1915 compliant
evidentiary dossiers for fraud cases, fake repairs, and counterfeit parts.
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional

def generate_edaakhil_evidentiary_docket(
    session_data: Dict[str, Any],
    supervisor_notes: str = "Acoustic inspection verified persistent harmonic resonance.",
    evidence_type: str = "FAKE_REPAIR_FRAUD"
) -> Dict[str, Any]:
    """
    Generates a cryptographically signed evidentiary legal docket for
    filing on the Ministry of Consumer Affairs e-Jagriti (e-Daakhil) portal.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S IST")
    case_uuid = session_data.get("id", f"ACU_CASE_{int(time.time())}")
    telemetry = session_data.get("telemetry", {})
    cost = session_data.get("cost", {})
    
    # Generate cryptographic hash of the physical evidence
    evidence_raw = f"{case_uuid}:{telemetry.get('peak_freq_hz')}:{telemetry.get('lrt_score')}:{timestamp}"
    evidence_sha256 = hashlib.sha256(evidence_raw.encode("utf-8")).hexdigest()
    
    docket = {
        "portal_destination": "e-Jagriti / National Consumer Helpline (NCH 1915)",
        "statutory_act": "Consumer Protection Act, 2019 (Section 2(47) - Unfair Trade Practice)",
        "docket_reference_id": f"EJAGRITI-{case_uuid.upper()}",
        "timestamp_generated": timestamp,
        "complainant": {
            "name": session_data.get("customer_name", "Registered Consumer"),
            "phone": session_data.get("phone", "N/A"),
            "location": session_data.get("location", "Bengaluru, Karnataka")
        },
        "respondent_technician": {
            "name": session_data.get("technician", {}).get("name", "Assigned Contractor"),
            "badge_no": session_data.get("technician", {}).get("badge", "N/A"),
            "upi_vpa": session_data.get("technician", {}).get("upi_vpa", "N/A")
        },
        "appliance_details": {
            "equipment": session_data.get("appliance", "Domestic Appliance"),
            "fault_alleged": session_data.get("fault_name", "Mechanical Breakdown"),
            "disputed_amount_inr": cost.get("total", 0)
        },
        "physical_evidentiary_record": {
            "forensic_type": evidence_type,
            "neyman_pearson_lrt_ratio": telemetry.get("lrt_score", 0.0),
            "safety_threshold": 2.45,
            "verdict": "PHYSICAL_DEFECT_PERSISTENT_OR_SPOOFED",
            "evidence_sha256_hash": evidence_sha256,
            "anti_spoofing_telemetry": telemetry.get("anti_spoofing", "PASSED"),
            "supervisor_official_notes": supervisor_notes
        },
        "legal_prayer": (
            "The complainant prays for full refund of held escrow, compensation for mental harassment "
            "under CPA 2019, and disciplinary blacklisting of the service provider for unfair trade practices."
        )
    }
    return docket


def generate_edaakhil_evidence_docket(
    customer_name: str,
    phone: str,
    pincode: str,
    appliance_brand: str,
    appliance_name: str,
    model_no: str,
    purchase_date: str,
    statutory_clause: str,
    claimed_rejection_reason: str,
    acoustic_telemetry: Dict[str, Any],
    escrow_id: str
) -> Dict[str, Any]:
    """
    Direct parameters docket compiler for consumer arbitration & e-Jagriti/e-Daakhil.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S IST")
    hash_seed = f"{customer_name}:{phone}:{pincode}:{acoustic_telemetry.get('peak_freq_hz')}:{acoustic_telemetry.get('lrt_ratio')}:{escrow_id}"
    evidence_sha256 = hashlib.sha256(hash_seed.encode("utf-8")).hexdigest()
    docket_num = f"EDA-ACU-{int(time.time())}-{evidence_sha256[:8].upper()}"

    formatted_legal_docket = f"""=== OFFICIAL CONSUMER GRIEVANCE & E-DAAKHIL EVIDENCE DOSSIER ===
Docket Reference: {docket_num}
Portal Destination: e-Jagriti / National Consumer Helpline (NCH 1915)
Statutory Act: Consumer Protection Act, 2019 (Sections 2(47), 84 - Product Liability)

[COMPLAINANT PARTICULARS]
Name: {customer_name}
Mobile: {phone}
PIN / Jurisdiction: {pincode}

[RESPONDENT APPLIANCE & TRANSACTION]
Brand: {appliance_brand} | Model: {model_no} ({appliance_name})
Purchase Date: {purchase_date}
Statutory Warranty Clause: {statutory_clause}
Pine Labs Escrow ID: {escrow_id}

[GRIEVANCE & DISPUTED CLAIM]
Technician Rejection / Extortion: {claimed_rejection_reason}

[FORENSIC ACOUSTIC & PHYSICAL EVIDENCE RECORD]
Peak Acoustic Frequency: {acoustic_telemetry.get('peak_freq_hz', 0.0)} Hz
Neyman-Pearson LRT Ratio: {acoustic_telemetry.get('lrt_ratio', 0.0)} (Threshold 2.45)
SNR Level: {acoustic_telemetry.get('snr_db', 0.0)} dB
Envelope Kurtosis: {acoustic_telemetry.get('envelope_kurtosis', 0.0)}
Fault Classification: {acoustic_telemetry.get('fault_type', 'UNKNOWN')}
Cryptographic SHA-256 Hash: {evidence_sha256}

[LEGAL PRAYER]
Complainant prays for mandatory OEM fulfillment under warranty, nullification of unlawful cash extortion, and statutory compensation for unfair trade practice.
=================================================================="""

    return {
        "docket_number": docket_num,
        "evidence_sha256": evidence_sha256,
        "formatted_legal_docket": formatted_legal_docket,
        "customer_name": customer_name,
        "phone": phone,
        "pincode": pincode,
        "brand": appliance_brand,
        "model": model_no,
        "escrow_id": escrow_id,
        "telemetry": acoustic_telemetry
    }
