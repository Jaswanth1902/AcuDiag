# AcuDiag Project Rules & Execution Standards

## 1. Project Overview & Context
- **Workspace**: `C:\Users\jaswa\Antigravity\01_Projects\AcuDiag`
- **Competition**: The Ken Case-Build 2026 (Round 3 Build Stage)
- **Partner Rails**:
  - **Gnani.ai**: Indic Voice Infrastructure (Prisma v2.5 STT, Timbre v2.5 TTS, Hinglish code-switching)
  - **Pine Labs**: Plural Escrow Lifecycle (Two-stage Pre-auth, Milestone Capture, Reversal, Idempotency)
  - **Delhivery**: CMU Forward & Reverse Logistics (Automated Return Manifestation, Waybill Tracking)
- **Platform**: Pine Labs AgenticOrg (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`, User: `ksaijaswanthr.cs24@rvce.edu.in`)

## 2. Invariants & Guardrails
1. **Pure Python Stdlib Priority**: Minimize external dependency weight; keep core math (DSP, LRT, FFT/DCT) lean and zero-bloat.
2. **Subprocess Visibility (CREATE_NO_WINDOW)**: On Windows, every subprocess invocation must pass `creationflags=0x08000000` (Layer 0 Law 8).
3. **Zero-Mock Physical Reality**: While mock servers simulate partner edge cases/chaos, all internal math, audio processing, and integration pipelines execute against real data buffers and real network sockets.
4. **Secret Hygiene**: Read credentials from `credentials/credentials.env` exclusively; never commit, hardcode, or echo secrets in logs or git.
5. **Fast AST & Testing**: Validate changes through `python 01_Projects/AcuDiag/run_full_verification.py` (<10s for 23 automated tests).
