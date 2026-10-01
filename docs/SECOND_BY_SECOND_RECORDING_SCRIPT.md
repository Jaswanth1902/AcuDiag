# 🎬 AcuDiag: 100% Native Pine Labs AgenticOrg Video Recording Script (120s / 2:00)
### *A Live, Zero-Distraction Customer Journey Walkthrough Exclusively Inside AgenticOrg*

> **Submission Target**: The Ken & Pine Labs AgenticOrg Case Competition (₹20 Lakhs Prize Pool)  
> **Platform Runtime**: **100% Pine Labs AgenticOrg** (`agenticorg.hackathon.pinelabs.com`)  
> **Target Video Runtime**: **120 Seconds (2:00)** [Strict maximum: 2:15]  
> **Screen Recording Target**: **Single Browser Window** locked to `https://agenticorg.hackathon.pinelabs.com` (Zero external tabs, zero localhost)  
> **Resolution & Framerate**: 1080p, 60 FPS (16:9), Browser Zoom: 110%  
> **Audio Strategy**: **Founder Natural Voice** for pitch narration (clear, energetic, authoritative).

---

## 🧭 The 100% Native Strategic Advantage

### Why scrap the external Cockpit HUD entirely?
1. **Zero Extraneous Surface Area**: The jury is comprised of Pine Labs platform leadership (Prakhar Gour, Shubham) and The Ken editors. Showing an external `localhost:8000` website risks making them think the logic lives outside their platform.
2. **100% Platform Fidelity**: By staying exclusively inside `agenticorg.hackathon.pinelabs.com`, every second of video proves mastery of their flagship product—Agent Settings, Knowledge Base RAG, Connector Registries, Live Run Traces, HITL Approvals, and Execution Auditing.
3. **Exact Alignment with Submission Questions**: Demonstrates the 6 chronological decisions directly inside the AgenticOrg execution trace.

---

## ⏱️ Master Second-by-Second Flow (0:00 – 2:00)

```
0:00        0:20                  0:45                  1:10                  1:40                  2:00
|-- Hook ---|-- Knowledge Base ---|-- Live Run Trace:---|-- Acoustic Verification|-- Settlement & -----|
| & Agent   |   & RAG Grounding   |   Escrow Lock &     |   & Anti-Spoof Rejection|  HITL Governance    |
| Overview  |   (Prakhar's SRE)   |   Delhivery Dispatch|   (Decisions 4 & 5)   |  (Dec 6 & Outro)    |
```

---

### Phase 1: The Problem & The Agent Command Center (0:00 – 0:20 | 20s)
* **Screen**: **AgenticOrg Dashboard $\rightarrow$ AcuDiag Agent Page** (`/dashboard/agents/c56edea9-8cd1-4e31-bf93-48e024d445d5`).
* **Visual Action**:
  - Show agent name: **AcuDiag Reliability Orchestrator**.
  - Highlight the status pill: `Active` / `shadow`.
  - Cursor highlights key metrics: **25 Shadow Samples**, **89.6% Accuracy**, **0 Pending Approvals**, and the **88% Confidence Threshold**.
* **Founder Narration (Natural Voice)**:
  > *"In India, over ₹18,000 Crores are lost annually to home appliance repair fraud—unnecessary part replacements, fake fixes, and unverified charges. Meet AcuDiag: the Autonomous Reliability and Escrow Orchestrator built natively on Pine Labs AgenticOrg. Following Prakhar Gour’s single-agent multi-connector paradigm, AcuDiag unifies 14 enterprise tools into one deterministic engine. Notice our calibrated 89.6% moving accuracy across 25 shadow evaluation runs."*

---

### Phase 2: Vector Knowledge Base Grounding (0:20 – 0:40 | 20s)
* **Screen**: **AgenticOrg Knowledge Base Page / Drawer** (`/dashboard/knowledge`).
* **Visual Action**:
  - Open `acudiag_appliance_specs.md` in the knowledge base list.
  - Highlight the acoustic fault frequency profiles: 1,450 Hz for Washing Machine Bearing Spalls, 320 Hz for Drain Pump Cavitation, OEM part SKU `BEAR-6205-2RS`, and standardized ₹1,250 labor/parts cost matrix.
* **Founder Narration**:
  > *"To eliminate LLM hallucination, AcuDiag grounds every decision in an uploaded appliance engineering knowledge base. Through vector retrieval, the agent references mechanical fault kinematics—such as 1,450 Hz drum bearing spalls—and pre-negotiated OEM part pricing before taking any external action."*

---

### Phase 3: Live Incident Execution — Escrow Lock & Logistics (0:40 – 1:10 | 30s)
* **Screen**: **AgenticOrg Agent Run / Execution Trace View** (Ticket #1042 — Priya Sharma).
* **Visual Action**:
  - Scroll through the input prompt: Shows Priya's vernacular voice intake via Gnani STT (*"Washing machine spin karte waqt tezz kharr-kharr awaz aa rahi hai..."*).
  - Highlight **Tool Call 1**: `pinelabs_plural__create_order` (`pre_auth: true`, amount: `125000`). Show order `PL_ORD_8A92B1C4` confirmed in `PRE_AUTH_LOCKED` status.
  - Highlight **Tool Call 2**: `gstn__generate_eway_bill` & `delhivery_logistics` dispatching OEM bearing SKU `BEAR-6205-2RS` directly to Priya's doorstep.
* **Founder Narration**:
  > *"Here is a live execution run for customer Priya in Bengaluru. Ingesting her Hinglish voice memo via Gnani STT, AcuDiag diagnoses a drum bearing failure. Operating under zero-trust, the agent invokes Pine Labs Plural to lock a ₹1,250 pre-auth escrow hold. Guaranteeing funds before anyone leaves the house, AcuDiag generates a legal GSTN e-way bill and manifests factory OEM bearings directly to her doorstep via Delhivery."*

---

### Phase 4: Acoustic Verification & Anti-Spoof Rejection (1:10 – 1:35 | 25s)
* **Screen**: **AgenticOrg Post-Repair Run Trace & Adversarial Run Contrast**.
* **Visual Action**:
  - Show the post-repair telemetry evaluation in the trace:
    `SNR: 23.8 dB` (passes 15 dB floor), `Neyman-Pearson LRT: Lambda = 0.38 <= 2.45` (PASS: bearing harmonic absent).
  - Quick scroll / click to the adversarial evaluation run (Ticket #1045):
    Show the agent response: `REJECTED_REPLAY_ATTACK`. Anti-spoofing caught 16 kHz DAC jitter and lack of physical sub-120Hz motor rumble from a technician's phone speaker, blocking payout and triggering `zendesk__escalate_ticket`!
* **Founder Narration**:
  > *"When the technician finishes, Priya runs a 10-second verification spin. In the execution trace, AcuDiag evaluates physical acoustic telemetry: the Neyman-Pearson score drops to 0.38, well below our 2.45 threshold, mathematically proving the fault is eliminated. In an adversarial run where a technician played a recorded sound from his phone speaker, AcuDiag’s anti-spoofing engine detected 16 kHz DAC jitter, blocked the payout, and escalated the fraud to Zendesk."*

---

### Phase 5: Closed-Loop Settlement, E-Invoicing & Ledger Sync (1:35 – 1:52 | 17s)
* **Screen**: **AgenticOrg Tool Output Trace** (End of Successful Run).
* **Visual Action**:
  - Point to the final sequence of automated tool executions:
    1. `pinelabs_plural__get_order_status` $\rightarrow$ Captures ₹1,250 to technician Suresh Kumar's UPI.
    2. `gstn__generate_einvoice_irn` $\rightarrow$ Government IRN generated (`4b8d7a...`).
    3. `whatsapp__send_media_message` $\rightarrow$ 90-day warranty certificate dispatched to customer.
    4. `tally__post_voucher` $\rightarrow$ Repair expense synced into merchant Tally ledger.
* **Founder Narration**:
  > *"With physical clearance confirmed, AcuDiag executes full financial closure inside AgenticOrg: capturing the Plural escrow to the technician's UPI, generating a legal GSTN e-invoice IRN, dispatching the warranty certificate via WhatsApp, and posting the voucher into Tally—completely autonomous, transparent, and auditable."*

---

### Phase 6: Human-In-The-Loop Governance & Outro (1:52 – 2:00 | 8s)
* **Screen**: **AgenticOrg Approvals Dashboard** (`/dashboard/approvals`).
* **Visual Action**:
  - Show **Pending Approvals: 0**, showing that all 20 historical edge cases were reviewed, elevating moving accuracy to 89.6%.
  - Pan back to the Agent Overview with all systems green.
* **Founder Narration**:
  > *"With zero pending approvals and an 88% confidence floor, AcuDiag turns broken human trust into mathematical and financial certainty. Built for India, 100% native on Pine Labs AgenticOrg. Thank you."*

---

## 🎬 3-Minute Quick Setup Guide for Recording

1. **Open Chrome**: Navigate to `https://agenticorg.hackathon.pinelabs.com/dashboard/agents/c56edea9-8cd1-4e31-bf93-48e024d445d5`.
2. **Browser Layout**:
   - Set zoom to **110%** (so metrics and tool names are crisp).
   - Have the Agent Page open. In another tab (for your own reference only), you can see the run trace, but during recording, you stay entirely within the AgenticOrg UI!
3. **OBS / Recorder Settings**:
   - Capture Mode: **Window Capture** (Chrome: AgenticOrg).
   - Resolution: 1920x1080 (1080p), 60 FPS.
4. **Recording Flow**:
   - Start on Agent Overview (0:00).
   - Click Knowledge Base (0:20).
   - Click Runs / Recent Execution Trace for Ticket #1042 (0:40).
   - Show Telemetry & Fraud rejection in trace (1:10).
   - Show Closed-Loop Tool Outputs (1:35).
   - Click Approvals tab showing 0 pending (1:52).
   - Finish on Agent Overview at exactly 2:00!
