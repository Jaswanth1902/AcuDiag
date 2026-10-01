"""
AcuDiag Live WhatsApp Interactive Tester
Simulates real WhatsApp webhook payloads (Text & Voice Notes) hitting whatsapp_agentic_bridge.py
Verifies end-to-end processing across Gnani STT, Acoustic DSP, and Pine Labs AgenticOrg.
"""

import sys
import io
import time
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.whatsapp_agentic_bridge import app
from src.gnani_voice_client import GnaniVoiceClient

client = TestClient(app)

def test_text_intake():
    print("\n--- 1. Testing Live WhatsApp Text Intake ---")
    start = time.time()
    res = client.post(
        "/api/whatsapp/webhook",
        data={
            "From": "whatsapp:+919876543210",
            "Body": "Godrej 7kg front load washing machine making loud metallic grinding noise in 1200 rpm spin"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    elapsed = time.time() - start
    print(f"Status: {res.status_code} (took {elapsed:.2f}s)")
    print("WhatsApp TwiML XML Response:\n")
    print(res.text)

def test_voice_intake():
    print("\n--- 2. Testing Live WhatsApp Voice Note Intake (Gnani STT + DSP) ---")
    # Generate real Hindi voice clip using Gnani TTS
    gnani = GnaniVoiceClient()
    temp_wav = str(proj_root / "temp_whatsapp_voice.wav")
    print("Synthesizing test voice note via Gnani Timbre...")
    tts_res = gnani.synthesize_speech("मेरी गोदरेज वॉशिंग मशीन स्पिन साइकिल में बहुत तेज़ खड़-खड़ आवाज़ कर रही है।", output_path=temp_wav)
    print(f"Synthesized voice note: {tts_res.get('bytes_received', 0)} bytes")

    start = time.time()
    res = client.post(
        "/api/whatsapp/webhook",
        data={
            "From": "whatsapp:+919876543210",
            "MediaUrl0": temp_wav
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    elapsed = time.time() - start
    print(f"Status: {res.status_code} (took {elapsed:.2f}s)")
    print("WhatsApp TwiML XML Response:\n")
    print(res.text)
    
    # Clean up
    import os
    if os.path.exists(temp_wav):
        os.remove(temp_wav)

def test_post_repair_settlement():
    print("\n--- 3. Testing Live WhatsApp Post-Repair Spin Verification ---")
    start = time.time()
    res = client.post(
        "/api/whatsapp/webhook",
        data={
            "From": "whatsapp:+919876543210",
            "Body": "Technician finished repair, ran spin test successfully"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    elapsed = time.time() - start
    print(f"Status: {res.status_code} (took {elapsed:.2f}s)")
    print("WhatsApp TwiML XML Response:\n")
    print(res.text)

if __name__ == "__main__":
    test_text_intake()
    test_voice_intake()
    test_post_repair_settlement()
