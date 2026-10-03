"""
AcuDiag Acoustic Test Tone Generator
Generates realistic 10-second WAV audio files for physical WhatsApp testing:
1. fault_bearing_ricketing_1450hz.wav: Metallic clattering bearing spall (1,450 Hz BPFO + motor rumble)
2. healthy_clean_spin_motor.wav: Smooth post-repair motor hum (zero fault harmonics)
"""

import os
import sys
import numpy as np
import scipy.io.wavfile as wav
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

out_dir = Path(__file__).resolve().parent.parent / "test_audio"
out_dir.mkdir(parents=True, exist_ok=True)

sr = 44100
duration = 10.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# 1. Faulty Washing Machine: Metallic Ricketing Bearing Spall
# - Motor rumble (25 Hz & 50 Hz chassis vibration)
motor_rumble = 0.35 * np.sin(2 * np.pi * 25.0 * t) + 0.20 * np.sin(2 * np.pi * 50.0 * t)

# - Periodic bearing spall impacts at 105 Hz repetition rate
impact_rate = 105.0
impact_train = np.zeros_like(t)
impact_indices = (np.arange(0, duration, 1.0 / impact_rate) * sr).astype(int)
impact_indices = impact_indices[impact_indices < len(t)]
impact_train[impact_indices] = 1.0

# Exponentially decaying resonance at 1,450 Hz
decay_samples = int(0.006 * sr) # 6ms decay per impact
decay_kernel = np.exp(-np.linspace(0, 5, decay_samples)) * np.sin(2 * np.pi * 1450.0 * np.linspace(0, 0.006, decay_samples))
bearing_clatter = np.convolve(impact_train, decay_kernel, mode='same')
bearing_clatter = bearing_clatter / (np.max(np.abs(bearing_clatter)) + 1e-9) * 0.65

# Ambient friction noise
friction = np.random.normal(0, 0.04, len(t))

fault_audio = motor_rumble + bearing_clatter + friction
fault_audio = fault_audio / np.max(np.abs(fault_audio)) * 0.90
fault_wav_path = out_dir / "fault_bearing_ricketing_1450hz.wav"
wav.write(str(fault_wav_path), sr, (fault_audio * 32767).astype(np.int16))
print(f"✅ Generated: {fault_wav_path} ({fault_wav_path.stat().st_size} bytes)")

# 2. Healthy Machine: Smooth Post-Repair Spin
smooth_motor = 0.50 * np.sin(2 * np.pi * 30.0 * t) + 0.25 * np.sin(2 * np.pi * 60.0 * t)
clean_air = np.random.normal(0, 0.02, len(t))
healthy_audio = smooth_motor + clean_air
healthy_audio = healthy_audio / np.max(np.abs(healthy_audio)) * 0.85
healthy_wav_path = out_dir / "healthy_clean_spin_motor.wav"
wav.write(str(healthy_wav_path), sr, (healthy_audio * 32767).astype(np.int16))
print(f"✅ Generated: {healthy_wav_path} ({healthy_wav_path.stat().st_size} bytes)")

# 3. Create a simple Windows audio player script
player_code = '''"""
Play generated test audio through Windows speakers for live WhatsApp recording.
Usage:
  python scripts/play_test_audio.py --fault
  python scripts/play_test_audio.py --healthy
"""
import sys
import winsound
from pathlib import Path

test_dir = Path(__file__).resolve().parent.parent / "test_audio"
target = "fault_bearing_ricketing_1450hz.wav" if "--fault" in sys.argv else "healthy_clean_spin_motor.wav"
wav_path = test_dir / target

if not wav_path.exists():
    print(f"Error: {wav_path} not found. Run generate_audio_test_tones.py first.")
    sys.exit(1)

print(f"\\n🔊 Playing {target} through PC speakers...")
print("👉 Hold your phone within 20-30 cm of your PC speaker and record a WhatsApp voice note!\\n")
winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)
print("✅ Audio playback complete.")
'''
(Path(__file__).resolve().parent / "play_test_audio.py").write_text(player_code, encoding="utf-8")
print(f"✅ Created player: {Path(__file__).resolve().parent / 'play_test_audio.py'}")
