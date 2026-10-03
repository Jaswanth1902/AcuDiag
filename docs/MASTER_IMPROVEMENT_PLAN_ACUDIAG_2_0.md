# 🗺️ Master Strategic Improvement & Innovation Roadmap: AcuDiag 2.0

> **System**: AcuDiag Autonomous Appliance Diagnostics & 3-Rail Orchestration  
> **Milestone**: Post-Round 3 Production Hardening & Future Capabilities Implementation  
> **Status**: APPROVED FOR EXECUTION  

---

## Phase 1: Acoustic Physics & Compound Fault Intelligence (DSP Layer)

### 1.1 Multi-Resolution Mel-Spectrogram & Envelope Kurtosis
- **Objective**: Eradicate the single-frequency limitation identified in edge cases (simultaneous bearing spall + drain cavitation).
- **Tasks**:
  1. Implement a 64-band Log-Mel temporal filterbank ($N_{\text{fft}}=1024, \text{hop}=512$) inspired by Hitachi MIMII baseline.
  2. Add high-frequency envelope kurtosis ($\text{Kurtosis} > 4.5$ indicates intermittent mechanical micro-impacts).
  3. Calibrate compound harmonic separation in `src/acoustic_analyzer.py` under 5ms CPU budget.
- **Verification Metric**: $100\%$ detection accuracy on dual-fault synthetic fixtures in `tests/test_audio_dsp.py`.

### 1.2 Bathroom Multi-Path Echo Cancellation (Dereverberation Filter)
- **Objective**: Mitigate room reflections in untreated concrete/tiled bathrooms ($RT_{60} > 1.2\text{s}$).
- **Tasks**:
  1. Add Minimum Mean Square Error (MMSE) spectral subtraction for ambient diffuse reverberation.
  2. Implement contact vibration prompt gating when spectral flatness variance exceeds $0.15$.

---

## Phase 2: 3-Rail Capabilities & Autonomous Network Expansion

### 2.1 Capability 1: Delhivery GeoNaksha 3D Hyper-Local Drop Coordination
- **Objective**: Auto-resolve complex Indian apartment addresses ("Tower B, Flat 402, Behind Clubhouse") into 3D spatial drop points.
- **Tasks**:
  1. Expand `databank/03_Mock_Server/mock_server.py` to expose `/api/v1/delhivery/geonaksha/validate`.
  2. Generate high-precision spatial drop coordinates and automated gate-entry delivery OTPs.
  3. Mirror delivery tracking and live GPS ETA into the WhatsApp conversation state.

### 2.2 Capability 2: Pine Labs Cryptographic Acoustic Escrow Release Trigger
- **Objective**: Direct cryptographic binding of escrow capture to Neyman-Pearson LRT telemetry.
- **Tasks**:
  1. Implement HMAC-SHA256 diagnostic proof envelopes signed with private session secrets (`ACU_PASS_SHA256_<hash>`).
  2. Update `src/pinelabs_agentic_bridge.py` and `mock_server.py` to enforce cryptographic signature validation on `PUT /capture`.
  3. Ensure dispute cooling period auto-refunds customer if verification is rejected.

### 2.3 Capability 3: Gnani Telephony VAD Bypass Acoustic Stream
- **Objective**: Enable non-verbal appliance acoustic diagnostic scans over phone calls without human voice filtering.
- **Tasks**:
  1. Implement raw 20Hz–8000Hz unfiltered SIP/RTP stream intake in `src/gnani_voice_client.py`.
  2. Add automatic acoustic/speech classifier: routes speech to Prisma v2.5 STT, routes motor noise directly to DSP core.

---

## Phase 3: WhatsApp Conversational Experience & Interactive Generative UI

### 3.1 WhatsApp Interactive Action Buttons & Rich Media Templates
- **Objective**: Move beyond text prompts to interactive native buttons ("Approve & Lock Escrow", "Decline Quote", "Start Spin Test").
- **Tasks**:
  1. Add WhatsApp Interactive Message Template payload generator in `src/whatsapp_agentic_bridge.py`.
  2. Support inline spectrogram PNG snapshot generation and delivery to the customer.

### 3.2 Real-Time Cockpit WebSocket Event Streaming
- **Objective**: Synchronize live customer and technician actions with the Operations Desk HUD in real time.
- **Tasks**:
  1. Add WebSocket endpoint `/ws/cockpit/events` to `mock_server.py`.
  2. Broadcast state changes (Onboarding $\rightarrow$ Escrow Locked $\rightarrow$ Dispatched $\rightarrow$ Settled) directly to `public/index.html`.

---

## Phase 4: Zero-Trust Teleoperation & Production Edge Deployment

### 4.1 AgentReach Execution Gating for Staging & Cloud Hubs
- **Objective**: Safe, zero-trust remote execution across Windows/WSL2/Docker.
- **Tasks**:
  1. Bind `reach.exe` CLI wrapper into deployment scripts (`scripts/deploy_staging.py`).
  2. Maintain strict local credential containment—no remote API key exposure.
  3. Implement automated pre-flight socket probes (<0.5s) and health verification.

### 4.2 Comprehensive Pass^k Continuous Verification
- **Objective**: 100% automated regression defense.
- **Tasks**:
  1. Maintain 100% pass rate across the full 64-test suite.
  2. Run 50-trial Pass^50 reliability benchmarks on every git commit.
  3. Keep `PROOF_REPORT.md` continuously updated with live latency and accuracy telemetry.
