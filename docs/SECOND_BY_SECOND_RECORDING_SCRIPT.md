# 🎬 AcuDiag: Story-Driven Customer Flow Video Recording Script (120s / 2:00)
### *A Live End-to-End Walkthrough of Ticket #1042 (Priya Sharma) on Pine Labs AgenticOrg*

> **Submission Target**: The Ken & Pine Labs AgenticOrg Case Competition (₹20 Lakhs Prize Pool)  
> **Platform Core**: Pine Labs AgenticOrg (`v4.8.0`) + Gnani.ai + Delhivery OS1 + Pine Labs Plural  
> **Target Video Runtime**: **120 Seconds (2:00)** [Strict maximum: 2:15]  
> **Video Style**: **Live Customer Journey Walkthrough** (Demonstrating Decisions 1 to 6 from our submission).  
> **Audio Strategy**: **Founder Natural Voice** for pitch narration; **Gnani STT** customer voice note audio played live.  
> **Visual Composition**: **75% Pine Labs AgenticOrg** (The Orchestrator Brain) + **25% Cockpit HUD (`localhost:8000`)** (WhatsApp Customer Interaction & Acoustic Waveform).

---

## 💡 Executive Verdict: Customer Flow vs. Overview Video

### Should the video be a high-level overview, or demonstrate the actual customer flow?
* **Verdict: It MUST be an active Customer Flow Walkthrough.**
* **Why**: 
  1. The Ken submission form Question 2 explicitly asks: **"Every Decision the Agent Makes in the Recording (Chronological Decision Log)"**.
  2. If the video is just a generic overview of settings, the judges will wonder if the agent actually works.
  3. By walking through **Priya Sharma's Washing Machine Repair (Ticket #1042)** from the first voice memo to the final UPI payout, you prove that AcuDiag actually runs end-to-end, making every single decision live on screen!

---

## ⏱️ Master Second-by-Second Flow (0:00 – 2:00)

```
0:00        0:15                  0:40                  1:05                  1:35                  1:55     2:00
|-- Hook ---|-- Inbound Voice ----|-- Escrow Lock & ----|-- Physical Acoustic-|-- Closed-Loop Payout|-- Outro |
| & AgenticOrg | & Knowledge RAG  |   Delhivery Dispatch|   Verification &    |   & GSTN / Tally    | & Metrics|
| Overview  | (Decision 1)        |   (Decisions 2 & 3) |   Anti-Spoof (Dec 4)|   (Decisions 5 & 6) | (Proof) |
```

---

### Phase 1: The Problem & The Brain (0:00 – 0:15 | 15s)
* **Screen**: **Pine Labs AgenticOrg Dashboard** (`agenticorg.hackathon.pinelabs.com`).
* **Visual Action**: Show the active AcuDiag agent in AgenticOrg. Cursor highlights the status `Active`, 25 shadow runs, and the 14 native connectors.
* **Founder Narration (Natural Voice)**:
  > *"Over ₹18,000 Crores are lost every year in India to home appliance repair fraud. Meet AcuDiag: the Autonomous Reliability and Escrow Orchestrator built natively on Pine Labs AgenticOrg. Let's watch AcuDiag resolve a live customer incident in real time."*

---

### Phase 2: Customer Voice Intake & RAG Quote (0:15 – 0:38 | 23s)
* **Screen**: Split view / quick cut to **Cockpit HUD WhatsApp Pane** (`localhost:8000`) $\rightarrow$ back to **AgenticOrg Trace**.
* **Visual Action**: Click **Ticket #1042 (Priya Sharma)**. Play/show the 3-second Hinglish voice note:
  > *Customer Audio*: *"Washing machine spin karte waqt tezz kharr-kharr awaz aa rahi hai..."*
  Show Gnani STT transcribing the vernacular audio with sub-350ms latency.
  Switch to AgenticOrg showing the prompt trace: AcuDiag queries the vector Knowledge Base (`acudiag_appliance_specs.md`), identifies `WM_BEARING_SPALL`, and generates the ₹1,250 quote (₹850 part + ₹400 labor).
* **Founder Narration**:
  > *"In Bengaluru, customer Priya reports a violent spin screech. Ingesting her Hinglish voice memo via Gnani STT, AcuDiag consults its appliance knowledge base, isolates a drum bearing spall, and issues a standardized ₹1,250 quote directly over WhatsApp."*

---

### Phase 3: Zero-Trust Escrow Lock & OEM Logistics (0:38 – 1:02 | 24s)
* **Screen**: **AgenticOrg Live Execution Trace** & **WhatsApp Simulator**.
* **Visual Action**: Priya taps *"Approve & Lock Escrow"* on WhatsApp.
  Show AgenticOrg dispatching `pinelabs_plural__create_order` (`pre_auth: true`).
  Order `PL_ORD_8A92B1C4` locks ₹1,250 in Pine Labs Plural escrow.
  Show agent immediately dispatching `delhivery_logistics` (Waybill `DEL16100984210`) manifesting genuine OEM bearing SKU `BEAR-6205-2RS` from Godrej Peenya Hub, and generating a GSTN e-way bill.
* **Founder Narration**:
  > *"When Priya approves, AcuDiag calls Pine Labs Plural to lock a ₹1,250 pre-auth escrow hold. Guaranteeing funds before anyone leaves the house, AcuDiag generates a GSTN e-way bill and dispatches genuine factory OEM bearings directly to her doorstep via Delhivery."*

---

### Phase 4: Physical Acoustic Test & Replay Fraud Block (1:02 – 1:30 | 28s)
* **Screen**: **Cockpit HUD Acoustic & Anti-Spoofing Inspector** (`localhost:8000`).
* **Visual Action**: Technician Ramesh installs the bearing. Priya runs a 10-second spin test.
  Point cursor to the 64-channel Gammatone filterbank waterfall and the Neyman-Pearson LRT score: $\Lambda = 0.38 \le 2.45$ (GREEN PASS: fault frequency eliminated).
  **The Fraud Contrast (5s)**: Click **Ticket #1045 (Rajesh Kumar)** in the inbox. Flash the bold red banner: 🚨 **REPLAY ATTACK FRAUD BLOCKED**! Point to the 16kHz DAC quantization jitter.
* **Founder Narration**:
  > *"Post-repair, Priya records a 10-second spin test. Our edge DSP engine runs 64-channel Gammatone filterbanks and Neyman-Pearson hypothesis testing, mathematically proving the fault harmonic is gone. And in Ticket #1045, when a technician tried playing a recorded sound from his phone speaker, our anti-spoofing engine detected 16 kHz DAC jitter, blocking payout fraud instantly."*

---

### Phase 5: Closed-Loop Payout, GSTN IRN & Ledger Sync (1:30 – 1:52 | 22s)
* **Screen**: **Pine Labs AgenticOrg Closed-Loop Trace**.
* **Visual Action**: Show the AgenticOrg execution log completing the full back-office closure:
  1. `pinelabs_plural__get_order_status` captures the ₹1,250 escrow hold to technician Suresh Kumar's UPI.
  2. `gstn__generate_einvoice_irn` creates the government-verified IRN tax invoice.
  3. `whatsapp__send_media_message` dispatches the 90-day warranty certificate to Priya's WhatsApp.
  4. `tally__post_voucher` synchronizes the repair expense into the merchant's Tally ledger.
* **Founder Narration**:
  > *"With the acoustic test verified, AcuDiag triggers the complete financial settlement inside AgenticOrg: capturing the Plural escrow to the technician's UPI, generating a legal GSTN e-invoice IRN, delivering a 90-day warranty certificate over WhatsApp, and posting the voucher into Tally."*

---

### Phase 6: Conclusion & Platform Metrics (1:52 – 2:00 | 8s)
* **Screen**: **Pine Labs AgenticOrg Fleet Dashboard**.
* **Visual Action**: Pan across the clean metrics: **25 Shadow Samples**, **89.6% Accuracy**, **0 Pending Approvals**, and the **88% Confidence Threshold**.
* **Founder Narration**:
  > *"With 25 shadow evaluations and 89.6% accuracy, AcuDiag turns broken human trust into mathematical and financial certainty. Powered by Pine Labs AgenticOrg. Thank you."*

---

## 🎬 Practical Recording Checklist for Jaswanth

1. **Browser Tab 1**: `https://agenticorg.hackathon.pinelabs.com/dashboard/agents/c56edea9-8cd1-4e31-bf93-48e024d445d5` (Zoomed to 110%).
2. **Browser Tab 2**: `http://localhost:8000/` (Full screen `F11`, Ticket #1042 ready).
3. **Audio Setup**: Plug in your headset or USB mic. Speak with energy, pacing your words clearly.
4. **Transition**:
   - `0:00 - 0:15`: On AgenticOrg.
   - `0:15 - 0:38`: Switch to Cockpit HUD WhatsApp pane to show Priya's ticket and audio note.
   - `0:38 - 1:02`: Back to AgenticOrg to show the Plural pre-auth escrow call and Delhivery dispatch.
   - `1:02 - 1:30`: Switch to Cockpit HUD to show the acoustic waveform & Ticket #1045 replay fraud block.
   - `1:30 - 2:00`: Return to AgenticOrg for the final escrow capture, GSTN IRN, and dashboard metrics.
