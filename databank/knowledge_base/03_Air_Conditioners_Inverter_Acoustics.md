# 🔬 Knowledge Base 03: Air Conditioners — Inverter Acoustics & Gas Circuit Signatures

> **Category**: `appliances_air_conditioners`  
> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Applicable Equipment**: 1.0T / 1.5T / 2.0T Inverter Split ACs (Voltas, Daikin, Blue Star, LG, Panasonic)

---

## 1. Acoustic & Pressure Anomaly Signatures

### 1.1 Outdoor Unit (ODU) Compressor Discharge Valve Leak
* **Physical Mechanism**: Carbonized valve seat on twin-rotary inverter compressor; high-pressure R32/R410A gas blowing by during compression stroke.
* **Characteristic Acoustic Signature**:
  - High-velocity gas jet resonance producing a persistent harmonic whistle at **$2,400\text{ Hz}$**.
  - Escalates in amplitude as compressor driver ramps from 40 Hz to 85 Hz.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.85$.
* **OEM Part SKU**: `COMP-ROTARY-1.5T-R32` (High-efficiency twin rotary compressor).
* **Cost Standard**: Part ₹6,500.00 | Nitrogen pressure test & R32 charge ₹2,200.00 | Labor ₹1,200.00 | Total Escrow: **₹9,900.00**.

### 1.2 Indoor Blower Cross-Flow Fan (Tangential) Bearing Squeal
* **Physical Mechanism**: Self-lubricating bronze sleeve bearing dried out by condensation; micro-vibration of long cylindrical barrel fan.
* **Characteristic Acoustic Signature**:
  - Continuous mechanical squeal at **$640\text{ Hz}$** originating from the left indoor evaporator bracket.
  - Modulates precisely with remote control fan speed setting (Low: 850 RPM, Med: 1100 RPM, High: 1350 RPM).
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.45$.
* **OEM Part SKU**: `BEAR-BUSH-IDU-RUBBER` (Anti-vibration sleeve bearing with silicone boot).
* **Cost Standard**: Part ₹350.00 | Labor ₹500.00 | Total Escrow Pre-Auth: **₹850.00**.

### 1.3 Electronic Expansion Valve (EEV) Stepper Motor Jam
* **Physical Mechanism**: Magnetite sludge or copper shavings jamming 500-step linear pulse needle valve; outdoor unit locks expansion orifice.
* **Characteristic Acoustic Signature**:
  - Rapid pulsing clicking sound (**15 clicks at 30 Hz repetition rate**) when AC unit is powered on, followed by silence and high suction pipe frost.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 3.00$.
* **OEM Part SKU**: `VALVE-EEV-COIL-500S` (5-wire unipolar stepper coil assembly).
* **Cost Standard**: Part ₹1,200.00 | Labor ₹650.00 | Total Escrow Pre-Auth: **₹1,850.00**.

### 1.4 High-Pressure Flare Nut Gas Discharge Hiss
* **Physical Mechanism**: Over-torqued or cracked brass flare union on 1/4" liquid line; pinhole refrigerant leak.
* **Characteristic Acoustic Signature**:
  - Ultrasonic ultrasonic hiss with broad energy between **$3,500\text{ Hz}$ and $6,000\text{ Hz}$** detected near service valves.
* **Neyman-Pearson Decision Boundary**: $\Lambda(x) > 2.70$.
* **Service Standard**: Flare rework, vacuum nitrogen test, R32 recharge (₹2,400 total).
