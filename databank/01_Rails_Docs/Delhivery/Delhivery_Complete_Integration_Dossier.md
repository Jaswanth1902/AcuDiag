# 🚚 Delhivery Rail: Comprehensive Architecture & Integration Dossier

> **Platform**: Delhivery Express & Supply Chain Platform (`delhivery.com` / `one.delhivery.com`)  
> **Target Project**: AcuDiag (Problem Space #9: Keeping the Machines Running — The Ken Case-Build 2026)  
> **Classification**: Partner Rail 3 Specification (Forward Logistics, Reverse Pickup, Doorstep QC)  
> **Environment**: Staging (`staging-express.delhivery.com`) • Production (`track.delhivery.com`) • Mock Connector

---

## 1. Executive Summary & Strategic Alignment

In consumer appliance repair, **logistics is the anti-extortion moat**. The traditional appliance repair model fails because the technician controls the parts supply chain, enabling invoice manipulation, junkyard salvage parts, and artificial markup.

**AcuDiag deploys Delhivery as an autonomous physical rail**:
1. **OEM Direct Spare Dispatch (Forward Flow)**: Once sub-10ms acoustic DSP diagnoses a failing component (e.g., Godrej washing machine drum bearing SKU `BEAR-6205-2RS`), AcuDiag autonomously manifests a genuine OEM replacement part dispatch from the nearest regional fulfillment center directly to the customer's doorstep.
2. **Doorstep Quality Check (QC)**: Delhivery field executives verify the OEM barcode, tamper seal, and physical integrity upon handover.
3. **Automated Reverse Logistics (RTO/DTO)**: Following technician replacement and post-repair acoustic verification, Delhivery reverse pickup collects the damaged/worn part for OEM forensic analysis, recycling, and core-deposit escrow release.
4. **Resilient Chaos Tolerance**: As mandated by Round 3, AcuDiag gracefully absorbs real-world logistics failures (no rider available, non-serviceable pincode clusters, upstream gateway timeouts, malformed carrier payloads).

---

## 2. Delhivery Infrastructure & Service Capabilities

Delhivery operates India's largest integrated logistics network:
- **Express Parcel**: 19,000+ PIN codes covered, door-to-door surface and air delivery.
- **Doorstep QC (Reverse Flow)**: Dedicated reverse pickup workflow where the delivery executive checks returned goods against predetermined checklist parameters before accepting parcel.
- **Fulfillment Centers (Warehousing)**: 90+ mega hubs and automated sortation centers enabling sub-day dispatch of high-velocity appliance spare parts.
- **OS1 Platform**: Operating system layer powering dispatch routing (`DispatchOne`), automated tracking (`TrackOne`), and carrier management.
- **Developer Gateway (Delhivery One)**: RESTful APIs utilizing Token authentication (`Authorization: Token <token>`), dual-environment staging/production switches, and webhooks for real-time status transitions.

---

## 3. Core Production API Specifications & Schemas

### 3.1. Pincode Serviceability & SLA Lookup
- **Endpoint**: `GET https://track.delhivery.com/c/api/pin-codes/json/?filter_codes={pincode}`
- **Staging**: `GET https://staging-express.delhivery.com/c/api/pin-codes/json/?filter_codes={pincode}`
- **Headers**:
  ```http
  Authorization: Token {{DELHIVERY_API_TOKEN}}
  Content-Type: application/json
  ```
- **Response Schema**:
  ```json
  {
    "delivery_codes": [
      {
        "postal_code": {
          "pin": 560059,
          "is_serviceable": true,
          "pre_paid": "Y",
          "cod": "N",
          "pickup": "Y",
          "repl": "Y",
          "cash": "N",
          "sort_code": "BLR/KEN",
          "hub": "BLR_KENGERI_GW",
          "state_code": "KA"
        }
      }
    ]
  }
  ```
- **AcuDiag State Trigger**: Validates customer pincode before triggering parts order. If non-serviceable (`NSZ` or `is_serviceable: false`), falls back to alternate hub or informs user via Gnani voice prompt.

---

### 3.2. Shipment Manifestation & Order Creation (CMU)
- **Endpoint**: `POST https://track.delhivery.com/api/cmu/create.json`
- **Method**: `POST` (Form-URLencoded `format=json&data={payload}` or direct application/json)
- **Headers**:
  ```http
  Authorization: Token {{DELHIVERY_API_TOKEN}}
  Content-Type: application/json
  ```
- **Request Payload (Forward Spare Part Dispatch)**:
  ```json
  {
    "shipments": [
      {
        "name": "K.Sai Jaswanth Reddy",
        "add": "RVCE Campus, Mysore Road",
        "pin": "560059",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "phone": "+919876543210",
        "order": "ACUDIAG-ORD-98214",
        "payment_mode": "Prepaid",
        "products_desc": "OEM Washing Machine Drum Bearing BEAR-6205-2RS",
        "cod_amount": "0.0",
        "order_date": "2026-09-30 16:30:00",
        "total_amount": "850.00",
        "seller_name": "Godrej Official Parts Hub",
        "seller_add": "Plot 12, Peenya Industrial Area, Bengaluru, KA",
        "seller_inv": "INV-GODREJ-4412",
        "quantity": "1",
        "weight": "0.45",
        "shipment_width": 10,
        "shipment_height": 8,
        "shipment_length": 10,
        "fragile_shipment": true,
        "return_add": "Plot 12, Peenya Industrial Area, Bengaluru, KA",
        "return_pin": "560058",
        "return_city": "Bengaluru",
        "return_state": "Karnataka",
        "return_country": "India"
      }
    ],
    "pickup_location": {
      "name": "GODREJ_BLR_PEENYA_HUB"
    }
  }
  ```
- **Response Schema**:
  ```json
  {
    "cash_pickups_count": 0,
    "package_count": 1,
    "upload_wbn": "CMU_UPLOAD_20260930_8921",
    "replacement_count": 0,
    "rmk": "None",
    "packages": [
      {
        "status": "Success",
        "client": "ACUDIAG_TECH",
        "sort_code": "BLR/KEN",
        "remarks": [""],
        "waybill": "DEL16100984210",
        "cod_amount": 0.0,
        "payment": "Prepaid",
        "serviceable": true,
        "refnum": "ACUDIAG-ORD-98214"
      }
    ],
    "success": true
  }
  ```

---

### 3.3. Reverse Pickup Request (Defective Part Return)
- **Endpoint**: `POST https://track.delhivery.com/fm/request/new/`
- **Request Payload**:
  ```json
  {
    "pickup_time": "18:00:00",
    "pickup_date": "2026-10-01",
    "pickup_location": "CUSTOMER_DOORSTEP_ACUDIAG_98214",
    "expected_package_count": 1,
    "shipment_type": "Express",
    "reverse_qc": {
      "qc_enabled": true,
      "checks": [
        "VERIFY_SERIAL_BARCODE_MATCH",
        "PHYSICAL_DESTRUCT_CHECK_ONLY",
        "OEM_METALLIC_CORE_PRESENT"
      ]
    }
  }
  ```
- **Response Schema**:
  ```json
  {
    "pr_id": 9821473,
    "pickup_date": "2026-10-01",
    "pickup_time": "18:00:00",
    "pickup_location": "CUSTOMER_DOORSTEP_ACUDIAG_98214",
    "status": "Scheduled",
    "rider_assigned": "Ramesh K (+919845012345)"
  }
  ```

---

### 3.4. Package Real-Time Tracking & Push Webhook
- **Tracking Endpoint**: `GET https://track.delhivery.com/api/v1/packages/json/?waybill={waybill}&verbose=2`
- **Response Schema**:
  ```json
  {
    "ShipmentData": [
      {
        "Shipment": {
          "AWB": "DEL16100984210",
          "Status": {
            "Status": "Out for Delivery",
            "StatusCode": "OFD",
            "StatusType": "UD",
            "StatusDateTime": "2026-10-01T09:15:00+05:30",
            "Instructions": "Contact customer before arrival"
          },
          "Consignee": {
            "Name": "K.Sai Jaswanth Reddy",
            "City": "Bengaluru",
            "PinCode": 560059
          },
          "Scans": [
            {
              "ScanDetail": {
                "ScanDateTime": "2026-09-30T19:30:00+05:30",
                "ScanType": "Manifested",
                "ScannedLocation": "Peenya Hub",
                "Instructions": "Forward Transit Initialized"
              }
            },
            {
              "ScanDetail": {
                "ScanDateTime": "2026-10-01T06:45:00+05:30",
                "ScanType": "Arrived at Destination Facility",
                "ScannedLocation": "Kengeri Delivery Center",
                "Instructions": "Bag De-consolidated"
              }
            },
            {
              "ScanDetail": {
                "ScanDateTime": "2026-10-01T09:15:00+05:30",
                "ScanType": "Out for Delivery",
                "ScannedLocation": "Kengeri Delivery Center",
                "Instructions": "Assigned to Van Route #4"
              }
            }
          ]
        }
      }
    ]
  }
  ```

---

## 4. The 3 Future Capabilities (Round 3 Innovation Requirement)

Adhavan's Round 3 instructions permit up to 3 forward-looking capabilities that the rails do not offer today, backed by existing partner data assets:

| # | Future Capability | Target Endpoint | Underlying Partner Data & Mechanics |
| :- | :--- | :--- | :--- |
| **1** | **Delhivery GeoNaksha Hyper-Local Building Drop** | `POST /api/v1/delhivery/geonaksha/validate` | **Data**: Delhivery's proprietary geospatial delivery graph (1B+ successful deliveries).<br>**Mechanic**: Resolves vague Indian addresses ("Behind temple, 2nd green gate, 3rd floor") into millimeter-accurate entrance coordinates and automated security guard OTP entry tokens. |
| **2** | **Delhivery Doorstep Acoustic Handshake Verification** | `POST /api/v1/delhivery/acoustic-qc/verify` | **Data**: Rider delivery app audio telemetry + AcuDiag Gammatone model.<br>**Mechanic**: Rider mobile app records 3 seconds of the newly installed washing machine spinning. AcuDiag verifies normal harmonic curve ($LRT < \eta$) *before* rider seals the reverse pickup bag for the old part. |
| **3** | **Delhivery Instant Core-Deposit Escrow Release** | `POST /api/v1/delhivery/escrow/release-core-deposit` | **Data**: Reverse AWB transit scan event + Pine Labs Plural Escrow order ID.<br>**Mechanic**: The exact second the reverse waybill barcode is scanned into the Delhivery hub sorter, Delhivery fires a webhook directly to Pine Labs, immediately unlocking the customer's ₹500 core-deposit hold. |

---

## 5. AcuDiag Mock Server Implementation & Chaos Simulation

Per competition rules, AcuDiag hosts a production-parity FastAPI mock server registered on Pine Labs AgenticOrg as a custom connector. It features active **Chaos Injection** to prove resilience:

```
                  ┌───────────────────────────────┐
                  │ AcuDiag Autonomous Agent      │
                  │ (Pine Labs AgenticOrg v4.8.0) │
                  └──────────────┬────────────────┘
                                 │
                   HTTP REST via Custom Connector
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │ AcuDiag 3-Rail Mock Server     │
                  │ (FastAPI Port 8000 / Vercel)  │
                  └──────────────┬────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
  [ Pincode Lookup ]     [ Order Manifest ]     [ Tracking & Chaos ]
  • /c/api/pin-codes     • /api/cmu/create      • /api/v1/packages
  • SLA & Hub routing    • Forward/Reverse AWB  • Chaos: no_rider (503)
                                                • Chaos: timeout (504)
                                                • Chaos: malformed
```

### Chaos Scenarios & Agent Mitigations
1. **`no_rider` (HTTP 503)**:
   - *Failure*: No logistics executive or van available in cluster.
   - *Agent Recovery*: Agent alerts user via Gnani voice ("Delivery delayed by 2 hours due to high local volume"), logs retry mandate, and checks alternative regional micro-depot.
2. **`timeout` (HTTP 504)**:
   - *Failure*: Upstream telecom or cloud gateway unresponsive (>4.0s).
   - *Agent Recovery*: Exponential backoff with jitter (1s $\rightarrow$ 3s $\rightarrow$ 7s), state saved in SQLite WAL blackboard (`STATE_PARTS_PENDING`).
3. **`malformed` (Non-JSON stream)**:
   - *Failure*: Upstream proxy emits raw HTML error or corrupt bytes.
   - *Agent Recovery*: Robust Pydantic parser catches validation error, isolates connection, routes through secondary health check.

---

## 6. Actionable Implementation Checklist for Round 3

- [x] Extract full Delhivery endpoint schemas from live documentation (`ucp.delhivery.com` / `track.delhivery.com`).
- [x] Codify forward dispatch, reverse DTO, and tracking models in `mock_server.py`.
- [x] Implement the 3 forward-looking capabilities with exact partner data justification.
- [x] Embed chaos injection handles (`no_rider`, `timeout`, `malformed`, `low_balance`).
- [ ] Deploy `mock_server.py` to live public endpoint (ngrok / Vercel / Railway) for Pine Labs AgenticOrg connector registration.
- [ ] Register `delhivery_logistics` connector on `https://agenticorg.hackathon.pinelabs.com`.
- [ ] Run automated Eval Cases 3, 5, and 8 (testing logistics failure recovery).
