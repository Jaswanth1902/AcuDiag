# 🔬 AcuDiag Next-Gen Architectural Research & Improvement Plan

> **Author**: Antigravity Principal Systems Architect & Research Engine  
> **Source Vectors**: arXiv Peer-Reviewed Papers, MIMII/HAASD Appliance Benchmarks, GitHub Open-Source Ecosystem, Token-Bounded Scrapling  
> **Date**: 2026-10-03  
> **Status**: APPROVED FOR ROADMAP EXECUTION  

---

## 1. 🌐 Executive Synthesis & Literature Grounding

Through multi-vector research across academic literature (arXiv), industrial sound datasets (**MIMII** pumps/valves/fans and **HAASD** household appliance abnormal sound detection), and open-source tooling, we have identified critical state-of-the-art architectures to take AcuDiag from a single-appliance prototype to an enterprise-grade, edge-deployable acoustic diagnostic network.

### Academic Citations & Validated Methodologies
1. **HAASD (Household Appliances Abnormal Sound Detection)**:
   - Ground truth benchmark proving that real household environments suffer from severe negative-sample scarcity and low SNRs (down to -6 dB).
   - Confirms that single-frequency thresholding breaks down in heterogeneous room acoustics; validates the need for multi-band Gammatone ERB filterbanks coupled with statistical anomaly detection.
2. **MIMII Benchmark (Zenodo / Hitachi Research)**:
   - Evaluates pumps, valves, and fans across diverse factory and domestic noise conditions (16 kHz, 16-bit PCM).
   - Demonstrates that valve cavitation leaks and pump clogging manifest in high-frequency spectral bands (>2.2 kHz) modulated by low-frequency rotor fundamentals.
3. **Domain Adaptation & Transfer Learning (arXiv:1905.06004 & arXiv:2504.11513)**:
   - Multi-output classification (MOC) and frequency-layer normalization enable transferring acoustic diagnostic baselines across varying appliance brands (e.g., Godrej to LG or Samsung) without retraining from scratch.
4. **Voice & Acoustic Anti-Spoofing (arXiv:2310.05813 & arXiv:1909.00935)**:
   - Multi-order audio replay detection demonstrates that speaker playback introduces compression-assisted spectral phase distortion and elevated Wiener entropy in the 6 kHz – 20 kHz DAC region.

---

## 2. 🗺️ Enterprise Gap Analysis: Current vs. Target State

| Dimension | Current AcuDiag Implementation | Target Enterprise Architecture (Next-Gen) |
| :--- | :--- | :--- |
| **Acoustic Modeling** | 64-band Gammatone ERB + Neyman-Pearson LRT distance | Hybrid Dual-Tier Engine: Real-time Gammatone LRT (<2ms) + ONNX MobileNetV4 / AST Spectrogram Encoder (<15ms) |
| **Appliance Diversity** | Dynamic catalog across 5 major appliance classes | Complete Indian OEM coverage across 16 appliance topologies with automated HSN tariff synchronization |
| **Hardware & Remote Teleoperation** | Local Windows FastAPI process (`localhost:8000`) | Multi-Node AgentReach (`reach.exe`) execution across edge gateway hubs, remote technician mobile apps, and Docker microservices |
| **Anti-Spoofing & Security** | Sub-120Hz contact rumble + DAC high-frequency check | Dual-Sensor Telemetry: Accelerometer IMU vibration cross-correlation + microphone acoustic phase coherence |
| **Logistics & Escrow Rails** | 3-Rail Mock Server (Pine Labs, Delhivery, Gnani) | Production Webhook Integration with Pine Labs Plural P3P signature verification and live Delhivery B2B API |
| **Red Teaming & Resilience** | 13-vector adversarial test harness | Continuous automated fuzzing engine with synthetic noise injection (-6 dB to 30 dB) and Langfuse prompt auditing |

---

## 3. 🚀 Concrete Multi-Phase Roadmap for Next-Gen Upgrades

### Phase 1: Edge-Native Hybrid Inference & Micro-Embedding Compression
- **Milestone 1.1**: Package lightweight ONNX models trained on CWRU and HAASD datasets alongside the deterministic numpy Butterworth-Gammatone pipeline.
- **Milestone 1.2**: Implement micro-embedding caching in `.cache/blackboard.sqlite` using `sqlite-vec` or cosine hashes for zero-latency retrieval of historical appliance signatures.
- **Milestone 1.3**: Deploy client-side WebAssembly (Wasm) DSP analyzer inside `public/index.html` allowing offline in-browser audio filtering before uploading to the server.

### Phase 2: AgentReach (`reach`) Remote Teleoperation & Edge Micro-Hubs
- **Milestone 2.1**: Compile and register `reach.exe` in `05_Services/bin/` to enable zero-trust remote command execution across technician devices and test benches.
- **Milestone 2.2**: Establish secure tunnel relays (`reach up staging-box`) allowing Antigravity agents on the local workstation to remotely audit edge micro-servers in Delhivery fulfillment hubs without installing dependencies remotely.

### Phase 3: Compound Multi-Fault Kinematics & Cascading Repair Trees
- **Milestone 3.1**: Support multi-fault decomposition (e.g., simultaneous bearing spall + worn drive belt) using blind source separation (FastICA / NMF).
- **Milestone 3.2**: Implement multi-step repair workflows where post-repair acoustic verification can isolate secondary deeper faults and automatically issue supplemental warranty co-pays.

### Phase 4: Production Partner Rail Hardening & Multi-Tenant Scalability
- **Milestone 4.1**: Upgrade Pine Labs Plural integration with asymmetric RSA/HMAC webhook signature validation and distributed idempotency locking in Redis/WAL.
- **Milestone 4.2**: Implement Delhivery CMU auto-routing with pincode failover to regional 3PL partners (Bluedart / Shadowfax) during localized carrier stockouts.
- **Milestone 4.3**: Integrate real-time Prometheus / Opik telemetry collectors monitoring DSP latency percentiles ($p_{50} \le 2\text{ms}, p_{99} \le 10\text{ms}$).
