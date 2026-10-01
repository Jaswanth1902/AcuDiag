import sys
from pathlib import Path
proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

import numpy as np
from src.synthetic_acoustic_gen import ApplianceAcousticSynthesizer
from src.audio_diagnostic import AcousticDiagnosticEngine

synth = ApplianceAcousticSynthesizer(seed=42)
engine = AcousticDiagnosticEngine()

# Calibrate golden baseline
healthy = synth.generate_healthy_baseline(duration_sec=3.0)
engine.calibrate_baseline(healthy)

cases = {
    'Healthy Baseline': synth.generate_healthy_baseline(duration_sec=3.0),
    'Bearing Spall': synth.generate_bearing_fault(duration_sec=3.0, severity=1.0),
    'Drum Imbalance': synth.generate_drum_imbalance(duration_sec=3.0, severity=1.0),
    'Drain Cavitation': synth.generate_cavitation(duration_sec=3.0, severity=1.0),
    'Valve Leak': synth.generate_valve_leak(duration_sec=3.0, severity=1.0),
    'Speaker Replay Attack': synth.generate_replay_spoof(duration_sec=3.0)
}

print(f"{'Test Profile':24} | {'LRT Ratio':10} | {'Fault Status':14} | {'Replay Spoof':12} | {'SNR (dB)':8}")
print("-" * 75)
for name, audio in cases.items():
    res = engine.evaluate(audio)
    lrt = f"{res['lrt_ratio']:.2f}"
    status = res['fault_status']
    spoof = str(res['is_replay_spoof'])
    snr = f"{res['snr_db']:.1f}"
    print(f"{name:24} | {lrt:10} | {status:14} | {spoof:12} | {snr:8}")
