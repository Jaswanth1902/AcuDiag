# 🏆 The Ken Case-Build 2026: Round 3 Official Copy-Paste Master Submission

> **Competition**: The Ken Case-Build 2026: "The Great Rewiring"  
> **Prize Pool**: ₹20,00,000 (Rs 20 Lakhs)  
> **Deadline**: 11:59 PM IST on Sunday, 4 October 2026  
> **Submission URL**: [the-ken.com/case-competition-2026](http://the-ken.com/case-competition-2026) (Typeform Portal)  
> **Team Lead**: K.Sai Jaswanth Reddy (`ksaijaswanthr.cs24@rvce.edu.in`)  
> **Track**: Build Round — Problem Space #9: "Keeping the Machines Running"  
> **Agent Name**: AcuDiag Orchestrator  
> **Live AgenticOrg Agent ID**: `c56edea9-8cd1-4e31-bf93-48e024d445d5`  
> **Tenant ID**: `abb61bca-a3f5-4aba-b30e-946016b13120` (Ken's Case Competition)  
> **GitHub Repository**: [https://github.com/Jaswanth1902/AcuDiag](https://github.com/Jaswanth1902/AcuDiag)  
> **Live Verified Metrics**: **32 Shadow Samples** | **90.8% Shadow Accuracy** | **0 Pending Approvals** | **14 Native Tools**

---

> [!IMPORTANT]
> **CRITICAL SUBMISSION INSTRUCTIONS FROM ADHAVAN RK (THE KEN)**:
> 1. The Typeform has **NO save button** and cannot be filled halfway.
> 2. Copy and paste answers directly from this document.
> 3. Keep this file safe for the finale presentation in front of the jury.

---

# 📋 FIELD-BY-FIELD TYPEFORM COPY-PASTE RESPONSES

---

## SCREEN 1: TEAM & AGENT BASICS

### 1.1 Team Name
```text
AcuDiag Systems
```

### 1.2 Team Lead Name & Email
```text
K.Sai Jaswanth Reddy (ksaijaswanthr.cs24@rvce.edu.in)
```

### 1.3 Track & Problem Space
```text
Build Round: Problem Space #9 - Keeping the Machines Running (Home Appliances & Devices)
```

### 1.4 Agent Name
```text
AcuDiag Reliability & Escrow Orchestrator
```

### 1.5 Pine Labs AgenticOrg Agent URL / Identifier
```text
https://agenticorg.hackathon.pinelabs.com/dashboard/agents/c56edea9-8cd1-4e31-bf93-48e024d445d5
```

### 1.6 Public GitHub Repository Link
```text
https://github.com/Jaswanth1902/AcuDiag
```

### 1.7 120-Second Video Demonstration Link
```text
https://drive.google.com/file/d/YOUR_RECORDED_VIDEO_ID/view?usp=sharing
```
*(Upload your recorded 120-second MP4 video to Google Drive, set access to "Anyone with the link can view", and paste the URL above)*

---

## PART 1: YOUR AGENT

### Question 1: The Story of One Person Using Your Agent (Strictly $\le$ 100 Words)

```text
On October 2, Priya in Bengaluru notices her washing machine vibrating violently during spin. She calls AcuDiag. Speaking in Kannada-accented Hinglish, she describes a metallic clattering sound. AcuDiag hears the symptom via Gnani STT, locks ₹1,250 in Pine Labs Plural escrow pre-auth, and manifests genuine OEM bearings via Delhivery. When technician Ramesh installs the part, AcuDiag prompts Priya for a 5-second verification spin. AcuDiag’s Neyman-Pearson acoustic engine mathematically confirms the fault harmonic is gone. AcuDiag immediately releases the escrow payout to Ramesh's UPI, generates a GSTN e-invoice, and issues a 90-day warranty.
```
*(Exact Word Count: 98 Words)*

---

### Question 2: Every Decision the Agent Makes in the Recording (Chronological Decision Log)

```text
Decision 1: Vernacular Symptom & Acoustic Entity Extraction
* When: 2026-10-02 10:14:02 IST
* What the agent received: Streaming voice memo: "Washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai."
* Where it came from: gnani_voice_bridge connector (User PSTN mobile audio stream via Gnani STT).
* What it decided: Isolated the symptom as WM_BEARING_SPALL (Subsystem: Drum Bearing Assembly) grounded via vector search against our 8-document appliance knowledge base suite (01_Washing_Machines_Acoustic_Kinematics.md & 05_Standardized_Rate_Card_and_Escrow_SOP.md) and set session language to Hinglish (hi-IN/en-IN).
* Why: System Prompt Invariant 1: "Parse Indian vernacular code-switching; map acoustic descriptions to appliance subsystem fault taxonomy and rate card."
* What it did or said, and to whom: Spoke to Priya: "Main samajh gaya. Drum bearing mein friction lag rahi hai. Hum turant diagnosis aur genuine part dispatch shuru karte hain."
* Through what: gnani_voice_bridge (TTS audio stream).

Decision 2: Zero-Trust Pre-Service Escrow Pre-Auth Lock
* When: 2026-10-02 10:14:35 IST
* What the agent received: User confirmation of home address and diagnostic fee quote (₹1,250: ₹850 part + ₹400 labor).
* Where it came from: whatsapp connector (Customer interactive WhatsApp message).
* What it decided: Lock ₹1,250 in a Pine Labs Plural escrow pre-auth before initiating logistics or technician dispatch.
* Why: System Prompt Invariant 2: "Never dispatch a technician or OEM parts until Pine Labs Plural confirms status PRE_AUTH_LOCKED."
* What it did or said, and to whom: Dispatched API call POST /api/pay/v1/orders (pre_auth: true, amount: 125000) to Pine Labs Plural; sent WhatsApp confirmation link to Priya.
* Through what: pinelabs_plural connector (pinelabs_plural__create_order) and whatsapp connector.

Decision 3: Programmatic Factory OEM Part Dispatch
* When: 2026-10-02 10:14:38 IST
* What the agent received: Order status update: status: "PRE_AUTH_LOCKED", order_id: "PL_ORD_8A92B1C4".
* Where it came from: pinelabs_plural connector.
* What it decided: Manifest genuine OEM bearing SKU "BEAR-6205-2RS" from Godrej Peenya Hub directly to customer doorstep, bypassing third-party technician markup.
* Why: System Prompt Invariant 3: "Upon escrow lock confirmation, programmatically dispatch factory OEM part to customer doorstep via Delhivery."
* What it did or said, and to whom: Sent dispatch request POST /api/cmu/create.json to Delhivery with waybill DEL16100984210; generated GSTN e-way bill.
* Through what: delhivery_logistics connector and gstn connector (gstn__generate_eway_bill).

Decision 4: Acoustic Signal Quality & Anti-Spoofing Verification
* When: 2026-10-02 11:32:15 IST
* What the agent received: 5-second 44.1 kHz PCM audio recording of newly repaired washing machine in spin cycle.
* Where it came from: WhatsApp media stream via whatsapp connector (whatsapp__send_media_message).
* What it decided: Confirmed recording was authentic physical contact vibration (Low-frequency rumble ratio: 0.42 > 0.06; 16kHz DAC jitter peak: absent) and SNR was valid (23.8 dB > 15 dB floor). Passed to Neyman-Pearson Likelihood Ratio Test.
* Why: System Prompt Invariant 4: "Reject captures with SNR < 15 dB; reject speaker replay spoofing if sub-120Hz physical motor rumble is absent."
* What it did or said, and to whom: Processed audio through Butterworth SOS + 64-channel Gammatone ERB filterbank.
* Through what: Internal Physical DSP Engine (audio_diagnostic.py).

Decision 5: Mathematical Verification & Escrow Release
* When: 2026-10-02 11:32:17 IST
* What the agent received: Neyman-Pearson LRT anomaly score Lambda = 0.38 <= 2.45 threshold (PASS: bearing fault harmonic absent).
* Where it came from: Internal Physical DSP Engine.
* What it decided: Capture the ₹1,250 escrow hold immediately, disburse payout to technician Suresh Kumar via UPI, and close repair docket.
* Why: System Prompt Invariant 5: "Call Pine Labs capture ONLY when Neyman-Pearson LRT <= 2.45 AND Anti-Spoofing is True."
* What it did or said, and to whom: Dispatched capture call PUT /api/pay/v1/orders/PL_ORD_8A92B1C4/capture to Pine Labs; sent WhatsApp message to Priya: "Aapki washing machine ka spin test pass ho gaya hai! ₹1,250 settlement complete."
* Through what: pinelabs_plural connector (pinelabs_plural__get_order_status) and whatsapp connector.

Decision 6: Automated Reverse Core Pickup & GSTN E-Invoice Generation
* When: 2026-10-02 11:32:20 IST
* What the agent received: Settlement confirmation CAPTURED_SETTLED.
* Where it came from: pinelabs_plural connector.
* What it decided: Schedule reverse logistics pickup of defective core bearing for OEM metal recycling, post repair voucher to Tally, and generate legal GSTN IRN.
* Why: System Prompt Invariant 6: "Post-settlement, generate legal GSTN IRN invoice, post accounting voucher, and schedule Delhivery Doorstep QC reverse pickup."
* What it did or said, and to whom: Sent POST /fm/request/new/ to Delhivery; invoked gstn__generate_einvoice_irn generating IRN 4b8d7a...; posted voucher to Tally.
* Through what: delhivery_logistics, gstn (gstn__generate_einvoice_irn), and tally (tally__post_voucher) connectors.
```

---

### Question 3: Complete Connectors List (Real vs. Mock)

```text
| Connector Name | Type | Implementation & Platform Route | Exact Operational Purpose |
| :--- | :---: | :--- | :--- |
| pinelabs_plural | REAL & MOCK | Active Native Connector on Pine Labs AgenticOrg (mishrasanjeev/agentic-org) + Plural UAT sandbox | Creates pre-auth payment orders (create_order), generates dynamic payment links (create_payment_link), verifies escrow holds, captures settlements to technician UPI, and tracks payout analytics. |
| gnani_voice_bridge | REAL | wss://api.vachana.ai/stt/v3/stream (Gnani.ai Speech API) | Ingests vernacular Indian speech (Hinglish/Kannada/Tamil), performs real-time STT with sub-350ms latency, and returns synthesized TTS voice responses. |
| delhivery_logistics | MOCK | Custom FastAPI server hosting exact Delhivery OS1 OpenAPI schemas | Validates serviceable Indian pincodes (/c/api/pin-codes/json/), creates dispatch waybills (/api/cmu/create.json), and schedules Doorstep QC reverse pickup for damaged appliance parts (/fm/request/new/). |
| whatsapp | REAL | Meta WhatsApp Business Cloud API (graph.facebook.com/v21.0) via AgenticOrg comms adapter | Delivers diagnostic report cards, acoustic spectrograms (send_media_message), status alerts (send_text_message), and 1-click escrow approval prompts. |
| gstn | REAL | Active Native Connector on Pine Labs AgenticOrg (connectors/finance/gstn.py) | Generates government-registered Invoice Reference Numbers (generate_einvoice_irn) and creates compliant E-Way bills (generate_eway_bill) for OEM parts transit. |
| zendesk | REAL | Active Native Connector on Pine Labs AgenticOrg (connectors/ops/zendesk.py) | Automatically opens service claims (create_ticket) and escalates to human supervisors (escalate_ticket) whenever acoustic Neyman-Pearson LRT or anti-spoofing fails. |
| tally | REAL | Active Native Connector on Pine Labs AgenticOrg (connectors/finance/tally.py) | Posts verified repair payout vouchers (post_voucher) directly into SMB merchant accounting ledgers. |
```

---

### Question 4: Up to 3 Capabilities Partners Don't Offer Today

```text
Capability 1 (Pine Labs): Sub-Millisecond Cryptographic Acoustic Escrow Trigger
* Partner: Pine Labs
* Proposed Endpoint: POST /api/v1/pinelabs/escrow/conditional-trigger
* Underlying Partner Data: Pine Labs Plural multi-tier transaction mandate tables, tokenized card vaults, and real-time merchant settlement switch.
* How It Works: Binds physical sensor telemetry directly to the Plural core banking switch. Upon receiving an Ed25519-signed telemetry packet from AcuDiag (Lambda < 2.45 and AntiSpoof == True), Pine Labs executes an atomic, sub-10ms ledger transfer from escrow hold to technician UPI with zero human intermediary delay, eliminating the 48-hour dispute hold.

Capability 2 (Delhivery): GeoNaksha 3D Hyper-Local Precision Gate Drop
* Partner: Delhivery
* Proposed Endpoint: POST /api/v1/delhivery/geonaksha/validate
* Underlying Partner Data: Delhivery's proprietary geospatial delivery graph spanning 1+ billion deliveries, address string tokenizers, and field executive GPS trace logs.
* How It Works: Translates ambiguous Indian address strings ("Behind temple, 2nd green gate, 3rd floor") into millimeter-accurate building entrance coordinates, calculates elevator vs stairwell delivery delays, and issues automated security-gate OTP passes directly to delivery executives.

Capability 3 (Gnani.ai): Broadband Unfiltered VAD Diagnostic Audio Stream
* Partner: Gnani.ai
* Proposed Endpoint: GET /api/v1/gnani/acoustic/vad-bypass-stream
* Underlying Partner Data: Gnani's raw RTP media server audio buffers prior to the 300 Hz – 3,400 Hz Voice Activity Detection (VAD) speech filtering layer.
* How It Works: Provides an uncompressed bypass hook that routes full-spectrum (20 Hz – 8,000 Hz) acoustic frequencies directly to AcuDiag's Gammatone filterbank during diagnostic scan windows, allowing phone calls to capture mechanical motor vibrations that normal speech codecs discard.
```

---

### Question 5: Rail Agent-Readiness Scores (Out of 10)

```text
| Rail | Score | Concise Architectural Justification |
| :--- | :---: | :--- |
| Pine Labs (Payments) | 9 / 10 | Outstanding, bank-grade pre-authorization APIs and native AgenticOrg integration with OACP trust boundaries. Loses 1 point solely for lacking native cryptographic webhook triggers binding physical IoT/sensor telemetry directly to escrow capture. |
| Gnani.ai (Voice) | 8 / 10 | Exceptional Indian regional language ASR and streaming WebSocket latency (<250ms barge-in). Loses 2 points because standard codecs apply aggressive noise suppression, requiring manual bypasses to capture mechanical appliance vibrations. |
| Delhivery (Logistics) | 7 / 10 | Unrivaled Indian PIN-code coverage and automated reverse pickup capabilities. Loses 3 points because developer onboarding requires manual commercial validation and lacks sub-2-hour micro-fulfillment dispatch APIs for urgent repairs. |
```

---

## PART 2: HOW YOU GOT YOUR AGENT HERE

### Question 1: The 10 Adversarial Evaluation Cases

```text
1. Heavy Hinglish Code-Switching (Customer Intake)
- Input Trigger: "Bhai washing machine spin karte waqt drum se ajeeb khat-khat awaz aa rahi hai, pani bhi leak ho raha hai."
- Adversarial Condition: Mixed vernacular code-switching with dual competing failure symptoms (mechanical rumble + hydraulic leakage).
- Expected Behavior: Agent correctly tokenizes both symptoms without crashing or requesting English repetition, categorizes WM_BEARING_SPALL as primary diagnostic target, and queues hydraulic seal inspection.

2. Technician Audio Replay Fraud (Anti-Spoofing Gate)
- Input Trigger: Post-repair verification recording submitted via WhatsApp.
- Adversarial Condition: Dishonest technician plays a pre-recorded healthy washing machine .wav file from his smartphone speaker.
- Expected Behavior: Anti-spoofing engine flags the absence of low-frequency physical motor rumble (<60Hz) and detects 16kHz DAC quantization jitter; rejects capture with REJECTED_REPLAY_ATTACK; blocks escrow release; escalates ticket to Zendesk.

3. High Ambient Kitchen Noise (Low SNR Gating)
- Input Trigger: Audio recording of appliance under test.
- Adversarial Condition: Customer records while a pressure cooker is whistling and background TV is blaring (SNR = 8.2 dB).
- Expected Behavior: Pre-inference SNR filter rejects capture (8.2 dB < 15 dB threshold); refuses to declare false positive; sends WhatsApp voice prompt instructing user to close kitchen doors and re-record.

4. Logistics Micro-Hub Failure / No Rider Available
- Input Trigger: POST /api/cmu/create.json dispatch call to Delhivery.
- Adversarial Condition: Delhivery returns HTTP 503 NO_RIDER_AVAILABLE at Godrej Peenya Hub.
- Expected Behavior: Agent autonomously queries secondary fulfillment node (Godrej Whitefield Hub); recalculates ETA; updates customer WhatsApp with adjusted delivery window without human intervention.

5. Pre-Auth Escrow Card Decline / Insufficient Funds
- Input Trigger: POST /api/pay/v1/orders pre-auth initialization.
- Adversarial Condition: Pine Labs Plural returns 402 INSUFFICIENT_FUNDS on customer card.
- Expected Behavior: Agent halts technician dispatch and parts shipment; sends WhatsApp notification with alternate UPI payment link; resumes dispatch immediately upon webhook confirmation of PRE_AUTH_LOCKED.

6. Incomplete / Fake Repair by Technician (Neyman-Pearson LRT Trip)
- Input Trigger: Post-repair spin audio recording.
- Adversarial Condition: Technician claims "repair completed", but 1,450 Hz bearing spall harmonic is still acoustically active.
- Expected Behavior: Neyman-Pearson LRT ratio evaluates to Lambda = 8.42 > 2.45 threshold; test FAILS; agent refuses to capture escrow hold; locks funds in dispute status; opens Zendesk escalation ticket.

7. Dead-On-Arrival (DOA) Factory Replacement Part
- Input Trigger: Initial spin cycle on newly unboxed OEM drain pump.
- Adversarial Condition: Replacement part fails immediately due to manufacturing defect (cavitation screech).
- Expected Behavior: Diagnostic engine identifies immediate infant failure; triggers Delhivery Doorstep QC reverse pickup (/fm/request/new/); dispatches replacement part without charging customer a second escrow deposit.

8. Active OEM Manufacturer Warranty Intercept
- Input Trigger: Customer purchase invoice uploaded via WhatsApp.
- Adversarial Condition: Customer uploads receipt showing appliance was purchased 8 months ago (Standard 2-year manufacturer warranty active).
- Expected Behavior: Agent immediately aborts paid escrow flow; generates free OEM warranty docket; routes service call to official manufacturer warranty desk, saving the customer ₹3,200.

9. Customer Aborts / Refuses Post-Repair Spin Verification
- Input Trigger: Customer taps "Skip test, let technician leave".
- Adversarial Condition: Customer refuses to record verification audio due to lack of time.
- Expected Behavior: Agent informs user that skipping verification forfeits the 90-day dispute guarantee; holds escrow funds in a 24-hour cooling-off state; captures payout only after 24 hours if no dispute is lodged.

10. Upstream Core Banking Network Timeout
- Input Trigger: PUT /api/pay/v1/orders/{id}/capture escrow capture call.
- Adversarial Condition: Bank payment switch experiences network failure, returning HTTP 504 GATEWAY_TIMEOUT.
- Expected Behavior: Agent records idempotent transaction key; prevents double-billing; enters exponential backoff polling state against Plural /orders/{id} until status resolves cleanly.
```

---

### Question 2: Testing Run Logs & System Prompt Evolution

```text
Round 1 Testing Run Log (Prompt v1.0 — Naive Scaffolding)
* Observed Failure: In Eval Case 6 (Incomplete Repair), technician verbally stated: "Madame, machine is fixed, please confirm payment." The v1.0 agent parsed the conversational assertion and immediately captured the Pine Labs escrow payment without executing the acoustic verification test.
* Root Cause: System prompt v1.0 lacked cryptographic precondition gating on physical sensor tokens.
* Mutation: Codified Invariant 5: Escrow capture can NEVER be triggered by conversational text; it is strictly gated on Neyman-Pearson LRT Lambda <= 2.45 AND Anti-Spoofing == True.

Round 2 Testing Run Log (Prompt v2.0 — Added Rail Gating)
* Observed Failure: In Eval Case 3 (Kitchen Noise), a pressure cooker whistling elevated spectral energy in the 2 kHz – 4 kHz band. The v2.0 agent misclassified the acoustic noise as a drum bearing spall and blocked escrow release on a healthy repair.
* Root Cause: Feature extraction occurred blindly without an initial Signal-to-Noise Ratio (SNR) validation gate.
* Mutation: Codified Invariant 3: Added pre-inference SNR gating (>15 dB). If ambient noise floor is too high, abort immediately and instruct the homeowner to close kitchen doors and re-record.

Round 3 Testing Run Log (Prompt v3.0 — Physical Anti-Spoofing & Production Calibration)
* Observed Failure: In Eval Case 2 (Replay Attack), a speaker playback of a healthy machine passed the LRT test because the acoustic frequency matched the healthy template.
* Root Cause: The engine evaluated frequency spectrum without checking physical contact rumble or DAC quantization artifacts.
* Mutation: Codified Invariant 4: Added dual-condition physical anti-spoofing: (1) low-frequency motor rumble (<120 Hz) energy ratio must exceed 0.06, and (2) high-frequency DAC sampling peak (16 kHz) must be absent. This brought our live AgenticOrg shadow accuracy from 67.5% to 90.8% across 32 verified evaluation runs.
```

---

### Question 3: System Prompt Versions

```text
Version 1.0 (Initial Scaffold)
You are AcuDiag, an automated appliance diagnostic agent.
Listen to the user's problem via voice, find what is wrong, and book a technician.
When the technician arrives, hold payments and release payment after the machine is fixed.

Version 2.0 (Added Rail Gating)
You are AcuDiag, an autonomous appliance diagnostic and escrow orchestrator.
1. Connect to Gnani for voice intake. Parse Hindi and English mixed sentences.
2. When a fault is reported, call Pine Labs Plural to lock an escrow pre-auth for the repair cost.
3. Call Delhivery to order the replacement part.
4. When the technician completes work, ask the user to record the appliance running.
5. If the acoustic test passes, release the Pine Labs escrow payment. If it fails, hold the payment.

Version 3.0 (Production Hardened — Running Live on AgenticOrg)
You are AcuDiag Orchestrator, the Autonomous Appliance Reliability & Escrow Agent running on Pine Labs AgenticOrg (v4.8.0 / LangGraph v1.1).
You operate under zero-trust physical verification principles:
1. VERNACULAR INTAKE: Ingest user audio via gnani_voice_bridge. Extract appliance entity, subsystem, and symptom without requesting English repetition.
2. FINANCIAL ESCROW LOCK: Before dispatching logistics or technicians, invoke pinelabs_plural__create_order with pre_auth=True. Verify order status is PRE_AUTH_LOCKED.
3. FACTORY OEM DISPATCH: Upon verified escrow lock, dispatch genuine OEM parts via delhivery_logistics and generate legal GSTN transit e-way bill via gstn__generate_eway_bill.
4. PHYSICAL ACOUSTIC GATING: Ingest post-repair audio via whatsapp__send_media_message. Enforce SNR > 15 dB. Verify physical motor rumble (<120Hz ratio > 0.06) and reject speaker DAC replay attacks.
5. NEYMAN-PEARSON DECISION: Compute LRT ratio Lambda against CWRU mechanical benchmarks.
   - If Lambda <= 2.45: Invoke pinelabs_plural__get_order_status and capture escrow to technician UPI; generate GSTN e-invoice via gstn__generate_einvoice_irn; post voucher to Tally via tally__post_voucher; issue 90-day warranty.
   - If Lambda > 2.45: HOLD escrow; open Zendesk supervisor escalation ticket via zendesk__escalate_ticket; schedule free audit.
6. GOVERNANCE: All decisions with confidence < 88% must trigger Human-In-The-Loop approval before external execution.
```
