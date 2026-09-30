# 🎥 AcuDiag Enterprise Operations Desk Screen Recording Guide

> **Target URL**: `http://localhost:8000/` (or `http://127.0.0.1:8000/`)  
> **Platform Runtime**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`)  
> **Target Video Length**: 2 to 3 minutes (1080p, 60 FPS)  
> **Interface Layout**: 3-Pane Enterprise Workspace (Incident Queue $\rightarrow$ WhatsApp Simulator $\rightarrow$ Forensic Telemetry & Audit Inspector)  

---

## 1. Setup & Pre-Recording Checklist
1. Start the mock server: `python 01_Projects/AcuDiag/databank/03_Mock_Server/mock_server.py`
2. Open Chrome to `http://localhost:8000/`.
3. Press `F11` (or maximize full screen) so the 3-Pane Enterprise Console fills the display.
4. Verify all 6 incidents are visible in Pane 1 (Priya, Vikram, Ananya, Rajesh, Amit, Sunita).

---

## 2. 90–120 Second Video Narration Flow

### Scene 1: The Enterprise Fleet Command Overview (15–20 Seconds)
* **What to Show**: Pan across the full 3-Pane workspace.
* **Narration**:
  > *"Welcome to AcuDiag, the Autonomous Appliance Reliability & Escrow Orchestrator built on Pine Labs AgenticOrg, Gnani.ai, and Delhivery OS1. Instead of a toy demo chatbot, this is an authentic Enterprise Operations Desk managing active repair incidents across India in real time."*

---

### Scene 2: The Primary Happy Path — Ticket #1042 (Priya Sharma) (45 Seconds)
* **What to Click**: Click on **Ticket #1042 (Priya Sharma)** in the left inbox.
* **What to Show**: 
  - Center pane: Voice note in Hindi (*"Washing machine spin karte waqt..."*), diagnostic report card showing ₹1,250 quote (Part ₹850 + Labor ₹400).
  - Tapping "Approve & Lock Escrow" $\rightarrow$ Pine Labs order `PL_ORD_8A92B1C4` pre-auth locked.
  - Delhivery waybill `DEL16100984210` manifested from Godrej Peenya Hub.
  - Post-repair spin test $\rightarrow$ Neyman-Pearson LRT passes ($\Lambda=0.38 \le 2.45$), Anti-spoof passes.
  - Escrow released to technician Suresh Kumar via UPI, 90-day warranty issued.
* **Narration**:
  > *"In Ticket #1042, Priya in Bengaluru reports a violent drum screech. AcuDiag analyzes her smartphone microphone stream via Gnani STT and our DSP engine, identifying a CWRU-grounded 1,450 Hz drum bearing spall. AcuDiag locks ₹1,250 in a Pine Labs Plural pre-auth escrow and dispatches genuine OEM bearings via Delhivery. When the technician finishes, Priya runs a 10-second spin test. AcuDiag mathematically confirms the fault harmonic is gone, releases the payout to the technician's UPI, and delivers a 90-day warranty."*

---

### Scene 3: Technician Replay Fraud Caught — Ticket #1045 (Rajesh Kumar) (20 Seconds)
* **What to Click**: Click on **Ticket #1045 (Rajesh Kumar)** in the inbox.
* **What to Show**: Notice the red alert banner: 🚨 **REPLAY ATTACK FRAUD BLOCKED**.
* **Narration**:
  > *"Now watch our zero-trust security guardrails in Ticket #1045. A technician in Mumbai attempted fraud by playing a pre-recorded healthy sound through his smartphone speaker. AcuDiag's anti-spoofing engine detected the 16kHz DAC quantization jitter and the complete absence of physical motor rumble (<120Hz). The payout was instantly blocked, protecting the customer from fraud."*

---

### Scene 4: Fake / Incomplete Repair Caught — Ticket #1046 (Amit Verma) (15 Seconds)
* **What to Click**: Click on **Ticket #1046 (Amit Verma)**.
* **What to Show**: Red banner: 🚨 **FAKE REPAIR DETECTED (LRT FAILED)**.
* **Narration**:
  > *"In Ticket #1046, technician Manoj claimed a drain pump was fixed. But on the post-repair test, the 820 Hz impeller screech harmonic was still present (LRT 8.42 vs 2.45 threshold). AcuDiag refused to release the escrow and queued a supervisor audit."*

---

### Scene 5: Ambient Noise & User Protection — Ticket #1044 & #1043 (15 Seconds)
* **What to Click**: Click on **Ticket #1044 (Ananya)** or **#1043 (Vikram)**.
* **What to Show**: 
  - Ticket #1044: Amber banner 🚨 **LOW SNR (KITCHEN NOISE)** showing 9.4 dB SNR rejected.
  - Ticket #1043: Slate banner ⏸️ **QUOTE DECLINED** showing the user declined ₹4,600 and was not charged.
* **Narration**:
  > *"When background pressure cookers drown out the signal as in Ticket #1044, AcuDiag rejects the test rather than guessing. And when customer Vikram declined the ₹4,600 quote in Ticket #1043, the agent gracefully paused without charging his card."*

---

### Scene 6: Live Interaction & Conclusion (10 Seconds)
* **What to Do**: Type a live message in the WhatsApp input bar or click a quick action button.
* **Narration**:
  > *"AcuDiag re-wires home appliance servicing from broken human trust into verifiable physical reality. Thank you."*

---

## 3. Submission Export
- Export video to `G:\My Drive\Ken_Evidences\AcuDiag_PineLabs_AgenticOrg_Demo.mp4`.
- Paste the Google Drive public link into The Ken submission portal alongside `FINAL_SUBMISSION_PACK.md`.
