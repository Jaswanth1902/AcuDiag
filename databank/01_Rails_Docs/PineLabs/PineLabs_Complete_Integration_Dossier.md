# 💳 Pine Labs Rail: Comprehensive Architecture & Escrow Integration Dossier

> **Platform**: Pine Labs Plural Payment Gateway & AgenticOrg Enterprise Platform (`pinelabs.com` / `pluralonline.com`)  
> **Target Project**: AcuDiag (Problem Space #9: Keeping the Machines Running — The Ken Case-Build 2026)  
> **Classification**: Partner Rail 2 Specification (Conditional Pre-Auth Escrow, Settlement, Dispute Arbitrage)  
> **Environment**: Pine Labs AgenticOrg (`v4.8.0`) • Plural Sandbox • AcuDiag Mock Connector

---

## 1. Executive Summary & Strategic Rationale

In home appliance maintenance, **payment settlement is the ultimate leverage point**. 
The status quo fails because consumers are forced into immediate cash or UPI settlement before the appliance is physically verified under working load. Once the technician walks out the door, the homeowner has zero recourse.

**AcuDiag deploys Pine Labs as an autonomous truth-conditioned escrow rail**:
1. **Pre-Service Pre-Auth Hold**: Before parts or technician are dispatched, AcuDiag calls Pine Labs Plural to lock estimated labor and parts costs into escrow (`pre_auth: true`). Funds are held safely in an RBI-compliant escrow account without debiting the customer upfront.
2. **Deterministic Acoustic Gating**: Escrow release is cryptographically decoupled from human intervention. Pine Labs capture (`PUT /api/pay/v1/orders/{order_id}/capture`) is unlocked **ONLY** upon receipt of an HMAC-SHA256 signed diagnostic PASS token from AcuDiag's Neyman-Pearson LRT audio engine ($\Lambda(x) \le 2.45$).
3. **Automated Customer Protection**: If the post-repair test fails or a technician attempts a fake repair, the escrow lock remains active. If unrectified after secondary audit, funds are automatically refunded (`POST /api/pay/v1/orders/{order_id}/refund`) with zero customer confrontation.

---

## 2. Regulatory & Legal Grounding (RBI PA Master Direction 2025/2026)

AcuDiag's conditional escrow model operates under strict compliance with the **Reserve Bank of India (RBI)** regulations:
- **Master Direction on Regulation of Payment Aggregators (September 2025)**:
  - Pine Labs operates as an RBI-authorized Payment Aggregator (PA).
  - All funds are routed through designated escrow accounts maintained with scheduled commercial banks, strictly segregated from operational company capital.
- **Digital Payments E-Mandate Framework (2026)**:
  - Pre-authorization holds are executed via standardized UPI AutoPay mandates and tokenized card pre-auth locks.
  - Funds remain held in the consumer's bank balance until service fulfillment criteria are met.
- **T+1 Settlement SLA**:
  - Once the diagnostic PASS token is validated, Pine Labs triggers immediate capture with automated T+1 settlement directly into the certified technician's verified bank account.

---

## 3. Core Production API Specifications & Schemas

### 3.1. Pre-Auth Order Creation (Locking Escrow Funds)
- **Endpoint**: `POST https://api.pluralonline.com/api/pay/v1/orders`
- **Mock Endpoint**: `POST http://localhost:8000/api/pay/v1/orders`
- **Method**: `POST`
- **Headers**:
  ```http
  Authorization: Bearer {{PINELABS_PLURAL_API_KEY}}
  Content-Type: application/json
  x-verify: {{HMAC_SHA256_CHECKSUM}}
  ```
- **Request Payload**:
  ```json
  {
    "merchant_id": "PL_MERCHANT_ACUDIAG_8819",
    "customer_id": "CUST_JASWANTH_560059",
    "amount_in_paisa": 125000,
    "currency": "INR",
    "pre_auth": true,
    "appliance_ticket_id": "ACUDIAG-TKT-9921",
    "order_data": {
      "part_cost_paisa": 85000,
      "labor_cost_paisa": 40000,
      "escrow_type": "CONDITIONAL_ACOUSTIC_RELEASE"
    }
  }
  ```
- **Response Schema**:
  ```json
  {
    "order_id": "PL_ORD_8A92B1C4",
    "status": "PRE_AUTH_LOCKED",
    "amount": 1250.00,
    "escrow_hold_state": "ACTIVE_HOLD",
    "currency": "INR",
    "message": "Funds successfully held in escrow. Requires acoustic Neyman-Pearson PASS for release."
  }
  ```

---

### 3.2. Conditional Escrow Capture (Releasing Payout)
- **Endpoint**: `PUT https://api.pluralonline.com/api/pay/v1/orders/{order_id}/capture`
- **Mock Endpoint**: `PUT http://localhost:8000/api/pay/v1/orders/{order_id}/capture`
- **Method**: `PUT`
- **Request Payload**:
  ```json
  {
    "acoustic_token": "ACU_PASS_SHA256_9f82c1e83a4d...",
    "diagnostic_pass": true,
    "snr_db": 22.4,
    "neyman_pearson_lrt": 0.42,
    "anti_spoofing_verified": true
  }
  ```
- **Response Schema (200 OK — Technician Paid)**:
  ```json
  {
    "order_id": "PL_ORD_8A92B1C4",
    "status": "CAPTURED_SETTLED",
    "settled_amount": 1250.00,
    "acoustic_token_verified": "ACU_PASS_SHA256_9f82c1e83a4d...",
    "payout_recipient": "TECH_WALLET_CREDITED",
    "timestamp": 1727712000
  }
  ```
- **Rejection Schema (400 Bad Request — Incomplete/Fake Repair)**:
  ```json
  {
    "error": "ESCROW_RELEASE_BLOCKED",
    "message": "Diagnostic acoustic test failed. Technician cannot be paid for an incomplete repair.",
    "diagnostic_pass": false
  }
  ```

---

### 3.3. Disputed Escrow Refund
- **Endpoint**: `POST https://api.pluralonline.com/api/pay/v1/orders/{order_id}/refund`
- **Method**: `POST`
- **Request Payload**:
  ```json
  {
    "order_id": "PL_ORD_8A92B1C4",
    "reason": "FAILED_POST_REPAIR_TEST_SECONDARY_AUDIT_EXPIRED",
    "refund_amount_paisa": 125000
  }
  ```
- **Response Schema**:
  ```json
  {
    "order_id": "PL_ORD_8A92B1C4",
    "status": "REFUNDED_TO_CUSTOMER",
    "reason": "FAILED_POST_REPAIR_TEST_SECONDARY_AUDIT_EXPIRED",
    "refund_timestamp": 1727712120
  }
  ```

---

## 4. Partner Innovation Capability (Mandated by Round 3)

### Partner: Pine Labs
- **Capability Name**: **Sub-Millisecond Cryptographic Acoustic Escrow Trigger**
- **Target Endpoint**: `POST /api/v1/pinelabs/escrow/conditional-trigger`
- **Underlying Partner Data**:
  Pine Labs Plural manages tokenized multi-tier payment mandates, card network pre-authorization holds, and merchant escrow settlement sub-ledgers.
- **How It Works**:
  Binds the Neyman-Pearson Likelihood Ratio Test directly to the Plural switch. Upon receiving an Ed25519-signed hardware telemetry packet from the diagnostic engine ($\Lambda(x) < 2.45 \land \text{AntiSpoof} = \text{True}$), Pine Labs executes an atomic, sub-10ms ledger transfer from escrow to the technician's bank node with zero human middleman delay.

---

## 5. Pine Labs AgenticOrg Platform Setup (`v4.8.0`)

1. **Active Organization**: `Ken's Case Competition` (Tenant: `abb61bca-a3f5-4aba-b30e-946016b13120`)
2. **User Identity**: `K.Sai Jaswanth Reddy` (`ksaijaswanthr.cs24@rvce.edu.in`) — Domain Lead | Operations.
3. **Pre-Configured Native Connector**: `pinelabs_plural` is active under finance with pre-authorized API keys and a 60/min rate limit.
4. **Execution Protocol**:
   - Agent is instantiated on AgenticOrg with System Prompt v3.0.
   - External execution mediated via Python SDK (`from agenticorg import AgenticOrg`) and Grantex RS256 token authorization.

---

## 6. Chaos Tolerances & Mitigation Architecture

| Chaos Condition | HTTP Error | Root Cause | AcuDiag Agent Self-Healing Behavior |
| :--- | :---: | :--- | :--- |
| **`low_balance`** | `402` | Pre-auth hold declined due to insufficient customer card balance. | Pauses technician dispatch; dispatches automated WhatsApp prompt with UPI instant mandate link. |
| **`timeout`** | `504` | Upstream bank core switch unresponsive (>4s). | Generates SHA-256 idempotency key; caches transaction in SQLite WAL; enters async webhook polling state. |
| **`malformed`** | Corrupt | Upstream network proxy returns HTML crash page. | Pydantic response parser catches validation error; routes through fallback health probe. |
