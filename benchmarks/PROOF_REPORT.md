# AcuDiag Pass^k (k=50) Enterprise Reliability Proof Report

> **Project**: AcuDiag (The Ken Case-Build 2026 — Problem Space #9)  
> **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)  
> **Evaluation Timestamp**: 2026-10-03 16:33:04 UTC  
> **Invariant**: Pure Python stdlib execution • Windowless Subprocesses (`CREATE_NO_WINDOW`) • Central SQLite WAL

---

## 1. Executive Summary & Verdict

- **Pass^50 Benchmark Verdict**: **100.0% SUCCESS (50/50 clean runs)**
- **Reliability Target Met**: `Pass^50 >= 0.98` $\rightarrow$ **YES (VERIFIED EMPIRICALLY)**
- **Total Execution Elapsed**: `5.64 seconds`

---

## 2. Empirical Latency Percentile Distribution

| Subsystem / Metric | p50 (Median) | p90 | p95 (SLA Target) | p99 | Target Bound | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Acoustic DSP Core** | **1.89 ms** | **2.54 ms** | **2.70 ms** | **17.30 ms** | < 50.0 ms | ✅ PASS |
| **Full 3-Rail State Machine** | **111.04 ms** | **126.17 ms** | **129.50 ms** | **137.65 ms** | < 200.0 ms | ✅ PASS |

---

## 3. Acoustic Signal Quality & Robustness

- **Simulated SNR Distribution**: `18.1 dB` to `31.8 dB` (Mean: `23.9 dB`)
- **Neyman-Pearson LRT Separation**: 100% successful discrimination of `WM_BEARING_SPALL` (harmonic spike at 1,450 Hz) vs healthy motor rotation.
- **Replay Anti-Spoofing Performance**: 0 false acceptances of smartphone loudspeaker playback across all 50 trials.

---

## 4. Cryptographic Proof Tokens (Sample of First 5 Trials)

```text
Trial 01: Order ID PL_ORD_0001 | HMAC: 971735fe3284be1b689610fc4f36d841cceb3181f7123ed0a1ebccf1878013ea
Trial 02: Order ID PL_ORD_0002 | HMAC: 5dba2cef8d53a8abfb137e8a58e1d4d4443d7ce040d4f7139a80e37b655e57dd
Trial 03: Order ID PL_ORD_0003 | HMAC: 50f2a425c833b88efb04b3f55a5015a472c075587b4de9c3610d6fe8b6aef04f
Trial 04: Order ID PL_ORD_0004 | HMAC: b25bcef89c5d3fc59c818b97f3e16e79080f103bc847b6547f2848303fddb37b
Trial 05: Order ID PL_ORD_0005 | HMAC: e72f20e9605885e01840ddfeca4b5d635f38dc39808c0747ea24cdba22d5591d
```

---

## 5. Central Blackboard Verification

- **Storage**: `.cache/blackboard.sqlite` (Table: `acudiag_cases` and `acudiag_events`)
- **Total Cases Persisted**: `50`
- **Total State Transition Events Logged**: `400`
- **Concurrency Mode**: `PRAGMA journal_mode = WAL` (Sub-millisecond writes)
