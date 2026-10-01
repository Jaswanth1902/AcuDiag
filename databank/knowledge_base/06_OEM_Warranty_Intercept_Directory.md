# 📜 Knowledge Base 06: OEM Warranty Intercept & Consumer Protection Directory

> **Category**: `warranty_consumer_protection`  
> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Purpose**: Manufacturer Warranty Coverage Rules, Extended Compressor Warranties & Fraud Interception

---

## 1. Statutory & Manufacturer Warranty Thresholds in India

In India, an estimated 34% of paid appliance repair calls are conducted on appliances that are **still under active manufacturer warranty**, resulting in consumers paying ₹2,500 to ₹10,000 for repairs that the OEM is legally obligated to perform for free.

AcuDiag executes an automated **Warranty Intercept Gate** before any escrow pre-auth is authorized:

| Manufacturer | Category | Standard Comprehensive Warranty | Extended Motor / Compressor Warranty | Verification API / Endpoint |
| :--- | :--- | :---: | :---: | :--- |
| **Godrej Appliances** | Washing Machines | 2 Years (24 Months) | 10 Years (Direct Drive Motors) | `api.godrej.com/v1/warranty/verify` |
| **LG Electronics** | Refrigerators / Washers | 1 Year (12 Months) | 10 Years (Smart Inverter Compressor) | `api.lgservice.in/v2/claim/check` |
| **Samsung India** | Inverter Split ACs | 1 Year (12 Months) | 10 Years (Digital Inverter Compressor)| `api.samsung.com/in/warranty/status` |
| **Voltas Beko** | Refrigerators | 2 Years (24 Months) | 12 Years (ProSmart Inverter) | `api.voltas.com/oem/validate` |
| **IFB Industries** | Front-Load Washers | 4 Years (48 Months) | 10 Years (Motor & Drum) | `api.ifbappliances.com/warranty/serial` |
| **Whirlpool India** | Refrigerators | 1 Year (12 Months) | 10 Years (Intellisense Inverter) | `api.whirlpoolindia.com/verify` |

---

## 2. Autonomous Intercept Protocol

1. **Receipt / Serial Number OCR**:
   - Customer uploads purchase invoice or appliance serial plate via WhatsApp (`whatsapp__send_media_message`).
   - Agent extracts Serial Number, Purchase Date, and Model Code.
2. **Warranty Calculation**:
   - $\Delta t = t_{\text{incident}} - t_{\text{purchase}}$.
   - If $\Delta t \le \text{ComprehensiveWarranty}$ (e.g. 18 months $\le$ 24 months):
     - **ABORT PAID ESCROW IMMEDIATELY**.
     - Issue notification to user: *"Your washing machine is covered under Godrej's 2-Year Comprehensive Warranty! Do not pay ₹1,250. AcuDiag is transferring this claim directly to Godrej Peenya Service Center."*
   - If $\Delta t > \text{ComprehensiveWarranty}$ BUT fault is Compressor/Motor and $\Delta t \le \text{10 Years}$:
     - Part cost is discounted to ₹0.00 (OEM covered). Only standardized labor tariff is locked in Pine Labs Plural escrow.
3. **Consumer Savings Metric**:
   - The average Warranty Intercept saves an Indian household ₹3,200 in unnecessary out-of-pocket repair expenses.
