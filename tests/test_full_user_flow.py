"""
AcuDiag Full User Flow End-to-End Verification Test
Validates the complete 5-step customer journey on WhatsApp:
1. "Hello" -> Greeting & triage welcome
2. Voice message in Hindi specifying repair -> Diagnostic report (Godrej, SKF 6205, ₹1,250, 26 mo warranty expired)
3. "Approve" -> Escrow locked & parts dispatched
4. Voice message / clean spin test -> Post-repair settlement verdict (LRT <= 2.45, escrow released, 90-day warranty)
5. "Thank you" -> Warm closure with active warranty confirmation
"""

import sys
import os
import unittest
from pathlib import Path

# Ensure project root is in sys.path
PROJ_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJ_ROOT))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from src.whatsapp_agentic_bridge import app, user_sessions

class TestFullUserFlow(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.phone = "919876543210"
        # Reset session
        if self.phone in user_sessions:
            del user_sessions[self.phone]

    def _send_msg(self, body_text="", audio_path=""):
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": f"{self.phone}@s.whatsapp.net",
                            "type": "audio" if audio_path else "text",
                            "text": {"body": body_text},
                            "audio": {"id": audio_path} if audio_path else {}
                        }]
                    }
                }]
            }]
        }
        resp = self.client.post("/webhook", json=payload)
        self.assertEqual(resp.status_code, 200)
        return resp.json()["reply"]

    def test_complete_five_step_flow_with_hindi_voice(self):
        """Test the exact 5 steps requested by user."""
        # ----------------------------------------------------
        # STEP 1: Hello
        # ----------------------------------------------------
        r1 = self._send_msg(body_text="Hello")
        print("\n--- STEP 1: HELLO ---")
        print(r1)
        self.assertIn("Namaste! Welcome to AcuDiag", r1)
        self.assertIn("voice note", r1)
        self.assertEqual(user_sessions.get(self.phone, {}).get("state", "INTAKE"), "INTAKE")

        # ----------------------------------------------------
        # STEP 2: Voice message in Hindi specifying repair
        # ----------------------------------------------------
        hindi_voice_transcript = (
            "मेरे गोदरेज वाशिंग मशीन स्पिन साइकिल के दौरान खट खट और क्लिक करने जैसे आवाज कर रहा है "
            "मैंने इसे लगभग २६ महीने पहले खरीदा था"
        )
        r2 = self._send_msg(body_text=hindi_voice_transcript)
        print("\n--- STEP 2: HINDI REPAIR COMPLAINT ---")
        print(r2)
        self.assertIn("AcuDiag Autonomous Diagnostic Report", r2)
        self.assertIn("Godrej", r2)
        self.assertIn("Washing Machine", r2)
        self.assertIn("GODREJ-BEAR-6205-2RS", r2)
        self.assertIn("1,250", r2)
        self.assertIn("26 month", r2.lower())
        self.assertIn("Approve", r2)
        self.assertEqual(user_sessions.get(self.phone, {}).get("state"), "INTAKE")

        # ----------------------------------------------------
        # STEP 3: Approving the escrow
        # ----------------------------------------------------
        r3 = self._send_msg(body_text="Approve")
        print("\n--- STEP 3: APPROVAL ---")
        print(r3)
        self.assertIn("AcuDiag Service Confirmed & Escrow Locked", r3)
        self.assertIn("₹1,250", r3)
        self.assertIn("Pine Labs Plural", r3)
        self.assertIn("Delhivery", r3)
        self.assertIn("SPIN TEST", r3)
        self.assertEqual(user_sessions.get(self.phone, {}).get("state"), "APPROVED")

        # ----------------------------------------------------
        # STEP 4: Voice message demonstrating good spin & spin test
        # ----------------------------------------------------
        # Scenario 4A: User sends voice message saying spin test is successful
        spin_voice_transcript = "स्पिन टेस्ट सक्सेसफुल"
        r4 = self._send_msg(body_text=spin_voice_transcript)
        print("\n--- STEP 4: SPIN TEST VERIFICATION ---")
        print(r4)
        self.assertIn("AcuDiag Post-Repair Settlement Verdict", r4)
        self.assertIn("PASSED", r4)
        self.assertIn("₹1,250.00", r4)
        self.assertIn("Pine Labs Plural", r4)
        self.assertIn("WAR-GODREJ-98214", r4)
        self.assertEqual(user_sessions.get(self.phone, {}).get("state"), "COMPLETED")

        # ----------------------------------------------------
        # STEP 5: Thank you at the end
        # ----------------------------------------------------
        r5 = self._send_msg(body_text="Thank you AcuDiag!")
        print("\n--- STEP 5: THANK YOU CLOSURE ---")
        print(r5)
        self.assertIn("You're Most Welcome from AcuDiag", r5)
        self.assertIn("RESOLVED & CLOSED", r5)
        self.assertIn("WAR-GODREJ-98214", r5)
        self.assertNotIn("Autonomous Diagnostic Report", r5)

    def test_step_4_with_healthy_audio_file(self):
        """Verify Step 4 also passes with healthy clean spin audio WAV file."""
        # Set state to APPROVED
        user_sessions[self.phone] = {"state": "APPROVED"}
        
        healthy_wav = str(PROJ_ROOT / "test_audio" / "healthy_clean_spin_motor.wav")
        r4 = self._send_msg(audio_path=healthy_wav)
        print("\n--- STEP 4 WITH HEALTHY WAV FILE ---")
        print(r4)
        self.assertIn("AcuDiag Post-Repair Settlement Verdict", r4)
        self.assertIn("PASSED", r4)
        self.assertIn("WAR-GODREJ-98214", r4)
        self.assertEqual(user_sessions.get(self.phone, {}).get("state"), "COMPLETED")

    def test_step_5_in_hindi(self):
        """Verify Step 5 works with Hindi 'धन्यवाद'."""
        user_sessions[self.phone] = {"state": "COMPLETED"}
        r5 = self._send_msg(body_text="बहुत धन्यवाद")
        self.assertIn("You're Most Welcome from AcuDiag", r5)
        self.assertIn("RESOLVED & CLOSED", r5)

if __name__ == "__main__":
    unittest.main()
