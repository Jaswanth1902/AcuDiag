# 🔬 Knowledge Base 01: Washing Machines — Acoustic Kinematics & Fault Profiles

> **Category**: `appliances_washing_machines`  
> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Applicable Equipment**: Front-Load & Top-Load Washing Machines (Godrej, LG, Samsung, IFB, Whirlpool)

---

## 1. Kinematic Defect Profiles & Resonances

### 1.1 Drum Bearing Outer Race Defect (BPFO)
* **Kinematic Equation**: $f_{\text{BPFO}} = \frac{N_b}{2} f_r \left(1 - \frac{d}{D} \cos \theta\right)$
* **Target Mechanical Benchmark**: SKF 6205-2RS / 6206-2RS ($N_b = 9$ balls, pitch diameter $D = 39.04\text{ mm}$, ball diameter $d = 7.94\text{ mm}$, contact angle $\theta = 0^\circ$).
* **Rotor RPM**: 800–1200 RPM during spin ramp ($f_r = 13.33\text{ Hz}$ to $20.0\text{ Hz}$).
* **Characteristic Acoustic Signature**:
  - Fundamental impact frequency: $107.4\text{ Hz}$ with strong 4th-order structural excitation centered at **$1,450\text{ Hz}$**.
  - Periodic shock wave pulses as rolling elements strike the micro-spall on the outer race.
* **Neyman-Pearson Boundary**: $\Lambda(x) = \ln \frac{P(x \mid H_1)}{P(x \mid H_0)} > 2.45$ triggers fault verification.
* **OEM Part SKU**: `BEAR-6205-2RS` (Dual rubber sealed deep groove ball bearing).
* **Cost Standard**: Part ₹850.00 | Labor ₹400.00 | Total Escrow Pre-Auth: **₹1,250.00**.

### 1.2 Drum Bearing Inner Race Defect (BPFI)
* **Kinematic Equation**: $f_{\text{BPFI}} = \frac{N_b}{2} f_r \left(1 + \frac{d}{D} \cos \theta\right) \approx 162.6\text{ Hz}$.
* **Characteristic Acoustic Signature**: High-frequency modulated amplitude envelope with sidebands spaced at rotational frequency $f_r$ ($1,450\text{ Hz} \pm 20\text{ Hz}$).
* **Neyman-Pearson Boundary**: $\Lambda(x) > 2.60$.
* **Cost Standard**: Part ₹850.00 | Labor ₹400.00 | Total Escrow Pre-Auth: **₹1,250.00**.

### 1.3 Drain Pump Impeller Lock & Cavitation Flutter
* **Physical Mechanism**: Foreign object (coin, bobby pin, lint buildup) wedged against magnetic impeller; air cavitation during drain cycle.
* **Acoustic Signature**: Low-frequency hydraulic flutter coupled with 50 Hz line hum harmonic (**$320\text{ Hz}$** cavitation peak).
* **Neyman-Pearson Boundary**: $\Lambda(x) > 3.10$.
* **OEM Part SKU**: `PUMP-DRAIN-02` (Universal 30W magnetic synchronous drain pump).
* **Cost Standard**: Part ₹600.00 | Labor ₹350.00 | Total Escrow Pre-Auth: **₹950.00**.

### 1.4 Drive Belt Slippage & Pulley Glaze
* **Physical Mechanism**: Elastomer thermal decay, loss of tensile friction on motor pulley under wet load.
* **Acoustic Signature**: Continuous friction screech at **$220\text{ Hz}$** with pitch glide during acceleration ramps.
* **Neyman-Pearson Boundary**: $\Lambda(x) > 2.80$.
* **OEM Part SKU**: `BELT-V-POLY` (Optibelt Multi-Rib 5EPJ 1225).
* **Cost Standard**: Part ₹450.00 | Labor ₹300.00 | Total Escrow Pre-Auth: **₹750.00**.

### 1.5 Suspension Friction Strut Damper Decay
* **Physical Mechanism**: Piston grease dry-out; loss of 100N hydraulic resistance causing unconstrained drum precession.
* **Acoustic Signature**: Heavy structural chassis thumping at drum fundamental rotation (**$14\text{ Hz}$ – $20\text{ Hz}$**).
* **Neyman-Pearson Boundary**: $\Lambda(x) > 2.90$.
* **OEM Part SKU**: `STRUT-SUSP-FL` (100N friction damper pair).
* **Cost Standard**: Part ₹900.00 | Labor ₹500.00 | Total Escrow Pre-Auth: **₹1,400.00**.
