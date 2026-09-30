# AcuDiag Dependencies & Environment Signatures

## Core Python Packages
- `numpy`: Fast vectorized DSP, STFT, Gammatone filterbanks, Neyman-Pearson LRT detection.
- `fastapi` & `uvicorn`: High-throughput mock connector server & REST gateways.
- `httpx` / `requests`: Asynchronous and synchronous client transports for partner rails.
- `pytest`: Automated 23-test adversarial evaluation and mock server test suite.

## Runtime Ports & Endpoints
- **Mock Partner Server**: `http://127.0.0.1:8000`
  - Delhivery CMU: `/api/cmu/pincode/{pincode}`, `/api/cmu/manifest`, `/api/cmu/reverse-pickup`
  - Pine Labs Escrow: `/api/v1/escrow/preauth`, `/api/v1/escrow/capture`, `/api/v1/escrow/release`
  - Gnani Indic Voice: `/api/v1/stt/transcribe`, `/api/v1/tts/inference`
  - Health & Chaos: `/health` (Chaos modes: `no_rider`, `low_balance`, `timeout`, `malformed`)

## Pitfalls & Operational Boundaries
- Always enforce `creationflags=0x08000000` on Windows subprocesses.
- All credentials sourced dynamically from `credentials/credentials.env`.
- Ensure mock server includes CSP, X-Frame-Options, and HSTS headers.
