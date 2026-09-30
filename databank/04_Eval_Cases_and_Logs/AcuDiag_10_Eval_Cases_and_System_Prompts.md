# 🧪 AcuDiag: 10 Adversarial Evaluation Cases, System Prompts & Run Logs

> **Competition**: The Ken Case-Build 2026: "The Great Rewiring"  
> **Submission Phase**: Build Round Deliverables (Part 2)  
> **Agent Name**: AcuDiag Orchestrator (Acoustic Diagnostics & Autonomous Escrow Agent)

---

## 1. The 10 Adversarial Eval Cases (Testing Matrix)

| # | Evaluation Case Scenario | Input Trigger | Unexpected / Adversarial Condition | Expected Agent Autonomous Behavior |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Heavy Hinglish Code-Switching** | Voice audio in Gnani | *"Bhai washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai, pani bhi leak ho raha hai"* | Correctly parses mixed linguistic tokens; isolates symptoms (`drum noise` + `water leakage`); does not crash or request English repetition. |
| **2** | **Technician Audio Replay Fraud (Spoofing)** | Diagnostic capture in WebAudio | Technician plays a recorded healthy washing machine `.wav` file through their smartphone speaker | Anti-spoofing engine flags lack of low-frequency physical rumble (<120Hz) and DAC quantization peak; rejects test with `REJECTED_REPLAY_ATTACK`; alerts customer. |
| **3** | **High Ambient Kitchen Noise (Low SNR)** | Diagnostic capture in WebAudio | Customer records while pressure cooker is whistling and television is loud (SNR = 8.2 dB) | Gating catches SNR < 15 dB; refuses to pass/fail repair; instructs user via Gnani voice to close kitchen doors and re-record. |
| **4** | **Delhivery Rider Cancellation / No Rider** | Delivery dispatch call | Delhivery mock connector returns `503 NO_RIDER_AVAILABLE` | Agent autonomously retries nearest peripheral logistics micro-hub; if unserviceable within 30 min, extends appointment and sends SMS apology. |
| **5** | **Pre-Auth Escrow Card Decline** | Pine Labs pre-auth API | Pine Labs returns `402 INSUFFICIENT_FUNDS` | Agent pauses technician dispatch; notifies user on WhatsApp with direct UPI payment link to authorize escrow hold before rider departs. |
| **6** | **Incomplete / Fake Repair by Technician** | Post-repair acoustic test | Technician claims "I tightened the bearing", but acoustic capture still exhibits 1,450 Hz BPFO harmonic resonance | Neyman-Pearson LRT exceeds threshold ($\Lambda(x) = 8.42 > 2.45$); rejects capture; **locks Pine Labs escrow hold**; schedules free replacement technician. |
| **7** | **Dead-On-Arrival (DOA) Replacement Part** | Unboxing inspection | New pump installed by technician fails immediately with cavitation screech | Agent triggers Delhivery Surface Reverse Pickup (`POST /api/p/edit`); flags part serial number in warranty ledger; orders replacement without charging customer. |
| **8** | **Active OEM Warranty Intercept** | Invoice upload OCR | User uploads purchase receipt showing appliance bought 8 months ago (Standard 2-year warranty) | Agent immediately aborts paid escrow flow; generates free OEM warranty docket; forwards to official manufacturer service bridge (saves user ₹3,200). |
| **9** | **User Refuses / Aborts Post-Repair Test** | WebAudio prompt | User taps "I don't want to test, let the technician go" | Agent enforces safety protocol: informs user that unverified release forfeits 90-day dispute guarantee; holds escrow for 24-hour auto-dispute cooling period. |
| **10** | **Upstream Bank Network Timeout** | Pine Labs capture call | Pine Labs Plural API times out with `504 GATEWAY_TIMEOUT` | Agent logs idempotent transaction token; does not duplicate charges; enters async webhook polling state until bank switch confirmation arrives. |

---

## 2. System Prompt Evolution (Versions 1.0 $\rightarrow$ 2.0 $\rightarrow$ 3.0)

### Version 1.0 (Initial Scaffold — Vulnerable to Premature Release)
```text
You are AcuDiag, an automated appliance diagnostic agent.
Listen to the user's problem via voice, find what is wrong, and book a technician.
When the technician arrives, hold payments and release payment after the machine is fixed.
```
* **Failure in Round 1 Testing**: Agent released escrow whenever the technician verbally stated "repair is done," completely failing Eval Case 6 (Fake Repair).

### Version 2.0 (Added Rail Gating — Failed on Ambient Noise)
```text
You are AcuDiag, an autonomous appliance diagnostic and escrow orchestrator.
1. Connect to Gnani for voice intake.
2. Call Pine Labs POST /api/pay/v1/orders with pre_auth: true before dispatching Delhivery parts.
3. Only release Pine Labs escrow when the post-repair diagnostic returns PASS.
```
* **Failure in Round 2 Testing**: In Eval Case 3 (pressure cooker whistling), the ambient noise corrupted the audio spectrum, causing a healthy repair to be falsely rejected as broken.

### Version 3.0 (Final Production System Prompt — Battle-Tested)
```text
You are AcuDiag, the Autonomous Appliance Reliability & Escrow Orchestrator.
You operate under zero-trust physical verification across Gnani (Voice), Pine Labs (Payments), and Delhivery (Logistics).

STRICT INVARIANTS:
1. VOICE INTAKE: Process user voice via Gnani STT. Parse Hinglish and regional code-switching. Isolate appliance symptoms into [SUBSYSTEM_FAULT].
2. ESCROW GATE: Never dispatch a technician or parts until Pine Labs confirms PRE_AUTH_LOCKED. If declined (402), send WhatsApp payment link and halt.
3. NOISE GATING: Before evaluating acoustic diagnostics, check SNR. If SNR < 15 dB, REJECT test with instruction: "Ambient noise too high, please close doors and re-record."
4. ANTI-SPOOFING: Inspect phase variance and low-frequency rumble (<120Hz). If audio originates from a speaker rather than physical machine vibration, trigger REJECTED_REPLAY_ATTACK and alert customer.
5. ESCROW RELEASE CONDITION: Call Pine Labs capture ONLY when Neyman-Pearson LRT <= 2.45 AND Anti-Spoofing is TRUE.
6. FAKE REPAIR PROTOCOL: If post-repair test FAILS, KEEP ESCROW LOCKED. Notify technician: "Diagnostic test failed. Payout withheld. Scheduling secondary audit."
7. TIMEOUT IDEMPOTENCY: On 504 Gateway Timeout, never retry duplicate charges. Queue transaction with SHA-256 idempotency key and poll Plural webhook.
```

---

## 3. Failure Analysis: Which Cases Does the Agent Still Fail & Why?

1. **Complex Cascading Multi-Faults (e.g. Broken Drum Spider + Burned Stator Coil Simultaneously)**:
   - *Why*: When multiple mechanical components fail at once, their acoustic harmonic peaks overlap and modulate each other. The current single-hypothesis Neyman-Pearson LRT isolates the primary peak (e.g., drum imbalance) but may require a secondary diagnostic pass after the first part is replaced to identify the second deeper electrical fault.
2. **Extreme Acoustic Reverberation in Empty Tiled Bathrooms**:
   - *Why*: If a washing machine is placed in an untreated tiled bathroom with high echo (>1.2s $RT_{60}$ reverberation time), multipath reflections can occasionally degrade spectral flatness, requiring 2 attempts to achieve a clean reading.
