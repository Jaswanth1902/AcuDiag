# 🛡️ Knowledge Base 04: Zero-Trust Acoustic Anti-Spoofing & Fraud Gating Manual

> **Category**: `security_anti_spoofing`  
> **Platform Reference**: Pine Labs AgenticOrg Knowledge Base (`/dashboard/knowledge`)  
> **Purpose**: Formal Mathematical Criteria for Detecting Technician Audio Replay, Synthetic Sound Injection & Environmental Noise

---

## 1. Threat Models & Attack Vectors in Home Appliance Servicing

Technicians seeking illicit escrow disbursement commonly execute three classes of fraud:
1. **Speaker Replay Attack**: Playing a pre-recorded `.wav` file of a healthy running motor through a smartphone loudspeaker into the diagnostic microphone.
2. **Synthetic AI / Filter Attack**: Using frequency synthesis software or equalizer apps to mask fault harmonics.
3. **Environmental Masking**: Recording next to loud traffic, television, or pressure cookers to artificially inflate noise floors and obscure bearing spalls.

---

## 2. Mathematical Anti-Spoofing Discriminators

### 2.1 The Sub-120Hz Physical Contact Mechanical Rumble Test
* **Physical Ground Truth**: Real electric motors and washing machine drums transmit immense mechanical vibrational energy directly through their chassis into air and surface contact. Real machines have high energy in the 10 Hz – 100 Hz band.
* **Speaker Limitation**: Smartphone loudspeakers (micro-transducers) have a steep high-pass cutoff below 200 Hz due to physical cone excursion limits. Even high-end phones reproduce zero acoustic power below 120 Hz.
* **Discriminator Equation**:
  $$\text{RumbleRatio} = \frac{\int_{10\text{ Hz}}^{120\text{ Hz}} |S(f)|^2 \, df}{\int_{10\text{ Hz}}^{4000\text{ Hz}} |S(f)|^2 \, df}$$
* **Invariant Threshold**: If $\text{RumbleRatio} < 0.06$ (less than 6% low-frequency energy), the capture is classified as **`REJECTED_REPLAY_ATTACK`** (Origin: Smartphone Speaker).

### 2.2 Digital-to-Analog Converter (DAC) Quantization Jitter & Clock Peak
* **Physical Ground Truth**: DACs in mobile phones and Bluetooth speakers operate at 44.1 kHz or 48 kHz with distinctive anti-aliasing filter ringing near 16 kHz – 20 kHz.
* **Discriminator**: A sharp, unnatural spectral peak around 16.0 kHz with near-zero phase variance ($\sigma^2_\phi < 0.001$) indicates digital DAC playback rather than physical metal-on-metal friction.

### 2.3 Signal-to-Noise Ratio (SNR) Ambient Floor Gate
* **Requirement**: SNR must strictly satisfy $\text{SNR} \ge 15.0\text{ dB}$.
* **Welch Power Spectral Density Calculation**:
  $$\text{SNR}_{\text{dB}} = 10 \log_{10} \left( \frac{P_{\text{signal}}}{P_{\text{ambient\_floor}}} \right)$$
* **Gating Action**: If $\text{SNR} < 15.0\text{ dB}$, AcuDiag refuses to make a diagnostic determination, aborts the test gracefully, and instructs the customer via WhatsApp: *"Kitchen background noise too high (>85 dB). Please close doors and record from 30cm distance."*

---

## 3. Neyman-Pearson Decision Boundary Table

| Telemetry State | $\Lambda(x)$ Score | Anti-Spoof Flag | Autonomous Agent Action | Plural Escrow State |
| :--- | :---: | :---: | :--- | :--- |
| **Healthy / Clean Machine** | $\le 2.45$ | `TRUE` (Authentic) | Verification PASS; release payment to technician UPI | `CAPTURED_SETTLED` |
| **Active Defect / Fake Fix** | $> 2.45$ | `TRUE` (Authentic) | Verification FAIL; keep escrow locked; open supervisor ticket | `HOLD_DISPUTED` |
| **Speaker Replay Fraud** | Any | `FALSE` (Spoofed) | Fraud detected; block payment permanently; blacklist tech | `FROZEN_FRAUD_LOCK` |
| **Low SNR / Background Noise** | N/A | `INVALID` | Abort test; prompt customer to relocate microphone | `PRE_AUTH_LOCKED` (Unchanged) |
