# 🔬 Knowledge Base 02: Refrigerators — Compressor Thermodynamics & Acoustic Profiles

> **Category**: `appliances_refrigerators`  
> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Applicable Equipment**: Frost-Free & Direct Cool Refrigerators (LG, Samsung, Whirlpool, Godrej, Haier)

---

## 1. Thermodynamic & Mechanical Failure Signatures

### 1.1 Inverter Linear / BLDC Compressor Valve Flutter
* **Physical Mechanism**: Micro-fracture or fatigue in suction flapper valve; high-pressure backflow into cylinder cavity.
* **Operating Frequency**: Variable frequency modulation between 30 Hz and 75 Hz based on inverter inverter board command.
* **Characteristic Acoustic Signature**:
  - Metallic fluttering and rhythmic ticking at **$1,850\text{ Hz}$**.
  - Loss of thermodynamic compression efficiency accompanied by warm evaporator coils.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.75$.
* **OEM Part SKU**: `COMP-INV-BLDC-01` (Universal 1/5 HP BLDC Inverter Compressor).
* **Cost Standard**: Part ₹3,800.00 | Gas Charging ₹1,200.00 | Labor ₹800.00 | Total Escrow: **₹5,800.00**.

### 1.2 Thermal Overload Protector (TOP) Relay Chattering
* **Physical Mechanism**: Locked rotor condition due to oil sludge or failed starting capacitor; bi-metallic strip cycles rapidly under high inrush current (>8 Amps).
* **Characteristic Acoustic Signature**:
  - Distinct mechanical click every 60–90 seconds followed by 50 Hz stator hum dying out within 2 seconds.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 3.20$ on periodic transient burst detection.
* **OEM Part SKU**: `RELAY-PTC-TOP-04` (Combination PTC Starter + Overload Protector).
* **Cost Standard**: Part ₹450.00 | Labor ₹350.00 | Total Escrow Pre-Auth: **₹800.00**.

### 1.3 Evaporator Fan Motor Bearing Stiction & Blade Ice Rub
* **Physical Mechanism**: Defrost drain choke causing ice buildup in evaporator chamber; fan blade tips physically contacting frost layer.
* **Characteristic Acoustic Signature**:
  - High-pitched grinding and rhythmic scraping at **$820\text{ Hz}$** originating from the freezer compartment.
  - Abruptly halts when freezer door switch is depressed.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.50$.
* **OEM Part SKU**: `FAN-EVAP-12V-DC` (Brushless DC 12V 2.5W evaporator fan motor).
* **Cost Standard**: Part ₹750.00 | Labor ₹450.00 | Total Escrow Pre-Auth: **₹1,200.00**.

### 1.4 Refrigerant Capillary Cavitation (R600a Isobutane)
* **Physical Mechanism**: Partial moisture freeze in 0.7mm capillary tube or filter drier saturation; liquid slugging into suction line.
* **Characteristic Acoustic Signature**:
  - Gurgling and hissing boiling sound centered at **$2,100\text{ Hz}$ – $2,600\text{ Hz}$**.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.30$.
* **Service Standard**: Capillary flush, molecular sieve drier replacement, R600a vacuum charging (₹1,650 total).
