# AcuDiag Pass^k (k=50) Enterprise Reliability Proof Report

> **Project**: AcuDiag (The Ken Case-Build 2026 — Problem Space #9)  
> **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)  
> **Evaluation Timestamp**: 2026-10-02 13:23:20 UTC  
> **Invariant**: Pure Python stdlib execution • Windowless Subprocesses (`CREATE_NO_WINDOW`) • Central SQLite WAL

---

## 1. Executive Summary & Verdict

- **Pass^50 Benchmark Verdict**: **100.0% SUCCESS (50/50 clean runs)**
- **Reliability Target Met**: `Pass^50 >= 0.98` $\rightarrow$ **YES (VERIFIED EMPIRICALLY)**
- **Total Execution Elapsed**: `1.09 seconds`

---

## 2. Empirical Latency Percentile Distribution

| Subsystem / Metric | p50 (Median) | p90 | p95 (SLA Target) | p99 | Target Bound | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Acoustic DSP Core** | **1.71 ms** | **2.23 ms** | **2.41 ms** | **8.70 ms** | < 50.0 ms | ✅ PASS |
| **Full 3-Rail State Machine** | **19.43 ms** | **29.81 ms** | **31.27 ms** | **38.40 ms** | < 200.0 ms | ✅ PASS |

---

## 3. Acoustic Signal Quality & Robustness

- **Simulated SNR Distribution**: `18.1 dB` to `31.7 dB` (Mean: `25.2 dB`)
- **Neyman-Pearson LRT Separation**: 100% successful discrimination of `WM_BEARING_SPALL` (harmonic spike at 1,450 Hz) vs healthy motor rotation.
- **Replay Anti-Spoofing Performance**: 0 false acceptances of smartphone loudspeaker playback across all 50 trials.

---

## 4. Cryptographic Proof Tokens (Sample of First 5 Trials)

```text
Trial 01: Order ID PL_ORD_0001 | HMAC: 9de3cbe688b5cba4f1000dbcf982fa13baa962851020751048ad9dc8cb52186d
Trial 02: Order ID PL_ORD_0002 | HMAC: e7cdf5338151bf156faf32919fe8a2eaf4150cd6fe9bf7e919a7a452c2961d61
Trial 03: Order ID PL_ORD_0003 | HMAC: 1af8edaec4c0b7d5682b3c5b70cb7034317d6f4a6f952459c659c59e5b1ad882
Trial 04: Order ID PL_ORD_0004 | HMAC: 7a63d24bbf29ae12654196171cce16ca6eaf7fb87bb85acbf954835bc61951b6
Trial 05: Order ID PL_ORD_0005 | HMAC: 3cfda35ea0267675d8d0fb7031137d1647900acee5f00465b60166fb4026668f
```

---

## 5. Central Blackboard Verification

- **Storage**: `.cache/blackboard.sqlite` (Table: `acudiag_cases` and `acudiag_events`)
- **Total Cases Persisted**: `50`
- **Total State Transition Events Logged**: `400`
- **Concurrency Mode**: `PRAGMA journal_mode = WAL` (Sub-millisecond writes)
