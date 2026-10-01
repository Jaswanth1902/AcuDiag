# 🎬 AcuDiag: Second-by-Second Video Recording Plan & Script (120s / 2:00)

> **Submission Target**: The Ken & Pine Labs AgenticOrg Case Competition  
> **Platform Core**: Pine Labs AgenticOrg (`v4.8.0`) + Gnani.ai + Delhivery OS1 + Pine Labs Plural  
> **Target Video Runtime**: **120 Seconds (2:00)** [Maximum ceiling: 2:15]  
> **Resolution & Framerate**: 1080p, 60 FPS (16:9)  
> **Audio Strategy**: **Founder Natural Voice** for pitch narration; **Gnani STT** demonstrated live in-app for Hindi/English voice note processing.  
> **Visual Composition**: **70% Pine Labs AgenticOrg** (The Brain/Orchestrator) + **30% Cockpit HUD (`localhost:8000`)** (Physical Acoustic Reality).

---

## 🧭 Executive Directives & Answers to Core Strategic Questions

### 1. Should you show only AgenticOrg, or keep both AgenticOrg and Cockpit HUD?
* **Verdict: Keep BOTH, but enforce strict 70/30 hierarchy.**
* **Why**: The Pine Labs webinar (Prakhar Gour & Shubham) explicitly stated that judging centers on AgenticOrg adoption (agent configuration, connectors, shadow evals, confidence thresholds, and HITL approvals). If you only show a localhost UI, judges will penalize you for bypassing their platform. However, if you *only* show AgenticOrg, the physical acoustic waveforms, the 64-channel Gammatone filterbanks, and the live replay attack rejection are hidden in JSON payloads.
* **The Winning Formula**: Use AgenticOrg as the command orchestrator (0:00–1:05), flip to Cockpit HUD for 30 seconds (1:05–1:35) to showcase the physical acoustic reality and anti-spoofing defense, and return to AgenticOrg (1:35–2:00) for the final escrow capture, IRN invoicing, and audit trail.

### 2. Natural Voice vs. Gnani Synthetic Voiceover?
* **Verdict: 100% Natural Voice for narration; Feature Gnani live in-app.**
* **Why**: Synthetic TTS narration across an entire 2-minute pitch sounds flat, generic, and unconvincing to senior judges. Human enthusiasm and executive authority close competitions. You showcase Gnani where it truly shines: transcribing vernacular customer voice notes (Hindi/Hinglish) inside the diagnostic pipeline.

### 3. Video Duration & Cap
* **Verdict: 120 Seconds (2:00) Hard Cap.**
* **Why**: The official cap is 3 minutes (180s), but judge fatigue is real. A dense, high-tempo, 120-second video with zero filler, crisp transitions, and hard empirical numbers scores in the top 1%.

---

## ⏱️ Master Second-by-Second Breakdown (0:00 – 2:00)

| Timestamp | Screen / Interface | What to Click / Show | Spoken Narration (Natural Voice) |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:15** (15s) | **Pine Labs AgenticOrg** (Agent Dashboard) | Start on `agenticorg.hackathon.pinelabs.com`, displaying agent `AcuDiag Reliability Orchestrator`. Cursor highlights status: `Active`. | *"In India, over ₹18,000 Crores are lost annually to home appliance repair fraud—unnecessary part replacements, fake fixes, and unverified charges. Meet AcuDiag: the Autonomous Appliance Reliability and Escrow Orchestrator built natively on Pine Labs AgenticOrg."* |
| **0:15 – 0:40** (25s) | **AgenticOrg Agent Details & Metrics** | Scroll to **Agent Overview**: Highlight **25 Shadow Samples**, **89.6% Shadow Accuracy** (well above the 65% floor), **0 Pending Approvals**, and the **8 Registered Tools**. | *"Running natively inside AgenticOrg, AcuDiag has completed 25 shadow evaluation runs with an 89.6% accuracy score. We’ve integrated 8 production tools spanning Pine Labs Plural Escrow, Gnani speech intelligence, Delhivery logistics, and GSTN e-invoicing, governed by an 88% confidence threshold."* |
| **0:40 – 1:05** (25s) | **AgenticOrg Live Execution Trace** | Click on a recent execution run (e.g., Ticket #1042 / Washing Machine). Show inbound prompt, Gnani vernacular STT transcription, and agent dispatching `pinelabs_preauth_escrow` locking ₹1,250. | *"When a Bengaluru customer reports a violent washing machine noise, AcuDiag ingests her vernacular voice memo via Gnani STT. The agent diagnoses a drum bearing spall and immediately invokes Pine Labs Plural to lock a ₹1,250 pre-auth escrow, guaranteeing funds before dispatching genuine OEM parts via Delhivery."* |
| **1:05 – 1:25** (20s) | **Cockpit HUD (`localhost:8000`)** | Switch tab to Cockpit HUD. Click **Ticket #1042 (Priya Sharma)**. Point cursor to: (1) 64-channel Gammatone filterbank, (2) CWRU 1,450 Hz fault peak, (3) Neyman-Pearson LRT ratio ($\Lambda=3.88 > 2.45$). | *"Under the hood, AcuDiag uses physical acoustic reality. Using 64-channel Gammatone filterbanks and Neyman-Pearson hypothesis testing, it isolates the exact 1,450 Hz bearing spall from heavy kitchen noise at 18.4 dB SNR, matching CWRU mechanical benchmarks with zero guesswork."* |
| **1:25 – 1:35** (10s) | **Cockpit HUD (`localhost:8000`)** | Click **Ticket #1045 (Rajesh Kumar)** in the inbox queue. Flash the bold red alert: 🚨 **REPLAY ATTACK FRAUD BLOCKED**. | *"Even better, our zero-trust anti-spoofing engine blocks technician fraud. When a technician played a recorded sound from his phone speaker, AcuDiag detected the 16 kHz DAC jitter and lack of physical sub-120Hz motor rumble, locking the payout instantly."* |
| **1:35 – 1:55** (20s) | **Pine Labs AgenticOrg** (Closed Loop & Audit) | Switch back to AgenticOrg. Show the post-repair verification run: LRT $\Lambda=0.82 \le 2.45$, `pinelabs_capture_escrow` releasing ₹1,250 to technician UPI, `gstn_einvoice_generate` producing verified IRN, and 0 pending HITL items. | *"Once the repair is completed, the customer runs a 10-second verification spin. The fault harmonic drops below threshold, and AcuDiag autonomously captures the Plural escrow to the technician's UPI, generates a legal GSTN e-invoice, and issues a 90-day warranty—all audited transparently inside AgenticOrg."* |
| **1:55 – 2:00** (5s) | **Pine Labs AgenticOrg** (Logo / Overview) | Pan back to the AgenticOrg Command Center view with all systems green. | *"AcuDiag replaces broken human trust with mathematical certainty. Built for India, powered by Pine Labs AgenticOrg. Thank you."* |

---

## 🛠️ Step-by-Step Recording Preparation Checklist

### Step 1: Prepare the Browser Windows (Before Recording)
1. **Window 1 (Tab 1)**: Open `https://agenticorg.hackathon.pinelabs.com/dashboard/agents/c56edea9-8cd1-4e31-bf93-48e024d445d5`.
   - Verify metrics display: **Shadow Samples: 25**, **Shadow Accuracy: 89.6%**, **Approvals: 0**.
   - Zoom to 110% so text and numbers are sharp and readable.
2. **Window 1 (Tab 2)**: Open `http://localhost:8000/`.
   - Ensure `python 01_Projects/AcuDiag/databank/03_Mock_Server/mock_server.py` is running.
   - Maximize full-screen (`F11` or full window).
   - Have Ticket #1042 loaded, with Ticket #1045 one click away.

### Step 2: OBS / Screen Recorder Settings
- **Canvas Resolution**: 1920x1080 (1080p).
- **Framerate**: 60 FPS (smooth scrolling and cursor tracking).
- **Audio Input**: USB Microphone with noise gate (no fan noise).
- **Hotkey**: Use `Ctrl+F1` to Start, `Ctrl+F2` to Stop.

### Step 3: Rehearsal Run
- Do one 120-second dry run with a stopwatch.
- If you run over 2:05, trim 2–3 words per sentence.
- If you run under 1:50, slow down pacing on the Gammatone filterbank and escrow capture explanation.

---

## 🏆 Scoring Rubric Alignment (Why This Wins)

| Judging Criteria | How the 120s Demo Demonstrates It | Evidence Shown |
| :--- | :--- | :--- |
| **Platform Adoption** | 70% screen time on Pine Labs AgenticOrg; uses shadow evals, prompts, and connectors | 25 samples, 89.6% accuracy, 8 tools |
| **Technical Depth** | Physical DSP (Gammatone 64-ERB, Neyman-Pearson LRT, DAC jitter anti-spoofing) | Live waveform & spectrogram in Cockpit HUD |
| **Business Impact** | Addresses ₹18,000 Cr repair fraud via Plural escrow pre-auth & post-repair release | Pine Labs Plural API calls, GSTN IRN |
| **Multi-Lingual Reach** | Seamless handling of Hindi/English vernacular audio via Gnani STT | Ticket #1042 voice intake transcription |
| **Zero-Trust Security** | Catches dishonest technicians replaying audio or faking repairs | Ticket #1045 Replay Fraud Block banner |
