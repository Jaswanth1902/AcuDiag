"""
Play generated test audio through Windows speakers for live WhatsApp recording.
Usage:
  python scripts/play_test_audio.py --fault
  python scripts/play_test_audio.py --healthy
"""
import sys
import winsound
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

test_dir = Path(__file__).resolve().parent.parent / "test_audio"
target = "fault_bearing_ricketing_1450hz.wav" if "--fault" in sys.argv else "healthy_clean_spin_motor.wav"
wav_path = test_dir / target

if not wav_path.exists():
    print(f"Error: {wav_path} not found. Run generate_audio_test_tones.py first.")
    sys.exit(1)

print(f"\n🔊 Playing {target} through PC speakers...")
print("👉 Hold your phone within 20-30 cm of your PC speaker and record a WhatsApp voice note!\n")
winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)
print("✅ Audio playback complete.")
