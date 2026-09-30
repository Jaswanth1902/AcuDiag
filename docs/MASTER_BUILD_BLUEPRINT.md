# 🏆 AcuDiag Enterprise Master Build Blueprint (Round 3 Build Sprint)

> **Event**: The Ken Case-Build Competition 2026: "The Great Rewiring"  
> **Problem Space #9**: Keeping the Machines Running (Home Appliances & Devices)  
> **Sprint Window**: September 30 – October 4, 2026 (~4 Days)  
> **Platform**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`) • **Org**: Ken's Case Competition  
> **Three-Pillar Triad**: Gnani.ai (Voice) • Pine Labs Plural (Escrow Payments) • Delhivery (Logistics)  
> **Engineering Standard**: Enterprise Production-Grade, Dual-Channel Bridge, Zero-Mock Core, Physical Telemetry, Pass^k ($k=50$)

---

## 1. 🎯 The Winning Thesis & System Architecture

AcuDiag resolves the fundamental trust deficit in consumer home appliance maintenance: **the technician unilaterally declaring a repair complete when the machine is still failing, and the homeowner feeling intimidated to pay**.

```
[ Appliance Acoustic Sound ]
            │
            ▼
[ Dual-Mode Intake ] ───────────────────────────────────────────────┐
  Mode A: Gnani Conversational IVR (AMR-NB) for symptom triage      │
  Mode B: Raw PWA WebAudio (44.1kHz, noiseSuppression: false)       │
            │                                                       │
            ▼                                                       ▼
[ Sub-5ms DSP Engine (SciPy SOS + Gammatone 64-dim ERB) ]    [ Gnani STT / TTS ]
            │                                                 • Prisma v2.5 (10 Indian langs)
            ▼                                                 • Timbre v2.5 (Nalini/Kaveri)
[ Neyman-Pearson LRT Classifier + Replay Anti-Spoofing ]      • Domain Vocab Biasing
            │                                                       │
            ▼                                                       │
[ Central Data Fabric: blackboard_hub.py (SQLite WAL Event Bus) ] ◄─┘
            │
     ┌──────┴───────────────────────────┐
     ▼                                  ▼
[ Pine Labs Plural Escrow ]     [ Delhivery Logistics (OS1) ]
  • Connector: pinelabs_plural    • Forward OEM Part: /api/cmu/create.json
  • POST /api/pay/v1/orders       • Reverse Pickup: /fm/request/new/
  • pre_auth: true                • Pincode TAT: /c/api/pin-codes/json/
  • PUT /capture on LRT PASS      • Tracking: /api/v1/packages/json/
  • AUTO-REFUND on DOA fail       • 3 Capabilities: GeoNaksha, VAD, Trigger
```

---

## 2. ⚡ The Three Pillars Synchronized Specification

### Pillar 1: Gnani Voice Engine (`src/gnani_voice_client.py`)
- **Speech-to-Text (STT)**:
  - Gateway: `POST https://api.vachana.ai/stt/v3` (Prisma v2.5).
  - Languages: Hindi (`hi-IN`), Kannada (`kn-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Hinglish (`hi-en`).
  - Vocabulary Biasing: `bias_list: ["AcuDiag", "washing machine", "drum bearing", "escrow", "Pine Labs", "Delhivery"]`, `bias_score: 3`.
- **Text-to-Speech (TTS)**:
  - Gateway: `POST https://api.vachana.ai/api/v1/tts/inference` (Timbre v2.5).
  - Voices: `Nalini` (Warm, authoritative Hindi), `Kaveri` (Clear Southern Lead), `Deepak` (Inspector).
  - Audio Profiles: 24kHz linear PCM WAV for Atelier Web Cockpit; 8kHz G.711 µ-law for telephony IVR.

### Pillar 2: Pine Labs Plural Escrow (`src/pinelabs_agentic_bridge.py`)
- **AgenticOrg Connector**: `pinelabs_plural` pre-configured and active (`api_key`, rate: 60/min).
- **Escrow Pre-Authorization**: `POST /api/pay/v1/orders` (`pre_auth: true`) locks parts + labor funds before technician dispatches.
- **Cryptographic Release**: Triggered ONLY when Neyman-Pearson Likelihood Ratio Test satisfies $LRT \le \gamma$ and Replay Anti-Spoofing passes ($p_{replay} < 0.05$).
- **Disputed Refund**: Automatic partial or full refund if post-repair test fails consecutive trials.

### Pillar 3: Delhivery Logistics & Supply Chain (`databank/03_Mock_Server/mock_server.py`)
- **Pincode TAT Lookup**: `GET /c/api/pin-codes/json/?filter_codes={pincode}` validates regional serviceability.
- **Forward OEM Spare Part Dispatch**: `POST /api/cmu/create.json` manifests genuine OEM replacement components directly from regional fulfillment hubs to customer doorsteps.
- **Reverse Pickup (Core Deposit Return)**: `POST /fm/request/new/` collects damaged parts for OEM failure analysis and core deposit release.
- **Real-Time Tracking**: `GET /api/v1/packages/json/?waybill={waybill}` updates customer via Gnani voice and WhatsApp.
- **3 Future Capabilities**:
  1. *Delhivery GeoNaksha 3D Drop*: Sub-meter coordinate localization for gated community drops.
  2. *Pine Labs Acoustic Escrow Hardware Trigger*: Sub-millisecond direct crypto-settlement.
  3. *Gnani Telephony VAD Bypass*: Full-spectrum 20Hz-8kHz uncompressed vibration streaming.
- **Chaos Injection**: Real-world resilience against `no_rider` (503), `low_balance` (402), `timeout` (504), and `malformed` (corrupt buffer) responses.

---

## 3. 🔬 Stream A: Acoustic Physics & Sub-5ms DSP Core

1. **Bandpass Filtering**: 4th-order Butterworth filter implemented strictly as **Second-Order Sections (SOS)** ($20\,\text{Hz} - 8,000\,\text{Hz}$).
2. **Feature Extraction**: 64-dimension Gammatone Equivalent Rectangular Bandwidth (ERB) filterbank capturing mechanical resonance.
3. **Statistical Hypothesis Testing (Neyman-Pearson LRT)**:
   $$\Lambda(x) = \frac{p(x \mid H_1)}{p(x \mid H_0)} \gtrless \gamma$$
   False Alarm Rate $\alpha \le 0.01$. If $\Lambda(x) > \gamma$, repair test FAILS $\rightarrow$ Escrow remains LOCKED.
4. **Replay Anti-Spoofing Engine**:
   - Detects fake phone-speaker playback via High-Frequency Spectral Flatness and Phase Variance.
5. **Synthetic Appliance Acoustic Generator**:
   - Generates realistic waveforms across 4 fault classes: `WM_BEARING_SPALL`, `WM_DRUM_IMBALANCE`, `PUMP_CAVITATION`, `COMPRESSOR_VALVE_LEAK`.

---

## 4. 🎨 Stream C: Atelier Cockpit HUD (`public/index.html`)

- **Aesthetic**: Atelier Dark Obsidian (`#090D16`), Emil Kowalski tactile physics (:active scale 0.97).
- **60 FPS Canvas Spectrogram**: Live real-time audio FFT analyzer (20 Hz - 8 kHz).
- **9-State Machine Nodes**: Live visual state transitions from `ONBOARDING` to `ESCROW_RELEASED`.
- **Chaos Simulation Board**: Interactive toggles for `no_rider`, `low_balance`, `timeout`, and `malformed`.

---

## 5. 📅 4-Day Execution Roadmap & Verification

- **Day 1 (Sep 30 – Oct 1)**: Platform audit complete, dual-channel bridge verified, DSP core & 3-rail mock server operational.
- **Day 2 (Oct 1 – Oct 2)**: Register `delhivery_acudiag` and `gnani_acudiag` on AgenticOrg; instantiate `AcuDiag Orchestrator` virtual employee; attend Pine Labs Demo (5 PM).
- **Day 3 (Oct 2 – Oct 3)**: Build Atelier Cockpit HUD, connect 60 FPS spectrogram, and run 10 adversarial evaluation cases.
- **Day 4 (Oct 3 – Oct 4)**: Pass^k ($k=50$) benchmark validation, capture high-definition screen recording on Pine Labs platform, compile submission package.
