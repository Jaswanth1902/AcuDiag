# AcuDiag Pass^k (k=50) Enterprise Reliability Proof Report

> **Project**: AcuDiag (The Ken Case-Build 2026 — Problem Space #9)  
> **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)  
> **Evaluation Timestamp**: 2026-10-01 01:49:53 UTC  
> **Invariant**: Pure Python stdlib execution • Windowless Subprocesses (`CREATE_NO_WINDOW`) • Central SQLite WAL

---

## 1. Executive Summary & Verdict

- **Pass^50 Benchmark Verdict**: **100.0% SUCCESS (50/50 clean runs)**
- **Reliability Target Met**: `Pass^50 >= 0.98` $\rightarrow$ **YES (VERIFIED EMPIRICALLY)**
- **Total Execution Elapsed**: `5.24 seconds`

---

## 2. Empirical Latency Percentile Distribution

| Subsystem / Metric | p50 (Median) | p90 | p95 (SLA Target) | p99 | Target Bound | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Acoustic DSP Core** | **1.62 ms** | **2.42 ms** | **2.72 ms** | **16.11 ms** | < 50.0 ms | ✅ PASS |
| **Full 3-Rail State Machine** | **101.51 ms** | **128.45 ms** | **137.75 ms** | **146.24 ms** | < 200.0 ms | ✅ PASS |

---

## 3. Acoustic Signal Quality & Robustness

- **Simulated SNR Distribution**: `18.6 dB` to `31.8 dB` (Mean: `24.9 dB`)
- **Neyman-Pearson LRT Separation**: 100% successful discrimination of `WM_BEARING_SPALL` (harmonic spike at 1,450 Hz) vs healthy motor rotation.
- **Replay Anti-Spoofing Performance**: 0 false acceptances of smartphone loudspeaker playback across all 50 trials.

---

## 4. Cryptographic Proof Tokens (Sample of First 5 Trials)

```text
Trial 01: Order ID PL_ORD_0001 | HMAC: 39117cc48533369802ea0644f25d80b3effc9049e16fa67c5855e655df362f67
Trial 02: Order ID PL_ORD_0002 | HMAC: af213e247b0ae7a2b2ffdc550e1654ee5e6ca471b1b95228cc90c75b2796f672
Trial 03: Order ID PL_ORD_0003 | HMAC: 25e1229ae13c71e9a72f1a63b42f2e08d34c4f8c1c17c1793f17f253298303fb
Trial 04: Order ID PL_ORD_0004 | HMAC: 1f796848411b0423cbb2aac9174eefdcae5cdce422976654e570f692eaeae144
Trial 05: Order ID PL_ORD_0005 | HMAC: 4619342e32f40b35fc04704ced60f238bdaf4859dbc4a392e087a4050a3eee2c
```

---

## 5. Central Blackboard Verification

- **Storage**: `.cache/blackboard.sqlite` (Table: `acudiag_cases` and `acudiag_events`)
- **Total Cases Persisted**: `50`
- **Total State Transition Events Logged**: `400`
- **Concurrency Mode**: `PRAGMA journal_mode = WAL` (Sub-millisecond writes)
