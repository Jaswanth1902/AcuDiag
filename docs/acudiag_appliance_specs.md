# 🔬 AcuDiag Appliance Acoustic Failure Signatures & Knowledge Base

> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Tenant ID**: `abb61bca-a3f5-4aba-b30e-946016b13120`  
> **Target Appliance Categories**: Front-Load / Top-Load Washers, Refrigerators, Inverter ACs

---

## 1. Acoustic Signature Classification Profiles

### 1.1 Front-Load Washer: Drum Bearing Outer Race Spall (BPFO)
- **Primary Frequency**: 1,450 Hz harmonic peak with 4th-order Butterworth bandpass resonance.
- **Physical Dynamics**: Outer race micro-pitting causing shock pulses as ball bearings traverse defect under 800–1200 RPM centrifugal load.
- **Neyman-Pearson Decision Boundary**: $\Lambda(x) = \ln \frac{P(x | H_1)}{P(x | H_0)} > 2.45$ (Fault detected); $\Lambda(x) \le 2.45$ (Healthy/Cleared).
- **Anti-Spoofing Signature**: Low-frequency mechanical rumble present (<120 Hz, >30 dB SPL); phase variance $\Delta\phi > 0.65$ rad across spatial stereo bands. Speaker replay flagged if $<120$ Hz energy drops below 12 dB SPL.
- **Replacement SKU**: `BEAR-6205-2RS` (Godrej/LG OEM Dual Rubber Sealed).
- **Cost Matrix**: Part: ₹850.00 | Labor: ₹400.00 | Total Escrow Pre-Auth: ₹1,250.00.

### 1.2 Washing Machine: Drain Pump Cavitation & Impeller Lock
- **Primary Frequency**: 320 Hz cavitation flutter coupled with 50 Hz line hum harmonic.
- **Physical Dynamics**: Trapped foreign coin/pin impeding magnetic impeller rotation; fluid boiling at blade edge.
- **Neyman-Pearson Boundary**: $\Lambda(x) > 3.10$.
- **Replacement SKU**: `PUMP-DRAIN-02` (Universal 30W Magnetic Synchronous Drain Pump).
- **Cost Matrix**: Part: ₹600.00 | Labor: ₹350.00 | Total Escrow Pre-Auth: ₹950.00.

### 1.3 Drive Belt Slippage & Pulley Glaze
- **Primary Frequency**: 220 Hz continuous squeal with friction pitch glide during motor torque ramp.
- **Physical Dynamics**: Loss of belt elastomer tension; thermal expansion slippage under heavy wet-load spin.
- **Replacement SKU**: `BELT-V-POLY` (Optibelt Multi-Rib 5EPJ 1225).
- **Cost Matrix**: Part: ₹450.00 | Labor: ₹300.00 | Total Escrow Pre-Auth: ₹750.00.

### 1.4 Suspension Strut Damper Decay
- **Primary Frequency**: 14 Hz violent transient thumps with structural chassis resonance.
- **Physical Dynamics**: Hydraulic friction loss in drum friction dampers causing unconstrained precession.
- **Replacement SKU**: `STRUT-SUSP-FL` (Godrej/Whirlpool 100N Friction Damper Pair).
- **Cost Matrix**: Part: ₹900.00 | Labor: ₹500.00 | Total Escrow Pre-Auth: ₹1,400.00.

---

## 2. Operational Invariants for Multi-Rail Orchestrator

1. **Noise Gating Invariant**: SNR strictly $\ge 15.0$ dB required. If background whistle, TV, or traffic causes SNR $< 15.0$ dB, reject test with instructions to isolate acoustic environment.
2. **Escrow Hold Invariant**: Never dispatch Delhivery CMU forward shipment until Pine Labs Plural pre-auth order returns `PRE_AUTH_LOCKED`.
3. **Physical Clearance Invariant**: Post-repair escrow release strictly requires $\Lambda(x) \le 2.45$ and Anti-Spoofing `PASS`. Payout withheld on failure; dispute period enforced.
4. **Logistics Lifecycle**: Upon verified post-repair settlement, trigger Delhivery Reverse Pickup (`POST /fm/request/new/`) to recover defective core component for OEM recycling.
