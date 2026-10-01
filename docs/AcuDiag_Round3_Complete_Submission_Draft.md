# 🏆 AcuDiag: The Ken Case-Build 2026 Round 3 Official Submission Package

> **Competition**: The Ken Case-Build 2026: "The Great Rewiring"  
> **Track**: Build Round (Online Prototype Sprint)  
> **Team Lead**: K.Sai Jaswanth Reddy (`ksaijaswanthr.cs24@rvce.edu.in`)  
> **Problem Space #9**: Keeping the Machines Running (Home Appliances & Devices)  
> **Agent Name**: AcuDiag Orchestrator  
> **Platform Runtime**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`, Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)

> [!TIP]
> **MASTER COPY-PASTE SUBMISSION**: The finalized, field-by-field copy-paste responses for the official Typeform portal are maintained in:  
> 👉 [`THE_KEN_ROUND_3_FINAL_SUBMISSION_MASTER.md`](THE_KEN_ROUND_3_FINAL_SUBMISSION_MASTER.md)

---

# PART 1: YOUR AGENT

### 1. The Story of One Person Using Your Agent (Strictly $\le$ 100 Words)

On October 2, Priya in Bengaluru notices her washing machine vibrating violently during spin. She calls AcuDiag. Speaking in Kannada-accented Hinglish, she says the drum makes a metallic clattering sound. AcuDiag hears the symptom, locks ₹1,250 in a Pine Labs escrow pre-auth, and dispatches a genuine OEM drum bearing via Delhivery. When technician Ramesh arrives and installs it, AcuDiag prompts Priya to record a 5-second spin. AcuDiag’s audio engine confirms normal acoustics. Only then does AcuDiag release the escrow payment to Ramesh's wallet and schedule Delhivery to reverse-pickup the damaged part for recycling.

*(Word Count: 98 words)*

---

### 2. Every Decision the Agent Makes in the Recording (Chronological Decision Log)

#### Decision 1: Language & Fault Entity Extraction
* **When**: 2026-10-02 10:14:02 IST
* **What the agent received**: Raw streaming audio utterance: *"Washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai."*
* **Where it came from**: `gnani_voice_bridge` connector (Real source: User PSTN mobile phone call).
* **What it decided**: Decided to isolate symptom as `WM_BEARING_SPALL` (Subsystem: Drum Assembly) and set session language to Hinglish (`hi-IN/en-IN`).
* **Why**: System Prompt Invariant 1: *"Parse Hinglish code-switching; map acoustic descriptions to appliance subsystem fault taxonomy."*
* **What it did or said, and to whom**: Said to Priya: *"Main samajh gaya. Drum bearing mein friction lag rahi hai. Hum turant diagnosis shuru karte hain."*
* **Through what**: `gnani_voice_bridge` (TTS audio stream).

#### Decision 2: Pre-Service Escrow Pre-Auth Hold
* **When**: 2026-10-02 10:14:35 IST
* **What the agent received**: User confirmation of home address and appointment window.
* **Where it came from**: `gnani_voice_bridge` connector.
* **What it decided**: Decided to lock ₹1,250 in escrow before triggering any physical logistics or technician dispatch.
* **Why**: System Prompt Invariant 2: *"Never dispatch a technician or parts until Pine Labs confirms PRE_AUTH_LOCKED."*
* **What it did or said, and to whom**: Sent API payload `POST /api/pay/v1/orders` (`pre_auth: true`, amount: `125000`) to Pine Labs Plural.
* **Through what**: `pinelabs_plural` connector.

#### Decision 3: Programmatic OEM Part Manifestation
* **When**: 2026-10-02 10:14:38 IST
* **What the agent received**: `status: "PRE_AUTH_LOCKED"` with order ID `PL_ORD_8A92B1C4`.
* **Where it came from**: `pinelabs_plural` connector.
* **What it decided**: Decided to bypass third-party technician parts markup and manifest genuine OEM bearing SKU `BEAR-6205-2RS` directly from Godrej Peenya hub.
* **Why**: System Prompt Invariant 3: *"Upon escrow lock, programmatically dispatch factory OEM part to customer doorstep."*
* **What it did or said, and to whom**: Sent dispatch request `POST /api/cmu/create.json` to Delhivery.
* **Through what**: `delhivery_logistics` connector.

#### Decision 4: SNR Quality & Replay Anti-Spoofing Audit
* **When**: 2026-10-02 11:32:15 IST
* **What the agent received**: 5-second 44.1 kHz PCM audio recording of newly repaired washing machine.
* **Where it came from**: AcuDiag PWA WebAudio stream via `acudiag_webaudio_hook`.
* **What it decided**: Decided the capture was authentic physical vibration (Low rumble ratio: 0.42 > 0.06; Speaker resonance: 0.002 < 0.08) and SNR was clean (23.8 dB > 15 dB). Proceeded to Neyman-Pearson LRT.
* **Why**: System Prompt Invariant 4: *"Reject captures with SNR < 15 dB; flag speaker playback if low-frequency physical rumble is absent."*
* **What it did or said, and to whom**: Processed audio through Butterworth SOS + Gammatone 64-dim ERB filterbank.
* **Through what**: Internal DSP Engine (`audio_diagnostic.py`).

#### Decision 5: Conditional Escrow Release Trigger
* **When**: 2026-10-02 11:32:17 IST
* **What the agent received**: Neyman-Pearson anomaly score $\Lambda(x) = 0.38 \le 2.45$ (PASS).
* **Where it came from**: Internal DSP Engine (`audio_diagnostic.py`).
* **What it decided**: Decided to release the ₹1,250 escrow hold immediately to technician Ramesh's wallet and close the ticket.
* **Why**: System Prompt Invariant 5: *"Call Pine Labs capture ONLY when Neyman-Pearson LRT <= 2.45 AND Anti-Spoofing is TRUE."*
* **What it did or said, and to whom**: Sent capture call `PUT /api/pay/v1/orders/PL_ORD_8A92B1C4/capture` to Pine Labs; sent SMS to Priya: *"Aapki washing machine ka test pass ho gaya hai! ₹1,250 settlement complete."*
* **Through what**: `pinelabs_plural` and `twilio_sms` connectors.

#### Decision 6: Automated Reverse Core Logistics Dispatch
* **When**: 2026-10-02 11:32:20 IST
* **What the agent received**: Escrow settlement confirmation `CAPTURED_SETTLED`.
* **Where it came from**: `pinelabs_plural` connector.
* **What it decided**: Decided to schedule reverse pickup of the defective old bearing for OEM recycling and core-deposit return.
* **Why**: System Prompt Invariant 6: *"Post-settlement, schedule reverse pickup with Doorstep QC for damaged core recovery."*
* **What it did or said, and to whom**: Sent `POST /fm/request/new/` with `doorstep_qc_enabled: true` to Delhivery.
* **Through what**: `delhivery_logistics` connector.

---

### 3. Complete Connectors List (Real vs. Mock)

| Connector Name | Type | Implementation & Platform Route | Exact Operational Purpose |
| :--- | :---: | :--- | :--- |
| **`gnani_voice_bridge`** | **REAL** | `wss://api.vachana.ai/stt/v3/stream` (Gnani Speech API) | Streams real-time vernacular STT/TTS, handles barge-in, and captures Hinglish symptom descriptions. |
| **`pinelabs_plural`** | **REAL & MOCK** | Active native connector on AgenticOrg + Local FastAPI mock | Creates pre-auth payment orders (`POST /api/pay/v1/orders`), holds escrow, captures settlement, and issues refunds. |
| **`delhivery_logistics`** | **MOCK** | Custom FastAPI server hosting exact Delhivery OpenAPI schemas | Verifies pincode SLAs (`/c/api/pin-codes/json/`), creates waybills (`/api/cmu/create.json`), and schedules reverse QC (`/fm/request/new/`). |
| **`whatsapp_notifier`** | **REAL** | Meta Cloud WhatsApp Business API / Twilio | Delivers diagnostic spectrogram summary, invoice breakdown, and 1-click UPI authorization links to the user. |
| **`oem_beckn_gateway`** | **MOCK** | Custom Beckn Protocol connector | Checks appliance serial numbers against manufacturer warranty registries (`/api/v1/oem/warranty/verify`) to execute Warranty Intercept. |

---

### 4. Up to 3 Capabilities Partners Don't Offer Today

#### Capability 1 (Delhivery): GeoNaksha 3D Hyper-Local Precision Gate Drop
* **Partner**: Delhivery
* **Endpoint**: `POST /api/v1/delhivery/geonaksha/validate`
* **Underlying Partner Data**:
  Delhivery's proprietary geospatial delivery graph spanning 1+ billion successful deliveries, address string tokenizers, and field executive GPS trace logs.
* **How It Works**:
  Translates vague Indian addresses (*"Behind temple, 2nd green gate, 3rd floor"*) into millimeter-accurate building entrance coordinates, calculates elevator vs stairwell delivery times, and issues automated security-gate OTP clearance passes directly to the rider.

#### Capability 2 (Pine Labs): Sub-Millisecond Cryptographic Acoustic Escrow Trigger
* **Partner**: Pine Labs
* **Endpoint**: `POST /api/v1/pinelabs/escrow/conditional-trigger`
* **Underlying Partner Data**:
  Pine Labs Plural multi-tier transaction mandate tables, tokenized card vaults, and real-time merchant settlement switch.
* **How It Works**:
  Binds the Neyman-Pearson Likelihood Ratio Test directly to the Plural core banking switch. Upon receiving an Ed25519-signed telemetry packet from AcuDiag ($\Lambda(x) < 2.45 \land \text{AntiSpoof} = \text{True}$), Pine Labs executes an atomic, sub-10ms ledger transfer from escrow to the technician's bank node with zero human intermediary delay.

#### Capability 3 (Gnani.ai): Broadband Unfiltered VAD Diagnostic Audio Stream
* **Partner**: Gnani.ai
* **Endpoint**: `GET /api/v1/gnani/acoustic/vad-bypass-stream`
* **Underlying Partner Data**:
  Gnani's raw RTP media server audio buffers prior to the 300 Hz – 3,400 Hz Voice Activity Detection (VAD) speech filtering layer.
* **How It Works**:
  Provides a bypass hook that routes full-spectrum (20 Hz – 8,000 Hz) acoustic frequencies directly to AcuDiag's Gammatone filterbank during diagnostic scan windows, allowing standard phone calls to capture mechanical motor vibrations that normal speech codecs discard.

---

### 5. Rail Agent-Readiness Scores (Out of 10)

| Rail | Score | Concise Architectural Justification |
| :--- | :---: | :--- |
| **Gnani.ai (Voice)** | **8 / 10** | Outstanding Indian regional language ASR and streaming WebSocket latency (<200ms barge-in), but lacks an explicit non-speech acoustic diagnostic mode for mechanical sound capture without aggressive noise cancellation. |
| **Pine Labs (Payments)** | **9 / 10** | Robust, bank-grade pre-authorization APIs and native AgenticOrg integration, but lacks native cryptographic webhook triggers binding physical sensor telemetry directly to escrow release. |
| **Delhivery (Logistics)** | **7 / 10** | Industry-leading Indian PIN-code coverage and automated reverse pickup capabilities, but developer portal access requires manual commercial onboarding and lacks instantaneous micro-fulfillment API dispatch under 2 hours. |

---

# PART 2: HOW YOU GOT YOUR AGENT HERE

### 1. The 10 Adversarial Evaluation Cases

| # | Scenario | Input Trigger | Unexpected / Adversarial Condition | Expected Agent Autonomous Behavior |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Heavy Hinglish Code-Switching** | Voice audio in Gnani | *"Bhai washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai, pani bhi leak ho raha hai"* | Correctly parses mixed linguistic tokens; isolates symptoms (`drum noise` + `water leakage`); does not crash or request English repetition. |
| **2** | **Technician Audio Replay Fraud (Spoofing)** | Diagnostic capture in WebAudio | Technician plays a recorded healthy washing machine `.wav` file through their smartphone speaker | Anti-spoofing engine flags lack of low-frequency physical rumble (<60Hz) and DAC quantization peak; rejects test with `REJECTED_REPLAY_ATTACK`; alerts customer. |
| **3** | **High Ambient Kitchen Noise (Low SNR)** | Diagnostic capture in WebAudio | Customer records while pressure cooker is whistling and television is loud (SNR = 8.2 dB) | Gating catches SNR < 15 dB; refuses to pass/fail repair; instructs user via Gnani voice to close kitchen doors and re-record. |
| **4** | **Delhivery Rider Cancellation / No Rider** | Delivery dispatch call | Delhivery mock connector returns `503 NO_RIDER_AVAILABLE` | Agent autonomously retries nearest peripheral logistics micro-hub; if unserviceable within 30 min, extends appointment and sends SMS apology. |
| **5** | **Pre-Auth Escrow Card Decline** | Pine Labs pre-auth API | Pine Labs returns `402 INSUFFICIENT_FUNDS` | Agent pauses technician dispatch; notifies user on WhatsApp with direct UPI payment link to authorize escrow hold before rider departs. |
| **6** | **Incomplete / Fake Repair by Technician** | Post-repair acoustic test | Technician claims "I tightened the bearing", but acoustic capture still exhibits 1,450 Hz BPFO harmonic resonance | Neyman-Pearson LRT exceeds threshold ($\Lambda(x) = 8.42 > 2.45$); rejects capture; **locks Pine Labs escrow hold**; schedules free secondary audit. |
| **7** | **Dead-On-Arrival (DOA) Replacement Part** | Unboxing inspection | New pump installed by technician fails immediately with cavitation screech | Agent triggers Delhivery Surface Reverse Pickup (`/fm/request/new/`); flags part serial number in warranty ledger; orders replacement without charging customer. |
| **8** | **Active OEM Warranty Intercept** | Invoice upload OCR | User uploads purchase receipt showing appliance bought 8 months ago (Standard 2-year warranty) | Agent immediately aborts paid escrow flow; generates free OEM warranty docket; forwards to official manufacturer service bridge (saves user ₹3,200). |
| **9** | **User Refuses / Aborts Post-Repair Test** | WebAudio prompt | User taps "I don't want to test, let the technician go" | Agent enforces safety protocol: informs user that unverified release forfeits 90-day dispute guarantee; holds escrow for 24-hour auto-dispute cooling period. |
| **10** | **Upstream Bank Network Timeout** | Pine Labs capture call | Pine Labs Plural API times out with `504 GATEWAY_TIMEOUT` | Agent logs idempotent transaction token; does not duplicate charges; enters async webhook polling state until bank switch confirmation arrives. |

---

### 2. Testing Run Logs & System Prompt Evolution

#### Round 1 Testing Run Log (v1.0 Prompt)
* **Observed Failure**: In Eval Case 6 (Fake Repair), the technician verbally announced: *"Madame, machine theek ho gayi hai, payment confirm kijiye."* The v1.0 agent immediately invoked Pine Labs capture based on verbal technician assertion without waiting for acoustic verification.
* **Root Cause**: v1.0 prompt lacked strict cryptographic precondition gating on acoustic pass tokens.
* **Mutation**: Codified Invariant 5: Escrow capture can NEVER be triggered by conversational text; strictly gated on Neyman-Pearson PASS.

#### Round 2 Testing Run Log (v2.0 Prompt)
* **Observed Failure**: In Eval Case 3 (Kitchen Noise), a pressure cooker whistling raised spectral energy across the 2 kHz – 4 kHz band. The agent falsely classified a healthy repair as a bearing spall and blocked escrow release.
* **Root Cause**: Gating occurred post-inference without a preliminary Signal-to-Noise Ratio (SNR) threshold.
* **Mutation**: Codified Invariant 3: Added pre-inference SNR gating (>15 dB). If ambient noise floor is too high, abort immediately and instruct the homeowner to close the kitchen door.

#### Round 3 Testing Run Log (v3.0 Prompt)
* **Observed Failure**: In Eval Case 2 (Replay Attack), a speaker playback of a healthy machine passed the LRT test because the frequency spectrum matched.
* **Root Cause**: System evaluated spectral amplitude without inspecting mechanical contact vibration or DAC quantization artifacts.
* **Mutation**: Added Invariant 4: Mandatory low-frequency physical rumble ratio (<100 Hz) verification and contact requirement.

---

### 3. System Prompt Versions

#### Version 1.0 (Initial Scaffold)
```text
You are AcuDiag, an automated appliance diagnostic agent.
Listen to the user's problem via voice, find what is wrong, and book a technician.
When the technician arrives, hold payments and release payment after the machine is fixed.
```

#### Version 2.0 (Added Rail Gating)
```text
You are AcuDiag, an autonomous appliance diagnostic and escrow orchestrator.
1. Connect to Gnani for voice intake.
2. Call Pine Labs POST /api/pay/v1/orders with pre_auth: true before dispatching Delhivery parts.
3. Only release Pine Labs escrow when the post-repair diagnostic returns PASS.
```

#### Version 3.0 (Final Production System Prompt — Battle-Tested)
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

### 4. Which Cases Does the Agent Still Fail & Why?

1. **Simultaneous Cascading Multi-Faults (e.g. Broken Drum Spider + Burned Stator Coil)**:
   - *Why*: When multiple mechanical components fail at once, their acoustic harmonic peaks overlap and modulate each other. The single-hypothesis Neyman-Pearson LRT isolates the primary structural peak (e.g., drum imbalance) but requires a secondary diagnostic pass after the first part is replaced to identify the second deeper electrical fault.
2. **Extreme Acoustic Reverberation in Empty Tiled Bathrooms**:
   - *Why*: If a washing machine is placed in an untreated tiled bathroom with high echo (>1.2s $RT_{60}$ reverberation time), multipath reflections can occasionally degrade spectral flatness, requiring 2 attempts to achieve a clean reading.

---

### 5. Official Screen Recording Runbook (Video Walkthrough Guide)

1. **Primary Happy Flow Walkthrough (2 Mins)**:
   - Open browser on `https://agenticorg.hackathon.pinelabs.com`.
   - Show AcuDiag Agent with System Prompt v3.0 and active connectors (`pinelabs_plural`, `delhivery_logistics`, `gnani_voice_bridge`).
   - Trigger simulated user voice call in Hinglish.
   - Show Pine Labs Pre-Auth hold order appearing on dashboard (`PRE_AUTH_LOCKED`).
   - Show Delhivery forward waybill generation (`WAYBILL_DEL_...`).
   - Upload 5-second repaired audio $\rightarrow$ Show 60 FPS Spectrogram canvas passing LRT ($\Lambda(x) = 0.38 \le 2.45$).
   - Show Pine Labs Escrow capture transition to `CAPTURED_SETTLED` and reverse pickup scheduled.
2. **Alternative Human Input Run 1 (Pre-Auth Card Decline)**:
   - Run agent with customer card balance = ₹0.
   - Show Pine Labs returning `402 INSUFFICIENT_FUNDS`.
   - Show AcuDiag pausing technician dispatch and sending automated WhatsApp UPI link.
3. **Alternative Human Input Run 2 (Technician Fake Repair)**:
   - Upload faulty bearing sound post-repair.
   - Show Neyman-Pearson LRT failing ($\Lambda(x) = 8.42$).
   - Show Pine Labs Escrow remaining LOCKED (`ESCROW_RELEASE_BLOCKED`) and scheduling secondary audit.
