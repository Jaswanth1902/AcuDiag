"""
AcuDiag 25-Scenario Synthetic & Empirical Seed Generator
Generates 25 comprehensive test dockets spanning:
- Healthy Baselines (5)
- Bearing Spall / Motor Faults (5)
- Drain Cavitation & Valve Leaks (4)
- Replay Spoofing Fraud Attacks (3)
- Low SNR Ambient Noise Rejections (3)
- Payment Chaos & Idempotency Timeouts (3)
- Fake Repair Withheld Escrow Audits (2)
"""

import json
from typing import List, Dict, Any

def generate_25_scenarios() -> List[Dict[str, Any]]:
    scenarios = []

    # 1-5: Healthy Baseline (Pass, Release Escrow)
    for i in range(1, 6):
        scenarios.append({
            "scenario_id": f"SCENARIO_HEALTHY_{i:02d}",
            "category": "healthy_baseline",
            "appliance": f"Whirlpool 7kg Front-Load WM #{i}",
            "symptom_text": "Customer reported mild noise after spin cycle, requested health check.",
            "acoustic_telemetry": {
                "snr_db": round(28.5 + i * 1.2, 1),
                "lrt_ratio": round(1.10 + i * 0.15, 2),
                "lrt_threshold": 2.45,
                "is_replay_spoof": False,
                "fault_type": "NONE (HEALTHY)",
                "verdict": "PASS_NORMAL_OPERATION"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "RELEASE_ESCROW_CAPTURE",
            "expected_confidence": 0.96
        })

    # 6-10: Bearing Spall / Mechanical Faults (Fail, Withhold Payout)
    for i in range(1, 6):
        scenarios.append({
            "scenario_id": f"SCENARIO_BEARING_{i:02d}",
            "category": "bearing_spall",
            "appliance": f"LG DirectDrive Inverter #{i}",
            "symptom_text": "High-pitched rhythmic metallic grinding during 1200 RPM spin cycle.",
            "acoustic_telemetry": {
                "snr_db": round(22.0 + i * 0.8, 1),
                "lrt_ratio": round(3.40 + i * 0.45, 2),
                "lrt_threshold": 2.45,
                "is_replay_spoof": False,
                "fault_type": "WM_BEARING_SPALL",
                "verdict": "FAIL_FAULT_DETECTED"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "DISPATCH_PARTS_WITHHOLD_PAYOUT",
            "expected_confidence": 0.95
        })

    # 11-14: Cavitation & Compressor Valve Leaks
    for i in range(1, 5):
        scenarios.append({
            "scenario_id": f"SCENARIO_PUMP_VALVE_{i:02d}",
            "category": "cavitation_or_valve",
            "appliance": f"Samsung EcoBubble / Daikin Inverter #{i}",
            "symptom_text": "Gurgling cavitation from drain manifold and high-frequency valve hiss.",
            "acoustic_telemetry": {
                "snr_db": round(19.5 + i * 1.1, 1),
                "lrt_ratio": round(2.85 + i * 0.35, 2),
                "lrt_threshold": 2.45,
                "is_replay_spoof": False,
                "fault_type": "PUMP_CAVITATION" if i % 2 == 1 else "COMPRESSOR_VALVE_LEAK",
                "verdict": "FAIL_FAULT_DETECTED"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "AUTO_ORDER_DRAIN_IMPELLER",
            "expected_confidence": 0.93
        })

    # 15-17: Speaker Replay Attack Spoofing (Fraud Detection)
    for i in range(1, 4):
        scenarios.append({
            "scenario_id": f"SCENARIO_SPOOF_FRAUD_{i:02d}",
            "category": "replay_attack",
            "appliance": f"Bosch Serie 6 WM #{i}",
            "symptom_text": "Technician submitted recorded WAV file from smartphone speaker playback.",
            "acoustic_telemetry": {
                "snr_db": round(25.0 + i * 2.0, 1),
                "low_freq_ratio": 0.032,
                "speaker_resonance_ratio": 0.115,
                "dac_spectral_flatness": 0.42,
                "is_replay_spoof": True,
                "fault_type": "REPLAY_SPOOF_ATTACK",
                "verdict": "REJECTED_REPLAY_ATTACK"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "TRIGGER_FRAUD_ALERT_LOCK_ESCROW",
            "expected_confidence": 0.99
        })

    # 18-20: Low SNR Ambient Noise (Quality Gate Rejection)
    for i in range(1, 4):
        scenarios.append({
            "scenario_id": f"SCENARIO_LOW_SNR_{i:02d}",
            "category": "low_snr_rejection",
            "appliance": f"IFB Senator Smart #{i}",
            "symptom_text": "Audio captured with loud construction drilling and television playing in room.",
            "acoustic_telemetry": {
                "snr_db": round(8.5 + i * 1.5, 1),
                "lrt_ratio": 0.0,
                "is_replay_spoof": False,
                "fault_type": "UNCLASSIFIED_HIGH_NOISE",
                "verdict": "REJECTED_SNR_TOO_LOW"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "REJECT_REQUEST_CLEAN_RECORDING",
            "expected_confidence": 0.92
        })

    # 21-23: Payment Chaos & Idempotency Timeouts
    for i, chaos in enumerate(["low_balance", "timeout_504", "invalid_vpa"], 1):
        scenarios.append({
            "scenario_id": f"SCENARIO_PAYMENT_CHAOS_{i:02d}",
            "category": "payment_chaos",
            "appliance": "Siemens iQ500 WM",
            "symptom_text": f"Escrow pre-auth gateway failure mode: {chaos}.",
            "chaos_mode": chaos,
            "idempotency_key": f"IDEM_{chaos.upper()}_KEY_{i:04d}",
            "escrow_state": "INITIATED",
            "expected_action": "SEND_WHATSAPP_FALLBACK_LINK" if chaos != "timeout_504" else "QUEUE_IDEMPOTENT_POLL",
            "expected_confidence": 0.94
        })

    # 24-25: Fake Repair Protocol (Post-Repair Acoustic Test Fails)
    for i in range(1, 3):
        scenarios.append({
            "scenario_id": f"SCENARIO_FAKE_REPAIR_{i:02d}",
            "category": "fake_repair_withhold",
            "appliance": f"Godrej Edge Digi #{i}",
            "symptom_text": "Technician marked repair complete, but post-repair acoustic scan still exhibits severe bearing rattle.",
            "acoustic_telemetry": {
                "snr_db": 24.2,
                "lrt_ratio": 3.88,
                "lrt_threshold": 2.45,
                "is_replay_spoof": False,
                "fault_type": "WM_BEARING_SPALL",
                "verdict": "FAIL_FAULT_DETECTED"
            },
            "escrow_state": "PRE_AUTH_LOCKED",
            "expected_action": "WITHHOLD_PAYOUT_SECONDARY_AUDIT",
            "expected_confidence": 0.97
        })

    return scenarios

if __name__ == "__main__":
    scenarios = generate_25_scenarios()
    print(f"Generated {len(scenarios)} diverse diagnostic scenarios.")
    out_file = r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\databank\25_DIAGNOSTIC_SCENARIOS.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2)
    print(f"Saved to {out_file}")
