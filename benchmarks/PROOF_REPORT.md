# AcuDiag Pass^k (k=50) Enterprise Reliability Proof Report

> **Project**: AcuDiag (The Ken Case-Build 2026 — Problem Space #9)  
> **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)  
> **Evaluation Timestamp**: 2026-10-03 16:21:48 UTC  
> **Invariant**: Pure Python stdlib execution • Windowless Subprocesses (`CREATE_NO_WINDOW`) • Central SQLite WAL

---

## 1. Executive Summary & Verdict

- **Pass^50 Benchmark Verdict**: **100.0% SUCCESS (50/50 clean runs)**
- **Reliability Target Met**: `Pass^50 >= 0.98` $\rightarrow$ **YES (VERIFIED EMPIRICALLY)**
- **Total Execution Elapsed**: `5.85 seconds`

---

## 2. Empirical Latency Percentile Distribution

| Subsystem / Metric | p50 (Median) | p90 | p95 (SLA Target) | p99 | Target Bound | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Acoustic DSP Core** | **1.75 ms** | **2.42 ms** | **2.80 ms** | **24.78 ms** | < 50.0 ms | ✅ PASS |
| **Full 3-Rail State Machine** | **113.58 ms** | **133.58 ms** | **150.58 ms** | **168.12 ms** | < 200.0 ms | ✅ PASS |

---

## 3. Acoustic Signal Quality & Robustness

- **Simulated SNR Distribution**: `18.0 dB` to `31.8 dB` (Mean: `24.3 dB`)
- **Neyman-Pearson LRT Separation**: 100% successful discrimination of `WM_BEARING_SPALL` (harmonic spike at 1,450 Hz) vs healthy motor rotation.
- **Replay Anti-Spoofing Performance**: 0 false acceptances of smartphone loudspeaker playback across all 50 trials.

---

## 4. Cryptographic Proof Tokens (Sample of First 5 Trials)

```text
Trial 01: Order ID PL_ORD_0001 | HMAC: c688a4778b6cc1a6a042c86051f978176cb1adf1c6a869c36b3a3f0a740c2235
Trial 02: Order ID PL_ORD_0002 | HMAC: a3c0d2a2ac16c4106237966cdf7ca7a2179a96a2e2570108ad30a81e924ebe65
Trial 03: Order ID PL_ORD_0003 | HMAC: 024d54016fb071a6601e44849b7e18563a408dd248b50953713d285ea3ef576e
Trial 04: Order ID PL_ORD_0004 | HMAC: ff52f5fdd8836e83561dbbf4fc458fef9a1a141fa7269840a722b987d1d72f41
Trial 05: Order ID PL_ORD_0005 | HMAC: f03d46bb4a619dc23e79d2a6b5201ed6c37924771a9651abd868429d34e81dc7
```

---

## 5. Central Blackboard Verification

- **Storage**: `.cache/blackboard.sqlite` (Table: `acudiag_cases` and `acudiag_events`)
- **Total Cases Persisted**: `50`
- **Total State Transition Events Logged**: `400`
- **Concurrency Mode**: `PRAGMA journal_mode = WAL` (Sub-millisecond writes)
