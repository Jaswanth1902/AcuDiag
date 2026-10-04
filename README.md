<div align="center">

# 🔊 AcuDiag
### Autonomous Acoustic Vibration & Bearing Fault Diagnostic System

[![Audio Analysis](https://img.shields.io/badge/Signal-FFT%20%26%20Welch%20PSD-blue?style=flat-square)](https://github.com/Jaswanth1902/AcuDiag)
[![Hardware](https://img.shields.io/badge/Input-Standard%20Microphone-brightgreen?style=flat-square)]()
[![Domain](https://img.shields.io/badge/Application-Predictive%20Maintenance-orange?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**"Shazam for Industrial Mechanics"**  
Captures acoustic waveforms from machine motors, gearboxes, and bearings, computing real-time Fast Fourier Transforms (FFT) and Mel-spectrogram anomaly alerts to detect faults weeks before catastrophic failure.

[🚀 Quickstart](#quickstart) • [📐 Acoustic Signal Pipeline](#pipeline) • [🔬 Benchmarks](#benchmarks)

</div>

---

### 📐 Acoustic Signal Pipeline
1. **Waveform Acquisition**: Real-time microphone or WAV ingestion at 44.1 kHz.
2. **Spectral Transformation**: Fast Fourier Transform (FFT) & Welch Power Spectral Density (PSD) analysis.
3. **Harmonic Fault Matching**: Detects characteristic defect frequencies (BPFO, BPFI, BSF, FTF).
4. **Anomaly Scoring**: Alerts operators with probability scores and severity heatmaps.

---

### 🚀 Quickstart

```bash
git clone https://github.com/Jaswanth1902/AcuDiag.git
cd AcuDiag
pip install -r requirements.txt
python acudiag.py --listen --duration 10
```
