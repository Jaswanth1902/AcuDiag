# 🚀 AcuDiag: 3 Parallel Session Execution Architecture & Master Prompts

> **Project**: AcuDiag (Problem Space #9: Keeping the Machines Running — The Ken Case-Build 2026)  
> **Platform**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`) • Org: `Ken's Case Competition`  
> **Tenant ID**: `abb61bca-a3f5-4aba-b30e-946016b13120` • Account: `K.Sai Jaswanth Reddy`  
> **Root Directory**: `C:\Users\jaswa\Antigravity\01_Projects\AcuDiag`

---

## 0. Shared Context Block (Include at top of every session)

```text
PROJECT CONTEXT & REPOSITORY RULES:
- Workspace: C:\Users\jaswa\Antigravity\01_Projects\AcuDiag
- Competition: The Ken Case-Build 2026 (Round 3 Build Stage)
- Partner Rails: Gnani.ai (Voice: STT/TTS), Pine Labs (Escrow: Pre-auth/Capture), Delhivery (Logistics: CMU Forward/Reverse)
- Platform: Pine Labs AgenticOrg (Tenant: abb61bca-a3f5-4aba-b30e-946016b13120, user: ksaijaswanthr.cs24@rvce.edu.in)
- Invariants: Pure Python stdlib where possible, CREATE_NO_WINDOW for subprocesses, strict zero-mock physical reality.
- Credentials: Read from credentials/credentials.env (never commit raw secrets).
```

---

## 1. 🔬 SESSION A: Acoustic Physics & Sub-5ms DSP Core

### Purpose & Scope
Owns the mathematical signal processing engine: Butterworth 4th-order SOS filter, 64-dimension Gammatone ERB filterbank, Neyman-Pearson Likelihood Ratio Test (LRT) classifier, Replay Anti-Spoofing engine, and Pass^k multi-trial benchmark harness.

### Copy-Paste Prompt for Session A
```text
You are Lead Acoustic Engineer for AcuDiag (Session A: DSP & Acoustic Math Engine).
Your mission is to harden, calibrate, and benchmark the core mathematical acoustic diagnostic pipeline.

PRIMARY DIRECTIVES:
1. Source Ground Truth:
   - Inspect `src/audio_diagnostic.py` and `src/synthetic_acoustic_gen.py`.
   - Inspect `tests/test_audio_dsp.py`.
2. Tasks to Execute:
   A. Calibrate Neyman-Pearson LRT Decision Boundary:
      - Benchmark LRT anomaly score distribution across 100 healthy trials and 100 fault trials across all 4 appliance fault classes (WM_BEARING_SPALL, WM_DRUM_IMBALANCE, PUMP_CAVITATION, COMPRESSOR_VALVE_LEAK).
      - Guarantee false positive rate (alpha) <= 0.01 and false negative rate (beta) <= 0.02 with LRT threshold gamma = 2.45.
   B. Harden Replay Anti-Spoofing:
      - Verify discrimination of smartphone loudspeaker playback vs physical machine vibration using low-frequency physical rumble ratio (<120 Hz) and DAC high-frequency spectral flatness.
      - Ensure synthetic replay attack generator in `src/synthetic_acoustic_gen.py` produces realistic speaker impulse response.
   C. Performance & SLA Profiling:
      - Create `benchmarks/dsp_profiler.py` using cProfile and tracemalloc.
      - Measure end-to-end classification latency across 1,000 runs. Guarantee p95 latency < 5.0ms on standard CPU with zero GPU dependencies.
   D. Golden Baseline Persistence:
      - Export serialized golden reference acoustic feature vectors to `baseline_vectors/golden_baselines.json`.
3. Verification:
   - Run `pytest tests/test_audio_dsp.py -v`. All tests must pass 100%.
   - Output latency and accuracy metrics to `benchmarks/DSP_BENCHMARK_REPORT.md`.
```

---

## 2. 💼 SESSION B: 3-Rail Backbone & Platform Orchestration

### Purpose & Scope
Owns the business fabric: Pine Labs AgenticOrg platform registration, Gnani.ai STT/TTS integration, Delhivery OS1 logistics mock server with Chaos Injection, Pine Labs Plural escrow pre-auth/capture lifecycle, Central SQLite WAL Blackboard event hub, and 10 adversarial eval scenarios.

### Copy-Paste Prompt for Session B
```text
You are Lead Backend & Rails Orchestrator for AcuDiag (Session B: 3-Rail Backbone & AgenticOrg Hub).
Your mission is to establish the end-to-end business state machine linking Gnani, Pine Labs, and Delhivery on the Pine Labs AgenticOrg platform.

PRIMARY DIRECTIVES:
1. Source Ground Truth:
   - Inspect `databank/03_Mock_Server/mock_server.py`.
   - Inspect `src/pinelabs_agentic_bridge.py` and `src/gnani_voice_client.py`.
   - Inspect `databank/04_Eval_Cases_and_Logs/AcuDiag_10_Eval_Cases_and_System_Prompts.md`.
   - Inspect `databank/05_Final_Submission_Dossier/The_Ken_Round_3_Master_Submission_Dossier.md`.
2. Tasks to Execute:
   A. Public Exposure & Mock Server Hardening:
      - Ensure `mock_server.py` implements all official Delhivery endpoints (/api/cmu/create.json, /api/cmu/pincode, /fm/request/new/, /api/v1/packages/json/) and Pine Labs Plural (/api/pay/v1/orders, /capture, /refund) with 4 Chaos Injection modes (no_rider, low_balance, timeout, malformed).
      - Add FastMCP or custom REST connector endpoint discoverable by Pine Labs AgenticOrg.
      - Provide a tunnel launcher script `scripts/start_tunnel.py` (using ngrok or cloudflared) so the mock server has a live public HTTPS URL.
   B. Central Data Fabric (State Machine Hub):
      - Build `src/blackboard_hub.py` using SQLite WAL mode (.cache/blackboard.sqlite).
      - Implement the 9 Happy States (ONBOARDING -> INTAKE -> ACOUSTIC_CAPTURE -> FAULT_CLASSIFIED -> ESCROW_LOCKED -> PARTS_DISPATCHED -> TECH_BOOKED -> TECH_ARRIVED -> POST_REPAIR_TEST -> ESCROW_RELEASED).
      - Implement the 4 Unhappy Flows (Warranty Intercept, Fake Repair Escrow Lock, Scope Mismatch, SNR Low).
   C. AgenticOrg Custom Connector Registration & Agent Provisioning:
      - Use `src/pinelabs_agentic_bridge.py` (or Playwright script) to register custom connectors `delhivery_acudiag` and `gnani_acudiag` on tenant `abb61bca-a3f5-4aba-b30e-946016b13120`.
      - Upload appliance knowledge base to `/dashboard/knowledge`.
      - Provision the `AcuDiag Orchestrator` virtual employee with System Prompt v3.0.
3. Verification:
   - Run `pytest tests/test_mock_server.py tests/test_eval_cases.py -v`.
   - Verify all 10 adversarial eval scenarios pass autonomously with zero human intervention.
```

---

## 3. 🎨 SESSION C: Atelier Tactical Cockpit & Chaos Telemetry HUD

### Purpose & Scope
Owns the visual interface, human-in-the-loop experience, and submission video recording flow: Emil Kowalski tactile physics, 60 FPS HTML5 WebAudio Canvas Spectrogram, interactive 9-state machine node graph, simulated escrow balance ticker, live microphone capture, and chaos injection control panel.

### Copy-Paste Prompt for Session C
```text
You are Lead UI/UX & Frontend Engineer for AcuDiag (Session C: Atelier Tactical Cockpit & Chaos HUD).
Your mission is to build the executive-grade single-page diagnostic dashboard (`public/index.html`) adhering strictly to `.agents/rules/frontend_atelier_kowalski.md` and UI/UX Pro Max standards.

PRIMARY DIRECTIVES:
1. Source Ground Truth:
   - Inspect `.agents/rules/frontend_atelier_kowalski.md`.
   - Inspect `docs/MASTER_BUILD_BLUEPRINT.md` (Stream C specifications).
   - Inspect `databank/05_Final_Submission_Dossier/The_Ken_Round_3_Master_Submission_Dossier.md`.
2. Tasks to Execute:
   A. Visual Architecture & Design Language:
      - Dark luxury aesthetic: Obsidian background (#090D16), glowing emerald telemetry (#10B981), amber escrow hold indicators (#F59E0B), crimson fraud alerts (#EF4444).
      - Emil Kowalski micro-physics: button press feedback (:active transform: scale(0.97)), custom cubic-bezier transitions, zero `transition: all`.
      - Standalone, self-contained HTML/CSS/JS (no Node/npm build dependencies; runs directly in browser or via local Python HTTP server).
   B. Core Interactive Components:
      1. 60 FPS Canvas Spectrogram: Real-time WebAudio API FFT visualizer (20 Hz - 8,000 Hz) displaying harmonic peaks and live frequency waterfall.
      2. Interactive 9-State Machine Graph: Visual SVG node graph illuminating in real-time as AcuDiag transitions from Onboarding to Escrow Released.
      3. Live Escrow Balance Ticker: Glowing Rupee counter showing pre-auth hold (₹1,250 locked) and conditional settlement transition.
      4. Live Mic & File Ingestion: Supports both live browser microphone input and drag-and-drop of synthetic audio samples.
      5. Chaos Injection Control Board: One-click interactive buttons:
         - [Inject: Normal Spin] -> Shows 60 FPS clean spectrum -> PASS -> Green Escrow Release.
         - [Inject: Bearing Spall] -> Shows 1,450 Hz harmonic spike -> Escrow Locked -> Dispatches Delhivery.
         - [Inject: Replay Attack] -> Flags missing low-rumble -> Red Fraud Alert.
         - [Inject: High Kitchen Noise] -> Flags SNR 8.2 dB -> Prompts quiet recording.
         - [Inject: No Delhivery Rider] -> Simulates 503 -> Re-routes to peripheral hub.
   C. Screen Recording Workflow Preparation:
      - Ensure the dashboard contains a seamless 90-second "Demo Mode" button that executes the full happy path with animated audio playback and state transitions, ready for the hackathon video recording.
3. Verification:
   - Serve locally (`python -m http.server 3000 --directory public`) and test in Playwright browser.
   - Verify 60 FPS rendering with zero jank, zero console errors, and full mobile responsiveness.
```

---

## 4. ⚖️ SESSION D: Unification, Pass^k Verification & Master Submission Overseer

### Purpose & Scope
The Master Orchestrator and Council Chairman session. Runs after Sessions A, B, and C complete their deliverables. Consolidates all three streams, verifies end-to-end physical integration, executes the 50-trial Pass^k reliability benchmark, generates `PROOF_REPORT.md`, records the screen flow, and packages the final submission.

### Copy-Paste Prompt for Session D (The Unification Overseer)
```text
You are the Chief Solutions Architect & Council Chairman for AcuDiag (Session D: Unification & Submission Overseer).
Your mission is to audit, unify, and empirically verify all deliverables produced by Sessions A, B, and C, ensuring zero shortcomings, zero synthetic mocks, and total compliance with The Ken Round 3 Build Track requirements.

PRIMARY DIRECTIVES:
1. Multi-Stream Audit & Integration Check:
   - Verify Session A: Inspect `benchmarks/DSP_BENCHMARK_REPORT.md` and `baseline_vectors/golden_baselines.json`. Verify p95 DSP latency < 5ms.
   - Verify Session B: Inspect `src/blackboard_hub.py`, `databank/03_Mock_Server/mock_server.py`, and `src/pinelabs_agentic_bridge.py`. Verify all 10 eval scenarios execute cleanly.
   - Verify Session C: Inspect `public/index.html`. Launch local server, navigate in Playwright, and verify 60 FPS spectrogram, glowing 9-state machine, and chaos injection panel.
2. Pass^k Reliability Benchmark (k=50):
   - Build and execute `benchmarks/run_pass_k_benchmark.py`:
     - Run 50 consecutive noisy end-to-end trials across the full 3-rail state machine (Intake -> DSP Diagnosis -> Pine Labs Pre-auth -> Delhivery Dispatch -> Repair -> Anti-spoofing Post-Test -> Escrow Settlement).
     - Calculate Pass^50 reliability metric. Guarantee Pass^50 >= 0.98.
   - Generate `benchmarks/PROOF_REPORT.md` with empirical latency percentiles (p50, p90, p95, p99), SNR distribution curves, and cryptographic HMAC token logs.
3. Final Submission Deliverables Check:
   - Open `databank/05_Final_Submission_Dossier/The_Ken_Round_3_Master_Submission_Dossier.md` and verify all questions are addressed with zero omissions:
     [x] 100-word user story (Priya's washing machine, 92 words).
     [x] 10-step chronological decision log (date, input, connector, rule, action).
     [x] Connector inventory (real vs mock classification).
     [x] 3 future capabilities (GeoNaksha, Acoustic Escrow Trigger, Telephony VAD Bypass).
     [x] 3 rail readiness scores (Pine Labs: 8.5, Gnani: 8.0, Delhivery: 7.5).
     [x] 10 adversarial eval cases with system prompt evolution (v1 -> v3) and run logs.
     [x] Failure analysis (cascading multi-faults, empty tiled reverberation).
4. Pine Labs Platform Screen Recording Guide:
   - Provide step-by-step instructions for recording the agent running on `https://agenticorg.hackathon.pinelabs.com`, including the two required perturbed human runs (user saying no / replying late).
5. Final Delivery Gate Checklist 1-6 Sign-off:
   - Confirm Gate 1 (AST/Syntax: 0 errors), Gate 2 (Unit tests: 23+ passing), Gate 3 (Daemons/Sockets live), Gate 4 (Atelier UI polish), Gate 5 (Physical reality tagged), Gate 6 (executive_brief.md up to date).
   - Sync all final artifacts to Google Drive (`G:\My Drive\Ken_Evidences\`).
```
