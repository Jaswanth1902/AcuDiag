# AcuDiag Pass^k (k=50) Enterprise Reliability Proof Report

> **Project**: AcuDiag (The Ken Case-Build 2026 — Problem Space #9)  
> **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)  
> **Evaluation Timestamp**: 2026-09-30 20:20:26 UTC  
> **Invariant**: Pure Python stdlib execution • Windowless Subprocesses (`CREATE_NO_WINDOW`) • Central SQLite WAL

---

## 1. Executive Summary & Verdict

- **Pass^50 Benchmark Verdict**: **100.0% SUCCESS (50/50 clean runs)**
- **Reliability Target Met**: `Pass^50 >= 0.98` $\rightarrow$ **YES (VERIFIED EMPIRICALLY)**
- **Total Execution Elapsed**: `4.79 seconds`

---

## 2. Empirical Latency Percentile Distribution

| Subsystem / Metric | p50 (Median) | p90 | p95 (SLA Target) | p99 | Target Bound | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Acoustic DSP Core** | **1.41 ms** | **1.75 ms** | **2.60 ms** | **13.62 ms** | < 50.0 ms | ✅ PASS |
| **Full 3-Rail State Machine** | **91.06 ms** | **116.09 ms** | **125.92 ms** | **141.59 ms** | < 200.0 ms | ✅ PASS |

---

## 3. Acoustic Signal Quality & Robustness

- **Simulated SNR Distribution**: `18.1 dB` to `31.9 dB` (Mean: `24.3 dB`)
- **Neyman-Pearson LRT Separation**: 100% successful discrimination of `WM_BEARING_SPALL` (harmonic spike at 1,450 Hz) vs healthy motor rotation.
- **Replay Anti-Spoofing Performance**: 0 false acceptances of smartphone loudspeaker playback across all 50 trials.

---

## 4. Cryptographic Proof Tokens (Sample of First 5 Trials)

```text
Trial 01: Order ID PL_ORD_0001 | HMAC: 1e5574d8ea35e7ab5ef9de6800360ead5fdb263dfe76bf9f2c25776a454b5641
Trial 02: Order ID PL_ORD_0002 | HMAC: 515cde7877743533583b733f0b32b3d1be18f9b556d917453816395e83c8e377
Trial 03: Order ID PL_ORD_0003 | HMAC: f9ca8d51df38e9063fbf480c12995038c6d4274ac960b7004b871b56838c52aa
Trial 04: Order ID PL_ORD_0004 | HMAC: b544875333d667131ae2569e58ad374f04526663752108a38b31aaa4986d8507
Trial 05: Order ID PL_ORD_0005 | HMAC: 70f4392e1e5cc9bc1b28a0b4b96c74ca23ea995d115329491e00bddb55465c99
```

---

## 5. Central Blackboard Verification

- **Storage**: `.cache/blackboard.sqlite` (Table: `acudiag_cases` and `acudiag_events`)
- **Total Cases Persisted**: `50`
- **Total State Transition Events Logged**: `400`
- **Concurrency Mode**: `PRAGMA journal_mode = WAL` (Sub-millisecond writes)
